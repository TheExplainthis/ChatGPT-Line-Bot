FROM python:3.12

ENV PYTHONUNBUFFERED True

COPY ./ /ChatGPT-Line-Bot
WORKDIR /ChatGPT-Line-Bot
RUN find . -name "*.ipynb" -exec rm {} +
RUN apt-get install libpq-dev
RUN pip3 install -r requirements.txt

# CMD ["python3", "main.py"]
CMD nohup gunicorn -w 4 main:app --access-logfile /var/log/gunicorn_access.txt --error-logfile /var/log/gunicorn_error.txt -b :8080 --timeout 120