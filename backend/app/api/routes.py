from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import os
import shutil
from datetime import datetime, date

from app.database import get_db, User, LeaveType, LeaveRequest, Policy,AnnualLeave
from app.rag.leave_recommender import LeaveRecommender
from app.config import settings

router = APIRouter()
recommender = LeaveRecommender()

@router.post('/auth/login')
async def login( username: str = Body(...),password: str = Body(...),db: Session = Depends(get_db)):
    
    # 4. 查询年假数据
    user = db.query(User).filter(User.username == username,User.hashed_password == password).first()
    annual_leave =  db.query(AnnualLeave).filter(AnnualLeave.id == user.id).all()
    
    # 5. 构建响应数据
    return  {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "department": user.department,
        "position": user.position,
        "employee_id": user.employee_id,
        "hire_date": user.hire_date.strftime('%Y-%m-%d'),  # 格式化日期
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "annual_leave": [
            {
            "total_days": lt.total_days,
            "used_days": lt.used_days,
            "remaining_days": lt.remaining_days    
            }

            for lt in annual_leave
        ]
   }
# 用户相关路由
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "department": user.department,
        "position": user.position,
        "employee_id": user.employee_id,
        "hire_date": user.hire_date.strftime("%Y-%m-%d") if user.hire_date else None,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }

# 请假类型路由
@router.get("/leave-types")
async def get_leave_types(db: Session = Depends(get_db)):
    """获取所有请假类型"""
    leave_types = db.query(LeaveType).all()
    return [
        {
            "id": lt.id,
            "name": lt.name,
            "description": lt.description,
            "max_days": lt.max_days,
            "need_approval": lt.need_approval,
            "is_paid": lt.is_paid
        }
        for lt in leave_types
    ]

# 请假推荐路由
@router.post("/leave/recommend")
async def recommend_leave(
    user_id: int = Body(...),
    start_date: str = Body(...),
    end_date: str = Body(...),
    reason: str = Body(...),
    db: Session = Depends(get_db)
):
    """获取请假推荐方案"""
    try:
        recommendations = recommender.generate_leave_recommendations(
            db=db,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成推荐失败: {str(e)}"
        )

# 请假申请路由
@router.post("/leave/apply")
async def apply_leave(
    user_id: int = Body(...),
    leave_type_id: int = Body(...),
    start_date: str = Body(...),
    end_date: str = Body(...),
    reason: str = Body(...),
    ai_recommendation: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """提交请假申请"""
    result = recommender.submit_leave_request(
        db=db,
        user_id=user_id,
        leave_type_id=leave_type_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        ai_recommendation=ai_recommendation
    )
    
    if result.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message")
        )
    
    return result

# 请假记录路由
@router.get("/leave/requests/{user_id}")
async def get_leave_requests(user_id: int, db: Session = Depends(get_db)):
    """获取用户的请假记录"""
    # 以下SQLAlchemy 数据库查询的语句
    # 添加排序条件：按 created_at（创建时间）字段降序排列（desc() 表示降序）
    requests = db.query(LeaveRequest).filter(LeaveRequest.user_id == user_id).order_by(LeaveRequest.created_at.desc()).all()
    
    return [
        {
            "id": req.id,
            "user_id": req.user_id,
            "leave_type": db.query(LeaveType).get(req.leave_type_id).name,
            "start_date": req.start_date.strftime("%Y-%m-%d"),
            "end_date": req.end_date.strftime("%Y-%m-%d"),
            "days": req.days,
            "reason": req.reason,
            "status": req.status,
            "created_at": req.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for req in requests
    ]

# 政策文件上传路由
@router.post("/policies/upload")
async def upload_policy_file(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传政策文件"""
    # 检查文件类型
    allowed_extensions = [".txt", ".pdf", ".docx", ".csv", ".json"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型，仅支持: {', '.join(allowed_extensions)}"
        )
    
    # 保存文件
    file_path = os.path.join(settings.POLICY_DIR, file.filename)
    os.makedirs(settings.POLICY_DIR, exist_ok=True)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件保存失败: {str(e)}"
        )
    
    # 添加到数据库
    try:
        policy = Policy(
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_ext[1:],  # 去掉点号
            category=category,
            is_active=True
        )
        
        db.add(policy)
        db.commit()
        db.refresh(policy)
        
        return {
            "status": "success",
            "message": "政策文件上传成功",
            "policy": {
                "id": policy.id,
                "title": policy.title,
                "description": policy.description,
                "file_path": policy.file_path,
                "file_type": policy.file_type,
                "category": policy.category
            }
        }
    except Exception as e:
        db.rollback()
        # 删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"政策添加失败: {str(e)}"
        )

# 获取政策列表
@router.get("/policies")
async def get_policies(db: Session = Depends(get_db)):
    """获取所有政策"""
    policies = db.query(Policy).filter(Policy.is_active == True).all()
    
    return [
        {
            "id": policy.id,
            "title": policy.title,
            "description": policy.description,
            "file_type": policy.file_type,
            "category": policy.category,
            "created_at": policy.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for policy in policies
    ]

# 简单的聊天接口
@router.post("/chat")
async def chat(
    user_id: int = Body(...),
    message: str = Body(...),
    db: Session = Depends(get_db)
):
    """简单的聊天功能"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 简单的回复
    response = "您好！我是请假助手。请问有什么可以帮您的吗？"
    
    # 记录聊天历史
    try:
        from app.database import ChatHistory
        chat_history = ChatHistory(
            user_id=user_id,
            message=message,
            response=response
        )
        db.add(chat_history)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"记录聊天历史失败: {str(e)}")
    
    return {
        "response": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    } 