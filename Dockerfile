FROM python:3.8.2-slim
RUN apt-get update -y && apt-get install -y libgtk2.0-dev libsm6 libxext6 libxrender-dev
WORKDIR /code
ADD server.py /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD ["python","/code/server.py"]
