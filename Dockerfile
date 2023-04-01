FROM python:3.10-alpine3.13
WORKDIR /django

ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
COPY . .
COPY .env .env
COPY ./scripts /scripts

EXPOSE 8000
EXPOSE 5432


RUN python -m venv /py &&\
    /py/bin/pip install --upgrade pip &&\
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r requirements.txt &&\
    apk del .tmp-deps&&\
    adduser --disabled-password --no-create-home user &&\
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \ 
    chown -R user:user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER user

CMD ["run.sh"]
