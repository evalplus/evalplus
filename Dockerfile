# base env: py38 ubuntu20.04
FROM python:3.8-slim-buster

# upgrade to latest pip
RUN pip install --upgrade pip

# install evalplus and cache dataset
RUN pip install evalplus

WORKDIR /app

ENTRYPOINT ["python3", "-m", "evalplus.evaluate"]
