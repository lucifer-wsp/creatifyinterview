FROM python:3.12

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


# 安装 Poetry
RUN pip install poetry==2.2.0

# 设置 Poetry 配置
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# 设置工作目录
WORKDIR /code

# 复制 Poetry 文件
COPY pyproject.toml poetry.lock* ./

# 安装依赖（不使用虚拟环境）
RUN poetry config virtualenvs.create false && \
    poetry install --no-root && \
    rm -rf $POETRY_CACHE_DIR

# 复制项目文件
COPY . .

RUN poetry install

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "creatifyinterview.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
