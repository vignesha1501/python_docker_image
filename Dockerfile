FROM ubuntu:latest

RUN apt update 
RUN apt install python3 -y

WORKDIR /usr/app/src

COPY print.py ./

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
  
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader stopwords
COPY . .

COPY Sample.pdf ./

CMD [ "python3", "./print.py" ]


