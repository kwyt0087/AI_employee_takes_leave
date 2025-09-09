import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置类"""
    # 应用基础配置
    APP_NAME: str = "AI请假系统"
    DEBUG: bool = True
    
    # PostgreSQL 数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "ep-delicate-band-a8h2ythn-pooler.eastus2.azure.neon.tech")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "neondb_owner")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "npg_CFPsuoeQvR67")
    DB_NAME: str = os.getenv("DB_NAME", "neondb")
    
    # 兼容旧配置
    DB_TYPE: Optional[str] = None
    VECTOR_DB_PATH: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE: Optional[str] = None
    OPENAI_API_MODEL: Optional[str] = None
    VECTOR_DB_TYPE: Optional[str] = None
    EMBEDDING_MODEL: Optional[str] = None
    UPLOAD_DIR: Optional[str] = None
    
    # 数据库连接URL
    @property
    def DATABASE_URL(self) -> str:
        """生成数据库连接URL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # JWT认证配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 文件上传配置
    POLICY_DIR: str = os.getenv("POLICY_DIR", "./policies")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 允许额外的环境变量

# 创建全局配置实例
settings = Settings()

# 请假类型配置
# LEAVE_TYPES = [
#     {"id": 1, "name": "年假", "description": "带薪年假", "need_approval": True},
#     {"id": 2, "name": "病假", "description": "因病请假", "need_approval": True},
#     {"id": 3, "name": "事假", "description": "因私事请假", "need_approval": True},
#     {"id": 4, "name": "婚假", "description": "结婚请假", "need_approval": True},
#     {"id": 5, "name": "产假", "description": "生育请假", "need_approval": True},
#     {"id": 6, "name": "丧假", "description": "亲属丧事请假", "need_approval": True},
#     {"id": 7, "name": "调休", "description": "加班调休", "need_approval": True},
# ] 