# Better use newer Python as generated code can use new features
FROM python:3.10-slim

# install git
RUN apt-get update && apt-get install -y git

# upgrade to latest pip
RUN pip install --upgrade pip

COPY . /evalplus

RUN cd /evalplus && pip install .

# Pre-install the dataset
RUN python3 -c "from evalplus.data import get_human_eval_plus, get_mbpp_plus; get_human_eval_plus(); get_mbpp_plus()"

WORKDIR /app

ENTRYPOINT ["python3", "-m", "evalplus.evaluate"]
