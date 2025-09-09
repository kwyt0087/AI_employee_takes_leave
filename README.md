# AI请假系统

基于Vue 3 + Vant UI + FastAPI + RAG技术的智能请假推荐系统

## 项目介绍

AI请假系统是一个基于RAG技术的智能请假推荐系统，支持以下功能：

- 连接公司原有数据库进行SQL查询
- 使用RAG技术构建知识库，支持导入新的规章制度
- 集成线上AI模型（支持OpenAI、Azure、阿里云通义千问等）
- 员工可在聊天框中提出请假需求，系统会根据公司政策和员工情况推荐多个请假方案
- 员工可以选择推荐方案并提交请假申请

## 技术栈

### 前端

- Vue 3
- Vant UI
- Vite
- Pinia
- Vue Router
- Axios

### 后端

- FastAPI
- SQLAlchemy
- Pydantic
- LangChain
- OpenAI/Azure/阿里云通义千问

## 项目结构

```
askLeave/
  - backend/            # 后端代码
    - app/              # 应用代码
      - api/            # API接口
        - routes.py     # 路由定义
      - config.py       # 配置文件
      - database.py     # 数据库模型
      - rag/            # RAG相关代码
        - knowledge_base.py  # 知识库
        - leave_recommender.py  # 请假推荐器
    - main.py           # 入口文件
    - requirements.txt  # 依赖文件
  - frontend/           # 前端代码
    - src/              # 源代码
      - api/            # API接口
      - assets/         # 静态资源
      - components/     # 组件
      - config/         # 配置
      - router/         # 路由
      - stores/         # 状态管理
      - utils/          # 工具函数
      - views/          # 页面
    - index.html        # HTML模板
    - package.json      # 依赖配置
    - vite.config.js    # Vite配置
```

## 安装与运行

### 后端

1. 进入后端目录
   ```bash
   cd askLeave/backend
   ```

2. 使用环境文件创建conda环境（推荐）
   ```bash
   conda env create -f environment.yml
   ```

   或者手动创建conda环境：
   ```bash
   conda create -n askleave python=3.10
   ```

3. 激活conda环境
   ```bash
   # Windows/Linux/Mac
   conda activate askleave
   ```

4. 如果使用手动创建的环境，需要安装依赖：
   ```bash
   conda install --file requirements.txt
   ```
   
   或者如果某些包在conda中不可用，可以使用pip在conda环境中安装：
   ```bash
   pip install -r requirements.txt
   ```

5. 运行后端服务
   ```bash
   # 确保激活了conda环境
   conda activate askleave
   
   # 运行服务
   uvicorn main:app --reload
   ```

### 前端

1. 进入前端目录
   ```bash
   cd askLeave/frontend
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 运行开发服务器
   ```bash
   npm run dev
   ```

4. 构建生产版本
   ```bash
   npm run build
   ```

## 功能模块

1. 用户认证
   - 登录/注销
   - 用户信息管理

2. 聊天助手
   - 基于RAG的智能问答
   - 聊天历史记录

3. 请假申请
   - 填写请假信息
   - 获取AI推荐方案
   - 提交请假申请

4. 请假管理
   - 查看请假记录
   - 取消请假申请

5. 政策管理
   - 查看公司政策
   - 上传新政策（管理员）

## 环境变量

### 后端

在`.env`文件中配置以下环境变量：

```
# 数据库配置
DATABASE_URL=sqlite:///./knowledge_base.db

# OpenAI配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1

# Azure OpenAI配置
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_BASE=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# 阿里云通义千问配置
DASHSCOPE_API_KEY=your_dashscope_api_key
```

### 前端

在`.env`文件中配置以下环境变量：

```
# API基础URL
VITE_API_BASE_URL=http://localhost:8000

# 应用名称
VITE_APP_NAME=AI请假系统

# 应用版本
VITE_APP_VERSION=1.0.0
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT 