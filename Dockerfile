FROM python:3.7
 
MAINTAINER "cavediary@newlifedef.com"

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

RUN mkdir /DjangoWeb
RUN mkdir /DjangoWeb/db

WORKDIR /DjangoWeb

ADD . /DjangoWeb

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

EXPOSE 80 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]