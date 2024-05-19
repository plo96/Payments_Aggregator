FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY sample_files sample_files

COPY src src

COPY main.py main.py

CMD ["python3", "main.py"]