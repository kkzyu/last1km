# ZJU Last 1km - 浙大校园速递平台

一个基于 Vue 3 + Flask 的现代化校园快递代取平台，致力于解决校园内快递取件"最后一公里"的问题。为浙大学生和教职工提供便捷的快递代取服务。
![ZJULast1Km](https://github.com/user-attachments/assets/27e1c4ea-289e-4884-ba80-b784e49f6717)



## 📋 目录

- [项目概述](#项目概述)
- [核心功能](#核心功能)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [环境要求](#环境要求)
- [部署指南](#部署指南)
- [API文档](#api文档)
- [功能演示](#功能演示)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [更新日志](#更新日志)
- [许可证](#许可证)

## 📖 项目概述

ZJU Last 1km 是一个专为浙江大学校园设计的现代化快递代取平台。采用前后端分离架构，提供完整的快递代取解决方案，包括订单管理、实时通讯、智能路线规划、支付系统等功能。

### 🎯 核心价值
- **解决痛点**：解决学生没时间取快递的问题
- **提高效率**：智能匹配配送员，优化配送路线
- **安全可靠**：完善的认证机制和订单跟踪
- **用户友好**：现代化UI设计，操作简单直观

## 🚀 核心功能

### 👤 用户系统
- ✅ 用户注册与登录（支持学号/手机号）
- ✅ 个人信息管理与编辑
- ✅ 头像上传与实时预览
- ✅ JWT Token 安全认证
- ✅ 多角色权限管理（用户/配送员）
- ✅ 账户余额管理

### 📦 订单系统
- ✅ 快递代取委托发布
- ✅ 智能地址搜索与路线规划
- ✅ 实时订单状态追踪
- ✅ 多状态管理（待接单/进行中/已完成/已取消）
- ✅ 按日期分组的订单展示
- ✅ 订单评价与反馈系统
- ✅ 图片上传与OCR识别
- ✅ 订单详情查看与管理

### 💬 即时通讯
- ✅ 用户与配送员实时聊天
- ✅ 消息状态管理（已读/未读）
- ✅ 聊天记录持久化保存
- ✅ 文字和图片消息支持
- ✅ 配送员信息查看

### 🗺️ 地图服务
- ✅ 高德地图集成
- ✅ 智能地址搜索
- ✅ 路线规划与导航
- ✅ 距离和时间预估
- ✅ 交互式地图显示

### 🤖 AI 服务
- ✅ 百度OCR图片识别
- ✅ 智能客服聊天机器人
- ✅ 订单信息自动提取
- ✅ 常见问题自动回答


## 🛠️ 技术栈

### 前端技术
- **核心框架**：Vue 3.5.13 (Composition API)
- **构建工具**：Vite 6.2.4
- **UI组件库**：Ant Design Vue 4.0
- **状态管理**：Pinia 3.0.2
- **路由管理**：Vue Router 4.5.0
- **HTTP客户端**：Axios 1.9.0
- **图标库**：FontAwesome 6.7.2 + Ant Design Icons
- **地图服务**：高德地图 API
- **开发工具**：Vue DevTools

### 后端技术
- **Web框架**：Python Flask 2.3.2
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **ORM框架**：SQLAlchemy 3.0.5
- **认证系统**：Flask-JWT-Extended 4.5.2
- **跨域处理**：Flask-CORS 4.0.0
- **数据迁移**：Flask-Migrate 4.0.5
- **AI服务**：百度AI API、千帆大模型
- **地图服务**：高德地图API

### 开发与部署
- **版本控制**：Git
- **开发环境**：VS Code
- **API测试**：Postman
- **代码规范**：ESLint + Prettier
- **包管理**：npm (前端) + pip (后端)
- **虚拟环境**：Python venv

## 📁 项目结构
## 📁 项目结构

```
ZJU-Last-1km/
├── 📁 client/                          # 前端项目
│   ├── 📁 public/                      # 静态资源
│   │   ├── 📁 data/                   # 模拟数据
│   │   │   ├── messages.json         # 消息数据
│   │   │   ├── orders.json           # 订单数据
│   │   │   └── riders.json           # 配送员数据
│   │   └── 📁 images/                 # 图片资源
│   ├── 📁 src/                        # 源代码
│   │   ├── 📁 api/                    # API接口
│   │   │   └── api.js                # API统一管理
│   │   ├── 📁 assets/                 # 资源文件
│   │   ├── 📁 components/             # 组件库
│   │   │   ├── 📁 Bottom/            # 底部导航
│   │   │   ├── 📁 Header/            # 页面头部
│   │   │   ├── 📁 Home/              # 首页组件
│   │   │   ├── 📁 Message/           # 消息组件
│   │   │   ├── 📁 Order/             # 订单组件
│   │   │   ├── 📁 Profile/           # 个人中心
│   │   │   ├── 📁 Publish/           # 发布订单
│   │   │   └── 📁 UI/                # 通用UI组件
│   │   ├── 📁 router/                 # 路由配置
│   │   │   └── index.js              # 路由定义
│   │   ├── 📁 stores/                 # 状态管理
│   │   │   ├── chatStore.js          # 聊天状态
│   │   │   ├── orderStore.js         # 订单状态
│   │   │   ├── userStore.js          # 用户状态
│   │   │   └── messages.js           # 消息状态
│   │   ├── 📁 views/                  # 页面视图
│   │   │   ├── 📁 Home/              # 首页模块
│   │   │   ├── 📁 Login/             # 登录模块
│   │   │   ├── 📁 Messages/          # 消息模块
│   │   │   ├── 📁 Order/             # 订单模块
│   │   │   └── 📁 Profile/           # 个人中心
│   │   ├── App.vue                    # 根组件
│   │   └── main.js                    # 应用入口
│   ├── index.html                     # HTML模板
│   ├── package.json                   # 项目依赖
│   └── vite.config.js                 # Vite配置
│
├── 📁 server/                          # 后端项目
│   ├── 📁 models/                     # 数据模型
│   │   ├── __init__.py               # 模型初始化
│   │   ├── user.py                   # 用户模型
│   │   ├── order.py                  # 订单模型
│   │   ├── deliverer.py              # 配送员模型
│   │   ├── address.py                # 地址模型
│   │   └── chat_message.py           # 聊天消息模型
│   ├── 📁 routes/                     # 路由控制器
│   │   ├── __init__.py               # 路由初始化
│   │   ├── auth.py                   # 认证路由
│   │   ├── users.py                  # 用户路由
│   │   ├── orders.py                 # 订单路由
│   │   ├── chat.py                   # 聊天路由
│   │   ├── riders.py                 # 配送员路由
│   │   ├── messages.py               # 消息路由
│   │   ├── map.py                    # 地图路由
│   │   └── faq.py                    # FAQ路由
│   ├── 📁 services/                   # 业务服务
│   │   ├── ai_service.py             # AI服务
│   │   └── map_service.py            # 地图服务
│   ├── 📁 utils/                      # 工具函数
│   │   ├── auth_helpers.py           # 认证助手
│   │   ├── auth.py                   # 认证工具
│   │   └── response.py               # 响应格式化
│   ├── 📁 static/                     # 静态文件
│   │   └── 📁 uploads/               # 上传文件
│   ├── 📁 instance/                   # 实例配置
│   │   └── zjulast1km.db             # SQLite数据库
│   ├── app.py                         # Flask应用入口
│   ├── config.py                      # 配置文件
│   ├── migrate.py                     # 数据库迁移
│   └── requirements.txt               # Python依赖
│
├── 📁 prototype/                       # 原型设计
│   ├── submit.rp                      # 原型文件
│   ├── todolist.md                    # 待办事项
│   └── url.txt                        # 相关链接
│
├── README.md                           # 项目说明
├── user_guide.md                      # 用户指南
└── .gitignore                         # Git忽略文件
```

## ⚡ 快速开始

### 环境要求

确保您的开发环境满足以下要求：

- **Node.js** >= 16.0.0
- **Python** >= 3.12
- **npm** 或 **yarn** 包管理器
- **Git** 版本控制工具

### 1. 克隆项目

```bash
git clone https://gitee.com/zjusom/group4
cd group4
```

### 2. 后端启动

```bash
# 进入后端目录
cd server

# 创建Python虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
# .\.venv\Scripts\activate.bat
# Linux/Mac:
# source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量（复制.env.example到.env并修改）
cp .env.example .env

# 初始化数据库
python app.py

# 启动后端服务
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 3. 前端启动

```bash
# 进入前端目录
cd client

# 安装Node.js依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

### 4. 访问应用

打开浏览器访问 `http://localhost:3000`，即可开始使用应用。

## 🔧 环境配置（项目内已完成✅可忽略）

### 后端环境变量

在 `server/.env` 文件中配置以下环境变量：

```env
# Flask配置
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
DATABASE_URL=sqlite:///zjulast1km.db
FLASK_ENV=development
UPLOAD_FOLDER=uploads

# 百度AI OCR配置
BAIDU_AI_APP_ID=your_app_id
BAIDU_AI_API_KEY=your_api_key
BAIDU_AI_SECRET_KEY=your_secret_key

# 百度千帆大模型API配置
BAIDU_WENXIN_API_KEY=your_wenxin_api_key
BAIDU_WENXIN_SECRET_KEY=your_wenxin_secret_key

# 高德地图API配置
AMAP_KEY=your_amap_key
```

### 前端配置

在 `client/vite.config.js` 中已配置代理：

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true
    }
  }
}
```

## 🚀 部署指南

### 前端部署

#### 1. 构建生产版本

```bash
cd client
npm run build
```

#### 2. 部署到静态服务器

将 `dist/` 目录部署到任何静态文件服务器（如 Nginx、Apache、或 CDN）。

#### 3. GitHub Pages 部署

```bash
# 已配置homepage字段，可直接部署到GitHub Pages
npm run build
# 将dist目录内容推送到gh-pages分支
```

### 后端部署

#### 1. 生产环境配置

```bash
# 安装生产依赖
pip install -r requirements.txt
pip install gunicorn  # Linux/Mac
pip install waitress  # Windows

# 设置生产环境变量
export FLASK_ENV=production
```

#### 2. 使用Gunicorn部署（Linux/Mac）

```bash
# 启动Gunicorn服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或使用配置文件
gunicorn -c gunicorn.conf.py app:app
```

#### 3. 使用Waitress部署（Windows）

```bash
waitress-serve --port=5000 app:app
```

#### 4. 使用Docker部署

```dockerfile
# Dockerfile示例
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📚 API文档

### 认证接口

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "password": "string",
  "phone": "string"
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

### 订单接口

#### 获取订单列表
```http
GET /api/orders
Authorization: Bearer <token>
```

#### 创建订单
```http
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "start_address": "string",
  "end_address": "string",
  "item_description": "string",
  "total_amount": "number"
}
```

#### 获取订单详情
```http
GET /api/orders/{id}
Authorization: Bearer <token>
```

### 消息接口

#### 获取聊天列表
```http
GET /api/messages/chats
Authorization: Bearer <token>
```

#### 获取聊天详情
```http
GET /api/messages/chats/{chatId}
Authorization: Bearer <token>
```

### 地图接口

#### 地址搜索
```http
POST /api/map/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "keyword": "string",
  "city": "string"
}
```

#### 路线规划
```http
POST /api/map/route
Authorization: Bearer <token>
Content-Type: application/json

{
  "origin": {"lat": "number", "lng": "number"},
  "destination": {"lat": "number", "lng": "number"}
}
```

## 🎨 功能演示

### 用户界面截图

<details>
<summary>📱 主要界面展示</summary>

#### 首页
- 现代化卡片设计
- 订单历史展示
- 快速发布入口

#### 发布订单
- 智能地址搜索
- 路线规划预览
- 图片上传识别

#### 消息中心
- 实时聊天界面
- 配送员信息展示
- 消息状态管理

#### 个人中心
- 用户信息管理
- 订单历史查看
- 账户设置
</details>

### 核心功能流程

1. **用户注册/登录** → 2. **发布快递代取委托** → 3. **配送员接单** → 4. **实时沟通** → 5. **完成配送** → 6. **评价反馈**

## ❓ 常见问题

### 安装问题

**Q: npm install 失败怎么办？**
A: 尝试使用淘宝镜像源：
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

**Q: Python依赖安装失败？**
A: 确保Python版本>=3.12，使用虚拟环境：
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 运行问题

**Q: 前端无法连接后端？**
A: 检查：
1. 后端服务是否在5000端口运行
2. 前端代理配置是否正确
3. CORS配置是否正确

**Q: 地图服务无法使用？**
A: 确保在`.env`文件中配置了正确的高德地图API KEY。

### 功能问题

**Q: 图片上传失败？**
A: 检查：
1. 图片大小是否超过16MB
2. 上传目录权限是否正确
3. 百度OCR API配置是否正确

**Q: 聊天消息无法发送？**
A: 确保：
1. 用户已登录
2. WebSocket连接正常
3. 聊天对象存在

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. **创建特性分支**：`git checkout -b feature/your-feature`
3. **提交更改**：`git commit -am '添加新特性'`
4. **推送分支**：`git push origin feature/your-feature`
5. **提交Pull Request**

### 代码规范

- **前端**：遵循Vue.js官方风格指南
- **后端**：遵循PEP 8代码规范
- **Git提交**：使用语义化提交消息

### 开发流程

1. 在Issues中讨论新功能或bug修复
2. 分配任务给合适的开发者
3. 创建功能分支进行开发
4. 编写测试用例
5. 代码审查
6. 合并到主分支

## 🔄 更新日志

### Version 1.2.0 (2025-6-3)
- ✨ 新增AI智能客服功能
- 🗺️ 集成高德地图路线规划
- 🖼️ 添加OCR图片识别功能
- 💬 优化聊天体验和UI设计
- 🐛 修复若干已知问题

### Version 1.1.0 (2025-5-27)
- 📱 优化移动端响应式设计
- 🔍 增强地址搜索功能
- 📊 添加订单统计功能
- 🔧 优化性能和稳定性

### Version 1.0.0 (2025-5-20)
- 🎉 初始版本发布
- ✅ 完成核心功能开发
- 🏗️ 建立项目基础架构
- 📚 编写项目文档

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 👥 团队成员

- **项目负责人**：Group 4 Team
- **前端开发**：Vue.js + Ant Design Vue
- **后端开发**：Python Flask + SQLAlchemy
- **UI/UX设计**：现代化响应式设计

## 📞 联系我们

- **项目仓库**：[GitHub Repository](https://gitee.com/zjusom/group4)
- **问题反馈**：[Issues](https://gitee.com/zjusom/group4/issues)
- **功能建议**：[Discussions](https://gitee.com/zjusom/group4/discussions)

## 🙏 致谢

感谢以下开源项目和服务：

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架
- [Ant Design Vue](https://antdv.com/) - 企业级UI组件库
- [高德地图](https://lbs.amap.com/) - 地图服务支持
- [百度AI](https://ai.baidu.com/) - AI服务支持
- [gemini 2.5pro](https://gemini.google.com/)、[claude 4 sonnet](https://anthropic.com)、[deepseek v3-0324](https://deepseek.com)-提供代码帮助！

---



**⭐ 如果这个项目对您有帮助，请给我们一个Sr！**

**Made with ❤️ by ZJU Last 1km Team**

</div>
1. 项目概述和功能特性
2. 技术栈和项目结构
3. 安装和运行指南
4. 配置和部署说明
5. 测试账号信息
6. 贡献指南和许可证信息
