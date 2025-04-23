FROM python:3.9-slim

# 把檔案複製進去
COPY ./ /ChatGPT-Line-Bot
WORKDIR /ChatGPT-Line-Bot

# 更新 pip 並裝好套件
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 執行程式
CMD ["python", "main.py"]
