# 校园速递平台

![校园速递平台截图](preview.png)

一个基于Vue 3的校园快递代取平台，提供用户认证、订单管理和快递代取服务。

### 1. 首页轮播组件
- 支持默认图片展
- 图片加载失败处
- 自定义错误提示文本
- 响应式设计

### 2. 订单历史组件
- 按日期分组的订单展示
- 订单状态分类(进行中/已取消/已完成)
- 订单操作功能：
  - 发布新订单
  - 取消订单
  - 评价已完成订单
  - 恢复已取消订单
- 订单图片展示与错误处理
- 响应式设计适配移动端

## 技术特点
1. 使用Vue 3 Composition API
2. 组件化开发
3. 响应式布局
4. 图片懒加载与错误处理
5. 状态驱动的UI渲染

## 运行说明
1. 确保已安装Node.js (建议16.x或更高版本)
2. 安装依赖：
   ```bash
   npm install or yarn install
   ```
3. 启动开发服务器：
   ```bash
   npm run dev or yarn dev
   ```

## 项目结构
```bash
src/
├── assets/            # 静态资源
├── components/        # 公共组件
│   ├── BottomNav.vue  # 底部导航
│   ├── TopHead.vue    # 顶部导航
│   └── ...
├── views/             # 页面视图
│   ├── Login/         # 登录相关
│   │   └── LoginView.vue
│   ├── Order/         # 订单相关
│   └── ...
├── router/            # 路由配置
├── stores/            # 状态管理
├── App.vue            # 根组件
└── main.js            # 应用入口
```

## 生产构建
```bash
npm run build or yarn build
````
## 功能说明
1. 用户认证
登录功能：用户名/密码验证
登录状态持久化
路由守卫保护
2. 订单管理
订单创建、查看、取消
订单状态跟踪
历史记录查询
3. 界面组件
响应式轮播图
统一的头部/底部导航
表单验证与错误处理

## 部署说明
1. 构建生产版本
2. 将 dist/ 目录内容部署到Web服务器
3. 配置服务器重定向规则（单页应用需要）

## 测试账号
* 管理员账号: admin / password
* 普通用户: user123 / password123

## 贡献指南
1. Fork项目仓库
2. 创建特性分支 (git checkout -b feature/your-feature)
3. 提交更改 (git commit -am 'Add some feature')
4. 推送到分支 (git push origin feature/your-feature)
5. 创建Pull Request

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 文件内容概述

这个README文件包含以下内容：
1. 项目概述和功能特性
2. 技术栈和项目结构
3. 安装和运行指南
4. 配置和部署说明
5. 测试账号信息
6. 贡献指南和许可证信息