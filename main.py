from fastapi import FastAPI
from sqlalchemy import create_engine
from config.database import engine
import uvicorn
from models.AudioFiles import Base as AudioFiles 
from models.users import Base as users  
from routers import (
    users_route,
    upload_route,
)

# 초기 데이터베이스 연결
# DatabaseURL = 'mysql+pymysql://root:1234@localhost:3306/test'
DatabaseURL = 'mysql+pymysql://root:1234@localhost:3306/test'
engine = create_engine(DatabaseURL)

app = FastAPI()

# API 암호화
# setup_cors(app)

# 원하는 데이터베이스 생성
AudioFiles.metadata.create_all(bind=engine)
users.metadata.create_all(bind=engine)

# Prefix는 엔드포인트를 정할 때 사용
app.include_router(users_route.router, prefix="", tags=["Users"])
app.include_router(upload_route.router, prefix="", tags=["UploadFile"])

@app.get('/')
def home():
    return {'msg' : 'Creating DB'}

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)

