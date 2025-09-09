# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# 生成测试数据并导入数据库
# """
# import random
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.database import Base, User, AnnualLeave, LeaveType, LeaveRequest, Policy, ChatHistory
# from app.config import settings

# # 连接数据库
# engine = create_engine(settings.DATABASE_URL, echo=False)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def create_test_data():
#     """创建测试数据"""
#     # 创建所有表
#     Base.metadata.create_all(bind=engine)
    
#     # 创建数据库会话
#     db = SessionLocal()
    
#     try:
#         # 1. 添加请假类型数据
#         leave_type_data = [
#             {"name":"年假", "description":"员工带薪年假", "max_days":15, "need_approval":True, "is_paid":True},
#             {"name":"病假", "description":"员工因病请假", "max_days":30, "need_approval":True, "is_paid":True},
#             {"name":"事假", "description":"员工个人事务请假", "max_days":10, "need_approval":True, "is_paid":False},
#             {"name":"婚假", "description":"员工结婚请假", "max_days":3, "need_approval":True, "is_paid":True},
#             {"name":"产假", "description":"女性员工产假", "max_days":98, "need_approval":True, "is_paid":True},
#             {"name":"陪产假", "description":"男性员工陪产假", "max_days":15, "need_approval":True, "is_paid":True},
#             {"name":"丧假", "description":"员工直系亲属去世请假", "max_days":3, "need_approval":True, "is_paid":True},
#         ]
        
#         added_leave_types = 0
#         for data in leave_type_data:
#             # 检查是否已存在
#             existing = db.query(LeaveType).filter(LeaveType.name == data["name"]).first()
#             if not existing:
#                 leave_type = LeaveType(**data)
#                 db.add(leave_type)
#                 added_leave_types += 1
#         db.commit()
#         print(f"已添加 {added_leave_types} 条请假类型数据")
        
#         # 2. 添加用户数据
#         departments = ["技术部", "市场部", "人力资源部", "财务部", "销售部"]
#         positions = ["经理", "主管", "专员", "助理", "实习生"]
        
#         added_users = 0
#         # 查找已存在的最大用户ID
#         max_id = db.query(User.id).order_by(User.id.desc()).first()
#         start_id = max_id[0] + 1 if max_id else 1
        
#         for i in range(start_id, start_id + 20):
#             username = f"user{i}"
#             # 检查是否已存在
#             existing = db.query(User).filter(User.username == username).first()
#             if not existing:
#                 hire_date = datetime.now() - timedelta(days=random.randint(365, 1825))  # 入职1-5年
#                 user = User(
#                     username=username,
#                     email=f"user{i}@example.com",
#                     hashed_password=f"password{i}",  # 实际应用中应该加密
#                     full_name=f"员工{i}",
#                     department=random.choice(departments),
#                     position=random.choice(positions),
#                     employee_id=f"EMP{i:04d}",
#                     hire_date=hire_date,
#                     is_active=True,
#                     is_admin=True if i == start_id else False  # 第一个新用户是管理员
#                 )
#                 db.add(user)
#                 added_users += 1
#         db.commit()
#         print(f"已添加 {added_users} 条用户数据")
        
#         # 3. 添加年假数据
#         current_year = datetime.now().year
        
#         added_annual_leaves = 0
#         # 获取所有用户
#         all_users = db.query(User).all()
#         for user in all_users:
#             # 检查是否已存在今年的年假记录
#             existing = db.query(AnnualLeave).filter(
#                 AnnualLeave.user_id == user.id,
#                 AnnualLeave.year == current_year
#             ).first()
#             if not existing:
#                 # 根据入职年限计算年假天数 (1-5年每年10天, 5年以上15天)
#                 hire_years = (datetime.now() - user.hire_date).days // 365
#                 total_days = 15 if hire_years >= 5 else 10
#                 used_days = random.uniform(0, total_days * 0.8)  # 使用0-80%的年假
#                 remaining_days = total_days - used_days
                
#                 annual_leave = AnnualLeave(
#                     user_id=user.id,
#                     year=current_year,
#                     total_days=total_days,
#                     used_days=used_days,
#                     remaining_days=remaining_days
#                 )
#                 db.add(annual_leave)
#                 added_annual_leaves += 1
#         db.commit()
#         print(f"已添加 {added_annual_leaves} 条年假数据")
        
#         # 4. 添加请假申请数据
#         statuses = ["pending", "approved", "rejected"]
#         reasons = [
#             "家中有事需要处理",
#             "身体不适需要休息",
#             "需要回家探望父母",
#             "结婚需要请假",
#             "妻子生产需要陪护",
#             "亲人去世需要奔丧",
#             "个人事务需要处理"
#         ]
        
#         # 获取所有用户和请假类型
#         all_users = db.query(User).all()
#         all_leave_types = db.query(LeaveType).all()
        
#         added_leave_requests = 0
#         for user in all_users:
#             # 每个用户最多添加5条请假记录
#             existing_count = db.query(LeaveRequest).filter(LeaveRequest.user_id == user.id).count()
#             max_add = 5 - existing_count
#             if max_add > 0:
#                 for _ in range(random.randint(1, max_add)):
#                     # 随机选择请假类型
#                     leave_type = random.choice(all_leave_types)
                    
#                     # 随机生成请假开始和结束日期
#                     start_date = datetime.now() - timedelta(days=random.randint(1, 365))
#                     end_date = start_date + timedelta(days=random.randint(1, 5))
                    
#                     # 计算请假天数
#                     days = (end_date - start_date).days + 1
                    
#                     # 随机选择状态
#                     status = random.choice(statuses)
                    
#                     # 随机选择审批人 (除了自己)
#                     approver_id = random.choice([u.id for u in all_users if u.id != user.id])
                    
#                     leave_request = LeaveRequest(
#                         user_id=user.id,
#                         leave_type_id=leave_type.id,
#                         start_date=start_date,
#                         end_date=end_date,
#                         days=days,
#                         reason=random.choice(reasons),
#                         status=status,
#                         approver_id=approver_id if status != "pending" else None,
#                         approved_at=datetime.now() if status != "pending" else None,
#                         ai_recommendation="推荐使用年假" if leave_type.name == "年假" else None,
#                         ai_recommendation_accepted=random.choice([True, False]) if status != "pending" else False
#                     )
#                     db.add(leave_request)
#                     added_leave_requests += 1
#         db.commit()
#         print(f"已添加 {added_leave_requests} 条请假申请数据")
        
#                 # 5. 添加公司政策数据
#         policy_categories = ["请假政策", "福利政策", "考勤政策", "奖惩政策", "培训政策"]
#         policy_titles = [
#             "员工请假管理规定", "年度福利计划", "考勤制度实施细则",
#             "员工奖惩办法", "培训发展计划", "差旅费报销规定",
#             "绩效考核制度", "保密协议", "劳动合同管理办法"
#         ]
#         policy_descriptions = [
#             "本规定旨在规范员工请假流程，保障公司正常运转和员工合法权益。",
#             "公司为员工提供全面的福利保障，包括社会保险、商业保险、带薪年假等。",
#             "为加强公司考勤管理，维护工作秩序，提高工作效率，特制定本细则。",
#             "为激励员工积极工作，惩处违规行为，维护公司正常的工作秩序。",
#             "公司重视员工培训与发展，为员工提供丰富的培训机会和发展空间。"
#         ]
#         file_types = ["pdf", "doc", "docx", "xls", "xlsx"]

#         added_policies = 0
#         for i in range(10):
#             title = random.choice(policy_titles)
#             # 检查是否已存在
#             existing = db.query(Policy).filter(Policy.title == title).first()
#             if not existing:
#                 policy = Policy(
#                     title=title,
#                     description=random.choice(policy_descriptions),
#                     file_path=f"/policies/policy_{i+1}.{random.choice(file_types)}",
#                     file_type=random.choice(file_types),
#                     category=random.choice(policy_categories),
#                     is_active=random.choice([True, False])
#                 )
#                 db.add(policy)
#                 added_policies += 1
#         db.commit()
#         print(f"已添加 {added_policies} 条公司政策数据")

#         # 6. 添加聊天历史记录数据
#         chat_messages = [
#             "如何申请年假？",
#             "请帮我推荐最佳请假方案。",
#             "我的年假还剩多少天？",
#             "病假需要提供什么证明？",
#             "婚假可以请多少天？",
#             "产假的薪资怎么计算？",
#             "如何提交请假申请？",
#             "请假审批需要多长时间？"
#         ]
#         chat_responses = [
#             "您可以通过系统提交年假申请，流程通常需要1-3个工作日审批。",
#             "根据您的情况，推荐您使用年假，剩余年假天数为5天。",
#             "查询到您当前剩余年假天数为5天。",
#             "病假需要提供二级以上医院开具的诊断证明。",
#             "根据公司规定，婚假为3天，晚婚可额外享受7天。",
#             "产假期间薪资按照基本工资的80%发放。",
#             "您可以在系统首页点击'请假申请'按钮提交申请。",
#             "请假审批通常需要1-3个工作日，紧急情况可联系HR加急处理。"
#         ]

#         added_chat_histories = 0
#         # 为部分用户添加聊天记录
#         for user in random.sample(all_users, min(10, len(all_users))):
#             # 每个用户添加2-5条聊天记录
#             for _ in range(random.randint(2, 5)):
#                 chat_history = ChatHistory(
#                     user_id=user.id,
#                     message=random.choice(chat_messages),
#                     response=random.choice(chat_responses),
#                     created_at=datetime.now() - timedelta(days=random.randint(1, 90))
#                 )
#                 db.add(chat_history)
#                 added_chat_histories += 1
#         db.commit()
#         print(f"已添加 {added_chat_histories} 条聊天历史记录数据")

#         print("测试数据导入完成!")
#     except Exception as e:
#         print(f"导入测试数据时出错: {e}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     create_test_data()