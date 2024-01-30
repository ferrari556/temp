from fastapi import APIRouter, UploadFile, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.login_service import get_current_user_authorization
from services.upload_service import uploadtoazure
from models.users import User
from sqlalchemy.future import select

router = APIRouter()

@router.post("/uploadfile", tags=["UploadFile"])
async def create_upload_file(request: Request, file: UploadFile, db: AsyncSession = Depends(get_db)):
    login_id = await get_current_user_authorization(request)
    user_id = await get_user_id_by_login_id(db, login_id)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    file_data = await file.read()
    return await uploadtoazure(file.filename, file.content_type, file_data, user_id, db)

async def get_user_id_by_login_id(db: AsyncSession, login_id: str):
    result = await db.execute(select(User).filter_by(login_id=login_id))
    user = result.scalar_one_or_none()
    return user.user_id if user else None