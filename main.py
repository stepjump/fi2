# ========================================================================
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# [배포 하는법]
# git pull
# git add .
# git commit -m "update app"
# git push origin main
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# # 초기화
# git pull origin main --rebase
# git push origin main
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# [배포 시도시 충돌났을때 처리]
# git stash
# git pull origin main
# git stash pop
# git push -f origin main
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# ========================================================================

import os
import bcrypt
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. 환경 변수 로드 및 초기화
load_dotenv()

app = FastAPI(title="Python & Supabase Board API", version="1.1.0")

# CORS 설정 (Vue3 통신용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase 설정
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise ValueError(".env 파일에 SUPABASE_URL과 SUPABASE_KEY가 필요합니다.")
supabase: Client = create_client(url, key)

# --- 2. 보안 유틸리티 (bcrypt 직접 사용) ---

def hash_password(password: str) -> str:
    """비밀번호를 안전하게 해싱합니다 (최대 72바이트 제한 대응)"""
    pw_bytes = password.encode('utf-8')
    # bcrypt 제한인 72바이트를 넘으면 잘라줌
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력받은 비밀번호와 DB 해시값을 비교합니다."""
    try:
        pw_bytes = plain_password.encode('utf-8')
        if len(pw_bytes) > 72:
            pw_bytes = pw_bytes[:72]
        return bcrypt.checkpw(pw_bytes, hashed_password.encode('utf-8'))
    except Exception:
        return False

# --- 3. 데이터 모델 (Pydantic) ---

class PostCreate(BaseModel):
    title: str
    content: str
    password: str
    parent_id: Optional[int] = None

class PostUpdate(BaseModel):
    title: str
    content: str
    password: str

class PasswordRequest(BaseModel):
    password: str

# --- 4. API 엔드포인트 ---

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "API Server is running"}

# [목록 조회] 삭제되지 않은 글만 최신순으로
@app.get("/posts")
async def get_posts():
    try:
        response = supabase.table("posts") \
            .select("id, title, view_count, created_at, parent_id") \
            .neq("delete_yn", "y") \
            .order("created_at", desc=True) \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"목록 조회 오류: {str(e)}")

# [상세 조회] 조회수 증가 및 댓글 포함
@app.get("/posts/{post_id}")
async def get_post_detail(post_id: int = Path(..., description="조회할 글 ID")):
    try:
        # 1. 글 정보 조회
        post_res = supabase.table("posts") \
            .select("*, parent:parent_id(title)") \
            .eq("id", post_id) \
            .neq("delete_yn", "y") \
            .execute()
        
        if not post_res.data:
            raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
        
        post_data = post_res.data[0]
        
        # 2. 조회수 증가
        new_views = (post_data.get("view_count") or 0) + 1
        supabase.table("posts").update({"view_count": new_views}).eq("id", post_id).execute()
        post_data["view_count"] = new_views

        # 3. 댓글 조회
        comments_res = supabase.table("comments").select("*").eq("post_id", post_id).execute()

        return {"post": post_data, "comments": comments_res.data}
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# [생성] 새 글 또는 답변 작성
@app.post("/posts")
async def create_post(post: PostCreate):
    try:
        post_dict = post.model_dump() # Pydantic v2 기준 (안되면 .dict() 사용)
        post_dict["password"] = hash_password(post.password)
        post_dict["delete_yn"] = ""
        
        response = supabase.table("posts").insert(post_dict).execute()
        return {"message": "작성 성공", "id": response.data[0]["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"작성 오류: {str(e)}")

# [수정] 비밀번호 확인 후 제목/내용 변경
@app.put("/posts/{post_id}")
async def update_post(post_id: int, request: PostUpdate):
    try:
        post_res = supabase.table("posts").select("password").eq("id", post_id).execute()
        if not post_res.data: raise HTTPException(status_code=404, detail="글 없음")
        
        if not verify_password(request.password, post_res.data[0]["password"]):
            raise HTTPException(status_code=403, detail="비밀번호 불일치")
        
        update_data = {"title": request.title, "content": request.content}
        supabase.table("posts").update(update_data).eq("id", post_id).execute()
        return {"message": "수정 성공"}
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# [삭제] 비밀번호 확인 후 Soft Delete
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, request: PasswordRequest):
    try:
        post_res = supabase.table("posts").select("password").eq("id", post_id).execute()
        if not post_res.data: raise HTTPException(status_code=404, detail="글 없음")
        
        if not verify_password(request.password, post_res.data[0]["password"]):
            raise HTTPException(status_code=403, detail="비밀번호 불일치")
        
        supabase.table("posts").update({"delete_yn": "y"}).eq("id", post_id).execute()
        return {"message": "삭제 성공"}
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)