#!/bin/sh

celery -A config worker -l ${CELERY_LOG_LEVEL} -c ${CELERY_NUMBER_WORKERS} &
celery -A config flower --broker=${CELERY_BROKER_URL} --port=5555 &
wait
