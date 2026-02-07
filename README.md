# 图书管理系统

## 项目概述
图书管理系统是一个基于Flask框架开发的图书馆管理系统，支持用户管理、图书管理、借阅管理、分类管理等功能。

## 技术架构

### 后端技术
- **Flask**: Python Web框架
- **Flask-SQLAlchemy**: ORM数据库工具
- **Flask-Migrate**: 数据库迁移工具
- **Flask-Login**: 用户认证管理
- **Flask-WTF**: 表单处理和验证
- **SQLite**: 轻量级数据库系统

### 前端技术
- **Jinja2**: 模板引擎
- **HTML5/CSS3**: 页面结构和样式
- **Bootstrap**: 响应式UI框架

## 项目结构

```
BookLibrary-Flask-App/
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── books.html
│   ├── book_detail.html
│   ├── borrow.html
│   ├── return.html
│   ├── my_books.html
│   ├── admin.html
│   ├── add_book.html
│   ├── categories.html
│   ├── add_category.html
│   ├── users.html
│   ├── overdue.html
│   └── search.html
├── app.py
├── config.py
├── models.py
├── forms.py
├── routes.py
├── book.db
└── README.md
```

## 核心功能

### 1. 用户管理
- 用户注册和登录
- 用户信息管理
- 管理员权限管理

### 2. 图书管理
- 图书添加、编辑、删除
- 图书分类管理
- 图书搜索和浏览
- 图书详情查看

### 3. 借阅管理
- 图书借阅
- 图书归还
- 借阅记录查询
- 逾期图书管理

### 4. 统计功能
- 图书总数统计
- 可借图书统计
- 借出图书统计
- 用户总数统计

## 数据库设计

### 主要数据表
- **user**: 用户信息
- **category**: 图书分类
- **book**: 图书信息
- **borrow_record**: 借阅记录

## 快速开始

### 环境要求
- Python 3.6+
- pip

### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/sangjiexun/BookLibrary-Flask-App.git
   cd BookLibrary-Flask-App
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. 运行应用
   ```bash
   python app.py
   ```

## 部署说明

### 生产环境部署
- 使用Gunicorn作为WSGI服务器
- 使用Nginx作为反向代理
- 配置HTTPS
- 启用生产模式

### 环境变量配置
- `SECRET_KEY`: 应用密钥
- `DATABASE_URL`: 数据库连接URL
- `DEBUG`: 调试模式

## 许可证

MIT License

---

# Book Library System

## Project Overview
Book Library System is a Flask-based library management system, supporting user management, book management, borrowing management, category management, and other functions.

## Technical Architecture

### Backend Technologies
- **Flask**: Python Web framework
- **Flask-SQLAlchemy**: ORM database tool
- **Flask-Migrate**: Database migration tool
- **Flask-Login**: User authentication management
- **Flask-WTF**: Form handling and validation
- **SQLite**: Lightweight database system

### Frontend Technologies
- **Jinja2**: Template engine
- **HTML5/CSS3**: Page structure and styling
- **Bootstrap**: Responsive UI framework

## Project Structure

```
BookLibrary-Flask-App/
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── books.html
│   ├── book_detail.html
│   ├── borrow.html
│   ├── return.html
│   ├── my_books.html
│   ├── admin.html
│   ├── add_book.html
│   ├── categories.html
│   ├── add_category.html
│   ├── users.html
│   ├── overdue.html
│   └── search.html
├── app.py
├── config.py
├── models.py
├── forms.py
├── routes.py
├── book.db
└── README.md
```

## Core Features

### 1. User Management
- User registration and login
- User information management
- Admin privilege management

### 2. Book Management
- Book addition, editing, and deletion
- Book category management
- Book search and browsing
- Book detail viewing

### 3. Borrowing Management
- Book borrowing
- Book returning
- Borrowing record查询
- Overdue book management

### 4. Statistics Functions
- Total book count statistics
- Available book count statistics
- Borrowed book count statistics
- Total user count statistics

## Database Design

### Main Data Tables
- **user**: User information
- **category**: Book category
- **book**: Book information
- **borrow_record**: Borrowing record

## Quick Start

### Environment Requirements
- Python 3.6+
- pip

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/sangjiexun/BookLibrary-Flask-App.git
   cd BookLibrary-Flask-App
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize database
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application
   ```bash
   python app.py
   ```

## Deployment Instructions

### Production Environment Deployment
- Use Gunicorn as WSGI server
- Use Nginx as reverse proxy
- Configure HTTPS
- Enable production mode

### Environment Variables Configuration
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection URL
- `DEBUG`: Debug mode

## License

MIT License