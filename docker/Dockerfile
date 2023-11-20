FROM python:3.11

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

COPY ./src ./src
COPY ./README.md ./
COPY ./LICENSE.txt ./
COPY ./pyproject.toml ./
RUN pip install .[lint,test]
COPY ./tests ./tests

RUN chmod -R a+x .