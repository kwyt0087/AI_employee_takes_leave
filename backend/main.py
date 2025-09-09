from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.api.routes import router as api_router

# 初始化FastAPI应用
app = FastAPI(
    title="AI请假系统",
    description="智能请假申请和推荐系统",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api")

# 挂载静态文件目录（用于政策文件上传）
app.mount("/files", StaticFiles(directory="./policies"), name="files")

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    print("开始初始化数据库...")
    init_db()
    print("数据库初始化完成")

@app.get("/")
async def root():
    """根路径访问"""
    return {"message": "AI请假系统API服务"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 