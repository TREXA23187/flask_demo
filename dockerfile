# 使用官方的Python镜像作为基础镜像
FROM python:3.8-slim-buster

# 在容器内的/app目录下工作
WORKDIR /app

# 将当前目录的内容复制到容器的/app目录下
COPY . /app

# 安装必要的库和软件
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV FLASK_APP=app.py

# 在容器内部运行flask命令
CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"]
