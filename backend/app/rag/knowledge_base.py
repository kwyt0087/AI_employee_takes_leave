import os
import glob
from typing import List, Dict, Any, Optional
import json

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    Docx2txtLoader, 
    CSVLoader,
    JSONLoader
)
from langchain_community.vectorstores import Chroma

from app.config import settings
from app.database import SessionLocal, Policy

# 全局变量，存储向量数据库实例
vector_store = None

def init_knowledge_base():
    """初始化知识库
    
    加载所有政策文件，创建向量数据库
    """
    global vector_store
    
    print("开始初始化知识库...")
    
    # 确保向量数据库目录存在
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    print(f"向量数据库目录已确认: {settings.VECTOR_DB_PATH}")
    
    # 检查是否设置了API密钥
    if not settings.DEEPSEEK_API_KEY:
        print("警告: 未设置有效的 DEEPSEEK_API_KEY，将使用假数据初始化知识库")
        # 创建一个假的向量存储，用于开发测试
        vector_store = MockVectorStore()
        return
    
    try:
        # 获取所有政策文件
        db = SessionLocal()
        try:
            # 首先检查policies表是否存在
            try:
                print("检查policies表是否存在...")
                db.execute("SELECT 1 FROM policies LIMIT 1")
                print("policies表存在，继续初始化知识库")
            except Exception as e:
                print(f"policies表不存在或无法访问: {e}")
                print("将使用假数据初始化知识库")
                vector_store = MockVectorStore()
                return
                
            print("开始查询政策数据...")
            policies = db.query(Policy).filter(Policy.is_active == True).all()
            print(f"查询到 {len(policies)} 条政策数据")
            
            # 如果没有政策文件，加载示例政策
            if len(policies) == 0:
                print("没有找到政策文件，加载示例政策")
                load_example_policies()
                policies = db.query(Policy).filter(Policy.is_active == True).all()
                print(f"加载示例政策后，共有 {len(policies)} 条政策数据")
            
            # 加载所有文档
            documents = []
            for policy in policies:
                try:
                    file_path = policy.file_path
                    if not os.path.exists(file_path):
                        print(f"文件不存在: {file_path}")
                        continue
                    
                    # 根据文件类型选择加载器
                    if file_path.endswith('.txt'):
                        loader = TextLoader(file_path, encoding='utf-8')
                    elif file_path.endswith('.pdf'):
                        loader = PyPDFLoader(file_path)
                    elif file_path.endswith('.docx'):
                        loader = Docx2txtLoader(file_path)
                    elif file_path.endswith('.csv'):
                        loader = CSVLoader(file_path)
                    elif file_path.endswith('.json'):
                        loader = JSONLoader(
                            file_path=file_path,
                            jq_schema='.[]',
                            text_content=False
                        )
                    else:
                        print(f"不支持的文件类型: {file_path}")
                        continue
                    
                    # 加载文档
                    docs = loader.load()
                    
                    # 添加元数据
                    for doc in docs:
                        doc.metadata["title"] = policy.title
                        doc.metadata["description"] = policy.description
                        doc.metadata["category"] = policy.category
                        doc.metadata["policy_id"] = policy.id
                    
                    documents.extend(docs)
                    print(f"已加载文档: {file_path}, 文档数: {len(docs)}")
                except Exception as e:
                    print(f"加载文档失败: {file_path}, 错误: {e}")
            
            # 如果没有成功加载任何文档，使用假数据
            if not documents:
                print("未能加载任何文档，将使用假数据初始化知识库")
                vector_store = MockVectorStore()
                return
                
            print(f"共加载 {len(documents)} 个文档，开始文本分割...")
            
            # 文本分割
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", "。", "，", ".", ",", " ", ""]
            )
            
            chunks = text_splitter.split_documents(documents)
            print(f"文档分块完成，共 {len(chunks)} 个块")
            
            # 创建向量数据库 (使用假的嵌入)
            print("创建向量数据库...")
            vector_store = MockVectorStore()
            print("向量数据库创建完成")
            
        except Exception as e:
            print(f"初始化知识库失败: {e}")
            import traceback
            traceback.print_exc()
            # 使用假数据初始化知识库
            print("将使用假数据初始化知识库")
            vector_store = MockVectorStore()
        finally:
            db.close()
            print("数据库连接已关闭")
    except Exception as e:
        print(f"初始化知识库失败: {e}")
        import traceback
        traceback.print_exc()
        # 创建一个假的向量存储，用于开发测试
        print("将使用假数据初始化知识库")
        vector_store = MockVectorStore()

def query_knowledge_base(query: str, top_k: int = 5) -> List[Document]:
    """查询知识库
    
    根据查询文本返回相关文档
    
    Args:
        query: 查询文本
        top_k: 返回的文档数量
        
    Returns:
        相关文档列表
    """
    # 使用模拟数据代替向量检索
    print(f"查询知识库: {query}")
    
    # 返回模拟文档
    mock_docs = [
        Document(
            page_content="公司请假制度规定：年假每年最多15天，病假需要医院证明，事假不带薪。",
            metadata={"title": "请假政策", "source": "mock"}
        ),
        Document(
            page_content="加班调休规定：加班1天可调休1天，需在3个月内使用完毕。",
            metadata={"title": "加班调休", "source": "mock"}
        ),
        Document(
            page_content="婚假规定：员工结婚可享受3天带薪婚假，需提供结婚证明。",
            metadata={"title": "婚假政策", "source": "mock"}
        ),
        Document(
            page_content="产假规定：女员工生育可享受98天产假，难产可增加15天。",
            metadata={"title": "产假政策", "source": "mock"}
        ),
        Document(
            page_content="丧假规定：直系亲属去世可享受3天带薪丧假。",
            metadata={"title": "丧假政策", "source": "mock"}
        )
    ]
    
    return mock_docs[:min(top_k, len(mock_docs))]

def get_qa_response(query: str) -> Dict:
    """获取问答响应
    
    使用DeepSeek API回答问题
    
    Args:
        query: 问题文本
        
    Returns:
        回答结果
    """
    # 使用模拟数据代替API调用
    print(f"问答查询: {query}")
    
    # 返回模拟回答
    return {
        "result": "这是一个模拟的回答，实际开发中应该调用DeepSeek API。",
        "source_documents": query_knowledge_base(query)
    }

def load_example_policies():
    """加载示例政策文件
    
    当没有政策文件时，创建并加载示例政策
    """
    # 确保政策目录存在
    os.makedirs(settings.POLICY_DIR, exist_ok=True)
    
    # 示例政策内容
    example_policies = [
        {
            "title": "公司请假制度",
            "content": """
# 公司请假制度

## 1. 年假规定
- 工作满1年的员工可享受带薪年假
- 工作1-10年的员工每年可享受5天年假
- 工作10-20年的员工每年可享受10天年假
- 工作20年以上的员工每年可享受15天年假
- 年假应提前3个工作日申请
- 年假可以按天或半天为单位使用

## 2. 病假规定
- 病假需提供医院证明
- 病假3天以内的，需提供医院就诊证明
- 病假3天以上的，需提供医院诊断证明
- 病假期间，前3天按照基本工资的80%发放，第4天起按照基本工资的60%发放

## 3. 事假规定
- 事假需提前1个工作日申请
- 事假不享受工资
- 全年事假累计不得超过15天

## 4. 婚假规定
- 员工本人结婚可享受3天婚假
- 婚假期间享受正常工资
- 婚假应在结婚登记后一年内使用完毕

## 5. 产假规定
- 女员工生育可享受98天产假
- 难产的，增加产假15天
- 多胞胎生育的，每多生育一个婴儿，增加产假15天
- 产假期间享受生育保险待遇

## 6. 丧假规定
- 直系亲属（父母、配偶、子女）去世，可享受3天丧假
- 其他亲属去世，可享受1天丧假
- 丧假期间享受正常工资

## 7. 调休规定
- 因工作需要加班的，可安排调休
- 调休应在加班后3个月内使用完毕
- 调休按照1:1的比例安排
            """,
            "file_type": "txt",
            "category": "leave"
        },
        {
            "title": "考勤制度",
            "content": """
# 公司考勤制度

## 1. 工作时间
- 正常工作时间：周一至周五 9:00-18:00，中午休息1小时
- 弹性工作时间：允许前后浮动1小时，即8:00-17:00或10:00-19:00
- 核心工作时间：10:00-16:00，所有员工必须在岗

## 2. 打卡规定
- 所有员工必须进行上下班打卡
- 打卡方式：指纹打卡或手机APP打卡
- 每日打卡次数：上午上班1次，下午下班1次

## 3. 迟到早退
- 迟到：上班时间后15分钟（含）以内到岗为迟到
- 早退：下班时间前15分钟（含）以内离岗为早退
- 迟到或早退超过15分钟，按旷工0.25天计算
- 迟到或早退3次，视为旷工1天

## 4. 旷工
- 无故缺勤视为旷工
- 旷工1天，扣除当日工资的3倍
- 连续旷工3天或全年累计旷工10天，公司有权解除劳动合同

## 5. 外出登记
- 工作时间内因公外出，需填写外出登记表
- 外出时间超过2小时，需部门经理审批
- 外出返回后，需及时销假

## 6. 加班管理
- 加班需提前申请，并经部门经理批准
- 加班时间计算：工作日18:00后，周末及法定节假日
- 加班费计算：工作日加班1.5倍工资，周末加班2倍工资，法定节假日加班3倍工资
- 加班可选择调休或领取加班费

## 7. 请假规定
- 请假需提前申请，并按照请假流程审批
- 请假时间小于半天的，按半天计算；大于半天小于1天的，按1天计算
- 未经批准的请假，视为旷工
            """,
            "file_type": "txt",
            "category": "attendance"
        },
        {
            "title": "加班调休规定",
            "content": """
# 加班调休规定

## 1. 调休资格
- 因工作需要，经部门负责人批准加班的员工可申请调休
- 加班时长满4小时可申请半天调休，满8小时可申请1天调休

## 2. 调休申请
- 调休需提前1个工作日申请
- 调休申请需经部门负责人批准
- 调休应在加班后3个月内使用完毕

## 3. 调休计算
- 工作日加班：1:1计算调休时间
- 周末加班：1:1计算调休时间
- 法定节假日加班：1:2计算调休时间（加班1天可调休2天）

## 4. 调休使用
- 调休可与年假、事假等合并使用
- 调休优先于年假使用
- 调休到期未使用，自动失效

## 5. 特殊情况
- 出差期间的加班，需提供出差任务完成情况说明，经部门负责人确认后可申请调休
- 项目紧急情况下的加班，需提供项目负责人证明
- 离职员工的未休调休，不予以经济补偿
            """,
            "file_type": "txt",
            "category": "overtime"
        }
    ]
    
    # 创建示例政策文件并添加到数据库
    db = SessionLocal()
    try:
        for policy in example_policies:
            # 创建文件
            file_name = f"{policy['title'].replace(' ', '_')}.txt"
            file_path = os.path.join(settings.POLICY_DIR, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(policy['content'])
            
            # 添加到数据库
            db_policy = Policy(
                title=policy['title'],
                description=f"示例{policy['title']}",
                file_path=file_path,
                file_type=policy['file_type'],
                category=policy['category'],
                is_active=True
            )
            db.add(db_policy)
        
        db.commit()
        print("示例政策创建完成")
    except Exception as e:
        db.rollback()
        print(f"创建示例政策失败: {e}")
    finally:
        db.close()

class MockVectorStore:
    """模拟向量存储类，用于开发测试"""
    
    def as_retriever(self, **kwargs):
        """返回一个模拟检索器"""
        return MockRetriever()
    
    def similarity_search(self, query, k=4):
        """模拟相似度搜索"""
        return query_knowledge_base(query, k)

class MockRetriever:
    """模拟检索器类，用于开发测试"""
    
    def get_relevant_documents(self, query):
        """模拟获取相关文档"""
        return query_knowledge_base(query) 