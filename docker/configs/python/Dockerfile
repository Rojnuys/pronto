FROM python:3.12-alpine
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apk update

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r ./requirements.txt
EXPOSE 8000

CMD ["sh"]