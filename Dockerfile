FROM python:3
ADD app.py /
ADD src src
ADD templates templates

COPY requirements.txt .
RUN pip install -r requirements.txt  

CMD [ "python3", "app.py" ]