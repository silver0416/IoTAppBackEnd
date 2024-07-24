#!/bin/sh

# 運行數據庫遷移
python manage.py makemigrations
python manage.py migrate

# 啟動Django服務器
exec python manage.py runserver 0.0.0.0:8701