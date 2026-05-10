# News App Backend

新闻资讯应用后端服务，基于 FastAPI + SQLAlchemy 构建。

## 技术栈

- **框架**: FastAPI
- **ORM**: SQLAlchemy (异步)
- **数据库**: MySQL
- **缓存**: Redis
- **认证**: Token (UUID)
- **包管理**: uv

## 快速启动

### 1. 环境准备

```bash
# 安装依赖
uv sync

# 创建 .env 文件，配置数据库和 Redis
cp .env.example .env
```

`.env` 配置示例：

```
ASYNC_DATABASE_URL=mysql+aiomysql://root:root@localhost:3307/news_app?charset=utf8
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 2. 初始化数据库

执行 `database.sql` 脚本创建表结构和初始数据。

### 3. 启动服务

```bash
uv run uvicorn main:app --reload
```

服务运行在 `http://127.0.0.1:8000`。

## 项目结构

```
.
├── main.py              # 应用入口
├── config/              # 配置（数据库、缓存、设置）
├── models/              # SQLAlchemy 模型
├── schemas/             # Pydantic 请求/响应模型
├── crud/                # 数据访问层
├── routers/             # API 路由
├── utils/               # 工具函数（安全、异常、响应）
├── frontend/            # Vue3 前端
└── database.sql         # 数据库建表脚本
```

## API 接口

### 用户认证 (`/api/user`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/register` | 用户注册 | 否 |
| POST | `/login` | 用户登录 | 否 |
| GET | `/info` | 获取当前用户信息 | 是 |

### 新闻 (`/api/news`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/categories` | 获取新闻分类 | 否 |
| GET | `/list` | 新闻列表（分页+分类） | 否 |
| GET | `/detail` | 新闻详情 | 否 |

### 收藏 (`/api/favorite`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/check` | 检查收藏状态 | 是 |
| POST | `/add` | 添加收藏 | 是 |
| DELETE | `/remove` | 取消收藏 | 是 |
| GET | `/list` | 收藏列表（分页） | 是 |
| DELETE | `/clear` | 清空收藏 | 是 |

### 浏览历史 (`/api/history`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/add` | 添加浏览记录 | 是 |
| GET | `/list` | 历史列表 | 是 |
| DELETE | `/delete/{id}` | 删除单条记录 | 是 |
| DELETE | `/clear` | 清空历史 | 是 |

## 认证说明

登录后返回 Token，后续请求需在 Header 中携带：

```
Authorization: Bearer <token>
```
