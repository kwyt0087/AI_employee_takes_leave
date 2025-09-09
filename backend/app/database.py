from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
import os

from app.config import settings

# 打印数据库连接信息
print(f"数据库URL: {settings.DATABASE_URL}")

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 定义数据模型
class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    department = Column(String(50))
    position = Column(String(50))
    employee_id = Column(String(20), unique=True)
    hire_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    # leave_requests = relationship("LeaveRequest", back_populates="user", foreign_keys="LeaveRequest.user_id")
    leave_requests = relationship("LeaveRequest", backref="user", foreign_keys="LeaveRequest.user_id")
    annual_leaves = relationship("AnnualLeave", back_populates="user")

class LeaveRequest(Base):
    """请假申请模型"""
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ForeignKey("leave_types.id") 表示：
# 这个字段是一个外键，它关联到 leave_types 表（即 LeaveType 模型）里的 id 字段。
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    days = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    approver_id = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    ai_recommendation = Column(Text)
    ai_recommendation_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    # user = relationship("User", foreign_keys=[user_id], back_populates="leave_requests")
    leave_type = relationship("LeaveType", back_populates="leave_requests")
    approver = relationship("User", foreign_keys=[approver_id])

class AnnualLeave(Base):
    """年假记录模型"""
    __tablename__ = "annual_leaves"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0)
    remaining_days = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="annual_leaves")

class LeaveType(Base):
    """请假类型模型"""
    __tablename__ = "leave_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    max_days = Column(Integer)
    need_approval = Column(Boolean, default=True)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    leave_requests = relationship("LeaveRequest", back_populates="leave_type")



class Policy(Base):
    """公司政策模型"""
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    file_path = Column(String(255))
    file_type = Column(String(20))
    category = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatHistory(Base):
    """聊天历史记录模型"""
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User")

# 数据库初始化函数
def init_db():
    """初始化数据库，创建所有表"""
    # 确保目录存在
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./policies", exist_ok=True)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 添加初始数据
    db = SessionLocal()
    try:
        # 检查是否已有请假类型数据
        if db.query(LeaveType).count() == 0:
            # 添加请假类型
            leave_types = [
                LeaveType(name="年假", description="带薪年假", is_paid=True),
                LeaveType(name="病假", description="因病请假", max_days=15, is_paid=False),
                LeaveType(name="事假", description="因私事请假", is_paid=False),
                LeaveType(name="婚假", description="结婚请假", max_days=10, is_paid=True),
                LeaveType(name="产假", description="生育请假", max_days=98, is_paid=True),
                LeaveType(name="丧假", description="亲属丧事请假", max_days=3, is_paid=True),
                LeaveType(name="调休", description="加班调休", is_paid=True),
            ]
            db.add_all(leave_types)
            db.commit()
            print("已添加初始请假类型数据")
    except Exception as e:
        db.rollback()
        print(f"添加初始数据失败: {e}")
    finally:
        db.close()

# 获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 