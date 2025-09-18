# Creatify Interview

Django 5.2 + Python 3.12 + MySQL 8.0 + JWT 认证的 Web 应用

## 功能

- 用户注册 (`/signup/`)
- 用户登录 (`/signin/`)
- 获取用户信息 (`/me/`)

## 快速开始

### 使用 Docker

```bash
# 构建并启动服务
docker-compose up --build

# 运行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser
```

### 本地环境

```bash
pip install poetry==2.2.0

# 安装依赖
poetry install

# 运行迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

## API 测试

### 用户注册
```bash
curl --location 'http://127.0.0.1:8000/signup/' \
--data-raw '{
    "email": "test@test.com",
    "password": "123"
}'
```

### 用户登录
```bash
curl --location 'http://127.0.0.1:8000/signin/' \
--data-raw '{
    "email": "test@test.com",
    "password": "123"
}'
```

### 获取用户信息
```bash
curl --location 'http://127.0.0.1:8000/me/' \
--header 'Authorization: Bearer <access_token_from_signin>'
```

## 环境变量

创建 `.env` 文件：

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=creatifyinterview
DB_USER=root
DB_PASSWORD=mysql
DB_HOST=localhost
DB_PORT=3306
```

