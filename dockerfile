FROM python:3.10-alpine

ENV PYTHONBUFFERED 1
ENV PATH="/py/bin:$PATH"

# 安裝系統依賴
RUN apk add --no-cache bash vim curl tk

# 創建虛擬環境並安裝Python依賴
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN /py/bin/pip install -r /requirements.txt

# 創建非root用戶
RUN adduser --disabled-password --no-create-home app

# 設置工作目錄
WORKDIR /app
COPY ./app /app

# 創建啟動腳本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 切換到非root用戶
USER app

# 使用啟動腳本
CMD ["/entrypoint.sh"]