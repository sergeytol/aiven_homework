FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY requirements.txt /src/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /src/