FROM python:3.7.0-alpine

RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY bot.py .

# RUN python -m nltk.downloader "averaged_perceptron_tagger"; python
# RUN python -m nltk.downloader "punkt"; python
# RUN python -m nltk.downloader "stopwords"; python
# RUN python -m nltk.downloader "wordnet"; python
# RUN python -m spacy download en; python

EXPOSE 5000

CMD ["python3","bot.py"]
