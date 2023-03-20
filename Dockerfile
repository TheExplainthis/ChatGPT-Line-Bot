FROM python:3.9-alpine


COPY ./ /ChatGPT-Line-Bot
WORKDIR /ChatGPT-Line-Bot

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]