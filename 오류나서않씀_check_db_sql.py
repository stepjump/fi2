import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def fetch_posts_sql():
    # 엔진 생성
    engine = create_async_engine(DATABASE_URL)
    # 세션 생성
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        try:
            # 직접 SQL 쿼리 실행
            result = await session.execute(text("SELECT id, title, view_count FROM posts"))
            posts = result.all()
            
            print(f"--- SQL 조회 결과 ({len(posts)}건) ---")
            for post in posts:
                print(f"ID: {post.id} | 제목: {post.title} | 조회수: {post.view_count}")
        except Exception as e:
            print(f"연결 오류: {e}")
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fetch_posts_sql())