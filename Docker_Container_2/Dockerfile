FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/

#  erforderlichen Systempakete
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libmariadb-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["python", "analysis_script2.py"]
