
FROM python:3.8-slim-buster
WORKDIR /home/CST_Demo_Project
COPY . .
EXPOSE 5000
RUN pip install -r requirements.txt
CMD flask --app flaskr run