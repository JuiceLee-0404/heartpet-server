# 使用官方 Python 运行时基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY . /app

# 安装所需的包
RUN pip install --no-cache-dir requirements.txt

# 使端口可用
EXPOSE 5000

# 在容器内运行 app.py
CMD ["python", "server.py"]
