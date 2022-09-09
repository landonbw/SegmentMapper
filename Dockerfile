From python:3.10-buster
WORKDIR /usr/src/app
ENV FLASK_APP=webapp
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# RUN apk update && apk add mysql-client 
RUN apt-get install default-libmysqlclient-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]