FROM python:3.12

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY mess_user .

EXPOSE 80

CMD ["uvicorn", "app.main::app", "--host", "0.0.0.0", "--port", "80"]
