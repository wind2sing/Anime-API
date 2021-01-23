FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ /code/

EXPOSE 6001

CMD [ "python", "./deploy.py" ]