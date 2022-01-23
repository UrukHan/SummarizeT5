FROM python:3.9

WORKDIR /api

COPY requirements.txt .

RUN pip install gdown && \
  mkdir -p /api && \
  mkdir -p /api/model && \
  gdown "https://drive.google.com/u/0/uc?export=download&confirm=sGAD&id=1mBbh-fgA6To7FuSgt8rBux3zBApYpYeu" -O /api/model/model.zip && \ 
  unzip /api/model/model.zip -d /api/model/ && \
  rm /api/model/model.zip && \
  pip install -r requirements.txt && \
  pip install uvloop

COPY . /api

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--app-dir=./", "--reload", "--workers=1", "--host=0.0.0.0", "--port", "8000", "--use-colors", "--loop=uvloop"]


