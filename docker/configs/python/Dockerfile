FROM python:3.12-alpine
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apk update

COPY ./src ./src
COPY ./commands ./commands
COPY ./requirements.txt ./requirements.txt
COPY ./static ./static
COPY ./.black.toml ./.black.toml
COPY ./.flake8 ./.flake8

RUN python -m pip install --upgrade pip & pip install -r ./requirements.txt
EXPOSE 8000

CMD ["sh"]