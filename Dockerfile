FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ /code/

EXPOSE 6001

CMD [ "python", "./demo.py" ]