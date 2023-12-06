FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords

EXPOSE 80

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]