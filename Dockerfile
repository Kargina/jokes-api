FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install .
EXPOSE 5000
ENTRYPOINT [ "joke-api" ]
