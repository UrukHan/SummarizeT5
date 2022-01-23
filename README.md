docker build -t t5 .
docker run --rm --name rut5 -p 8000:8000 t5


curl -X POST -H "Content-Type: application/json" -d "{ \"input_text\": \"Введите текст.\" }" http://172.21.192.1:8000/api/predict



