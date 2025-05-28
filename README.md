# ZJU Last 1km - 浙大校园速递平台

一个基于 Vue 3 + Flask 的现代化校园快递代取平台，致力于解决校园内快递取件"最后一公里"的问题。提供用户认证、订单管理、即时通讯和快递代取服务。

## 项目概述

本项目采用前后端分离架构，前端使用 Vue 3 + Vite + Ant Design Vue 构建现代化 UI 界面，后端使用 Python Flask 提供 RESTful API 服务。主要功能包括用户认证、订单管理、即时通讯、支付系统等。


## 核心功能

### 1. 用户系统
- 账号注册与登录
- 个人信息管理
- 头像上传与修改
- JWT Token 认证
- 用户角色权限管理

### 2. 订单系统
- 发布快递代取委托
- 实时订单状态追踪
- 多状态订单管理（进行中/已完成/已取消）
- 按日期分组的订单展示
- 订单评价与反馈
- 图片上传与预览

### 3. 即时通讯
- 用户与骑手实时聊天
- 消息实时提醒
- 聊天记录保存
- 图片消息支持

### 4. 支付系统
- 余额管理
- 订单支付
- 交易记录
- 安全支付保障

## 技术栈

### 前端
- Vue 3.5.13 + Vite 6.2.4
- Ant Design Vue 4.0
- Pinia 状态管理
- Vue Router 4.5.0
- Axios HTTP 客户端
- WebSocket 即时通讯

### 后端
- Python Flask框架
- SQLite 数据库
- JWT 认证
- RESTful API
- WebSocket服务

### 开发工具
- VS Code
- Git 版本控制
- Chrome DevTools
- Postman API测试

## 环境要求
- Node.js >= 16.0.0
- Python >= 3.12
- npm 或 yarn 包管理器

## 本地开发
### 前端启动
```bash
# 进入前端项目目录
cd client

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 后端启动
```bash
# 进入后端项目目录
cd server

# 激活虚拟环境（Windows PowerShell）
.\.venv\Scripts\Activate.ps1
# 或在Linux/Mac下
# source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

注意：首次运行需要先创建并激活Python虚拟环境：
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（选择对应操作系统的命令）
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
# .\.venv\Scripts\activate.bat
# Linux/Mac:
# source .venv/bin/activate
```

## 项目结构说明
```bash
project/
├── client/                 # 前端项目目录
│   ├── src/
│   │   ├── api/           # API接口定义
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 组件目录
│   │   │   ├── Bottom/    # 底部导航组件
│   │   │   ├── Header/    # 页面头部组件
│   │   │   ├── Home/      # 首页相关组件
│   │   │   ├── Message/   # 消息相关组件
│   │   │   ├── Order/     # 订单相关组件
│   │   │   ├── Profile/   # 个人中心组件
│   │   │   ├── Publish/   # 发布订单组件
│   │   │   └── UI/        # 通用UI组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # Pinia状态管理
│   │   ├── views/         # 页面视图
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 应用入口
│   └── public/            # 公共资源目录
│       ├── data/          # 静态数据
│       └── images/        # 图片资源
│
└── server/                # 后端项目目录
    ├── models/            # 数据模型
    ├── routes/            # 路由控制器
    ├── static/           # 静态文件
    ├── utils/            # 工具函数
    ├── app.py            # 应用入口
    ├── config.py         # 配置文件
    └── requirements.txt  # Python依赖
```

## 部署说明

### 前端部署
```bash
# 构建生产版本
cd client
npm run build

# 部署到服务器
# 将dist目录的内容部署到Web服务器的相应目录
```

### 后端部署
```bash
# 安装生产环境依赖
cd server
pip install -r requirements.txt

# 配置数据库
python app.py init-db

# 使用gunicorn启动服务（Linux环境）
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Windows环境下可使用waitress
waitress-serve --port=5000 app:app
```

## 详细功能说明

### 用户系统
- JWT Token基础的身份认证
- 用户信息的CRUD操作
- 文件上传（头像等）
- 用户角色管理（普通用户/骑手）

### 订单系统
- 智能订单分配
- 实时状态更新
- 多维度订单查询
- 评价与反馈机制

### 即时通讯
- WebSocket实时消息
- 离线消息存储
- 消息通知机制
- 图片消息支持

## 安全说明

### 用户认证
- 基于JWT的Token认证机制
- 密码加密存储
- 会话管理与超时控制

### 数据安全
- 文件上传验证
- SQL注入防护
- XSS防护
- CSRF防护

## 测试账号
- 普通用户: `group4` / `123456`


## 贡献指南

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am '添加新特性'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交Pull Request

## 开源许可

本项目采用 [MIT License](LICENSE) 开源协议。

## 更新日志

### Version 1.0.0 (2024-05-27)
- 初始版本发布
- 实现基础功能
- 完成核心特性
1. 项目概述和功能特性
2. 技术栈和项目结构
3. 安装和运行指南
4. 配置和部署说明
5. 测试账号信息
6. 贡献指南和许可证信息