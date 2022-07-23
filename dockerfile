FROM python:3.10-alpine

ENV PYTHONBUFFERED 1
#複製 requirements.txt進入docker 內部
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#新增資料夾
RUN mkdir /app
#將外部的app資料夾複製進入docker內部
COPY ./app /app
#設定當前工作環境路徑為 /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app

ENV PATH = "/py/bin:$PATH"

USER app
