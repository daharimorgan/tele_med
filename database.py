# database.py - Database connection and optimization
import asyncpg
from asyncpg import Pool
from typing import Dict, Any, Optional

class Database:
    def __init__(self, db_url: str):
        self.pool: Optional[Pool] = None
        self.db_url = db_url
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url, min_size=10, max_size=20)
    
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
    
    async def fetch_patient(self, patient_id: str) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                SELECT p.*, u.email, u.role, u.created_at
                FROM patients p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = $1
            ''', patient_id)
    
    async def fetch_care_team(self, care_team_id: str) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
                SELECT ct.*, p.full_name as primary_provider_name
                FROM care_teams ct
                LEFT JOIN providers p ON ct.primary_provider_id = p.id
                WHERE ct.id = $1
            ''', care_team_id)
    
    async def fetch_workflows(self, patient_id: str) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            return await conn.fetch('''
                SELECT w.*, u.full_name as created_by_name
                FROM care_workflows w
                JOIN users u ON w.created_by = u.id
                WHERE w.patient_id = $1
                ORDER BY w.created_at DESC
            ''', patient_id)
    
    async def search_patients(self, query: str) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            return await conn.fetch('''
                SELECT p.id, p.demographics->>'name' as name, p.demographics->>'mrn' as mrn
                FROM patients p
                WHERE
                    p.demographics->>'name' ILIKE $1 OR
                    p.demographics->>'mrn' ILIKE $1 OR
                    p.demographics->>'email' ILIKE $1
                LIMIT 50
            ''', f"%{query}%")
    
    async def update_patient_document(self, patient_id: str, document_id: str, data: Dict[str, Any]) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute('''
                INSERT INTO documents (id, patient_id, content, created_at)
                VALUES ($1, $2, $3, NOW())
                ON CONFLICT (id) DO UPDATE
                SET content = $3, updated_at = NOW()
            ''', document_id, patient_id, data)
            return result != 'INSERT 0 0'

# Usage
db = Database('postgres://user:password@localhost/careconnect')
async def startup():
    await db.connect()

async def shutdown():
    await db.disconnect()