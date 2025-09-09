import json
from typing import Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import User, AnnualLeave, LeaveRequest, LeaveType

class LeaveRecommender:
    """请假推荐服务"""
    
    def __init__(self):
        """初始化请假推荐服务"""
        print("初始化请假推荐服务")
    # -> Dict 是 Python 3 的类型注解（Type Hint）语法 表示这个函数的返回值类型是 Dict（字典） 为了让代码更易读,不会影响代码运行
    def get_employee_info(self, db: Session, user_id: int) -> Dict:
        """获取员工信息"""
        # 查询用户信息
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "用户不存在"}
        
        # 查询年假信息
        current_year = datetime.now().year
        annual_leave = db.query(AnnualLeave).filter(
            AnnualLeave.user_id == user_id,
            AnnualLeave.year == current_year
        ).first()
        
        # 查询请假记录
        leave_requests = db.query(LeaveRequest).filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.status.in_(["pending", "approved"])
        ).all()
        
        # 构建员工信息
        employee_info = {
            "id": user.id,
            "name": user.full_name,
            "department": user.department,
            "position": user.position,
            "hire_date": user.hire_date.strftime("%Y-%m-%d") if user.hire_date else None,
            "employee_id": user.employee_id,
            "annual_leave": {
                "total_days": annual_leave.total_days if annual_leave else 0,  #py的三元表达式
                "used_days": annual_leave.used_days if annual_leave else 0,
                "remaining_days": annual_leave.remaining_days if annual_leave else 0
            } if annual_leave else None,
            # 列表推导式 等价于
            # leave_history = []
            # for req in leave_requests:
            #     leave_history.append({
            #         "id": req.id,
            #         "leave_type": db.query(LeaveType).get(req.leave_type_id).name,
            #         "start_date": req.start_date.strftime("%Y-%m-%d"),
            #         "end_date": req.end_date.strftime("%Y-%m-%d"),
            "leave_history": [
                {
                    "id": req.id,
                    "leave_type": db.query(LeaveType).get(req.leave_type_id).name,
                    "start_date": req.start_date.strftime("%Y-%m-%d"),
                    "end_date": req.end_date.strftime("%Y-%m-%d"),
                    "days": req.days,
                    "status": req.status
                }
                for req in leave_requests
            ]
        }
        
        return employee_info
    
    def calculate_leave_days(self, start_date: str, end_date: str) -> float:
        """计算请假天数"""
        # 解析日期
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # 计算天数差
        delta = end - start
        days = delta.days + 1  # 包含首尾两天
        
        # 计算工作日
        work_days = 0
        for i in range(days):
            day = start + timedelta(days=i)
            # 如果不是周末（5是周六，6是周日）
            if day.weekday() < 5:
                work_days += 1
        
        return work_days
    
    def generate_leave_recommendations(
        self, 
        db: Session, 
        user_id: int, 
        start_date: str,
        end_date: str,
        reason: str
    ) -> Dict:
        """生成请假推荐方案"""
        # 获取员工信息
        employee_info = self.get_employee_info(db, user_id)
        if "error" in employee_info:
            return {"error": employee_info["error"]}
        
        # 计算请假天数
        days = self.calculate_leave_days(start_date, end_date)
        
        # 获取所有请假类型
        leave_types = db.query(LeaveType).all()
        
        # 生成简单的推荐方案
        recommendations = []
        
        # 年假推荐
        annual_leave = employee_info.get("annual_leave")
        if annual_leave and annual_leave.get("remaining_days", 0) >= days:
            recommendations.append({
                "plan_name": "年假方案",
                "leave_type": "年假",
                "days": days,
                "is_compliant": True,
                "impact": "带薪休假，不影响绩效",
                "pros": ["带薪休假", "不影响绩效评估"],
                "cons": ["消耗年假额度"],
                "recommendation_level": "高"
            })
        
        # 事假推荐
        recommendations.append({
            "plan_name": "事假方案",
            "leave_type": "事假",
            "days": days,
            "is_compliant": True,
            "impact": "不带薪休假，可能影响绩效",
            "pros": ["审批流程简单", "无需提供证明"],
            "cons": ["不带薪", "可能影响绩效评估"],
            "recommendation_level": "中"
        })
        
        # 调休推荐
        recommendations.append({
            "plan_name": "调休方案",
            "leave_type": "调休",
            "days": days,
            "is_compliant": True,
            "impact": "带薪休假，不影响绩效",
            "pros": ["带薪休假", "不消耗年假额度"],
            "cons": ["需要有加班记录", "需要在3个月内使用"],
            "recommendation_level": "中"
        })
        
        return {
            "recommendations": recommendations,
            "employee_info": employee_info,
            "leave_request": {
                "start_date": start_date,
                "end_date": end_date,
                "days": days,
                "reason": reason
            }
        }

    def submit_leave_request(
        self,
        db: Session,
        user_id: int,
        leave_type_id: int,
        start_date: str,
        end_date: str,
        reason: str,
        ai_recommendation: Optional[str] = None
    ) -> Dict:
        """提交请假申请"""
        try:
            # 计算请假天数
            days = self.calculate_leave_days(start_date, end_date)
            
            # 创建请假申请
            # 你可以在 LeaveRequest 类的定义里看到类似 __tablename__ = "leave_requests"，这就指定了表名。
            # 只要是 LeaveRequest 创建的对象，db.add() 后 db.commit()，就会写入 leave_requests 表。
            leave_request = LeaveRequest(
                user_id=user_id,
                leave_type_id=leave_type_id,
                start_date=datetime.strptime(start_date, "%Y-%m-%d"),
                end_date=datetime.strptime(end_date, "%Y-%m-%d"),
                days=days,
                reason=reason,
                ai_recommendation=ai_recommendation,
                ai_recommendation_accepted=ai_recommendation is not None
            )
            
            db.add(leave_request)
            db.commit()
            db.refresh(leave_request)
            
            return {
                "status": "success",
                "message": "请假申请提交成功",
                "leave_request": {
                    "id": leave_request.id,
                    "user_id": leave_request.user_id,
                    "leave_type_id": leave_request.leave_type_id,
                    "start_date": leave_request.start_date.strftime("%Y-%m-%d"),
                    "end_date": leave_request.end_date.strftime("%Y-%m-%d"),
                    "days": leave_request.days,
                    "reason": leave_request.reason,
                    "status": leave_request.status,
                    "created_at": leave_request.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        # 异常处理，用于捕获和处理在数据库操作过程中可能发生的错误
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": f"请假申请提交失败: {str(e)}"} 