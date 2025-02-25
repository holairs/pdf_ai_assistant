import asyncpg

DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'

async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
