# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
ENV FLASK_APP=app.py
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["flask", "run", "--debug","--host=0.0.0.0"]