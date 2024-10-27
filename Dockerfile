FROM python:3.12-alpine

RUN apk update

WORKDIR /srv/src/app
COPY ./src ./src
COPY ./static ./static
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r ./requirements.txt
EXPOSE 80

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:80"]