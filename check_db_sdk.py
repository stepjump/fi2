import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def fetch_posts():
    try:
        # posts 테이블에서 모든 데이터 조회
        response = supabase.table("posts").select("*").execute()
        
        print(f"--- 게시글 목록 ({len(response.data)}건) ---")
        for post in response.data:
            print(f"ID: {post['id']} | 제목: {post['title']} | 조회수: {post['view_count']}")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    fetch_posts()