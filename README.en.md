# ChatGPT Line Bot

[中文](README.md) | English

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-Line-Bot)](https://github.com/TheExplainthis/ChatGPT-Line-Bot/releases/)


## Update
- 2023/03/03 Model change to chat completion: `gpt-3.5-turbo`


## Introduction
Import the ChatGPT bot to Line and start interacting with it by simply typing text in the input box. In addition to ChatGPT, the model for DALL·E 2 is also integrated. Enter `/imagine + text` to return the corresponding image, as shown in the figure below:

![Demo](https://github.com/TheExplainthis/ChatGPT-Line-Bot/blob/main/demo/chatgpt-line-bot.gif)

## Installation Steps
### Token Retrieval
1. Retrieve the OpenAI API Token:
    1. Register/login to your [OpenAI](https://beta.openai.com/) account.
    2. Click on the avatar on the top right corner and select `View API keys`.
    3. Click on `Create new secret key` in the middle, and the generated token will be `OPENAI_API` (to be used later).
    - Note: Each API has a free quota and restrictions. For details, please refer to [OpenAI Pricing](https://openai.com/api/pricing/).
2. Retrieve the Line Token:
    1. Login to [Line Developer](https://developers.line.biz/zh-hant/).
    2. Create a bot:
        1. Create a `Provider` -> click `Create`.
        2. Create a `Channel` -> select `Create a Messaging API channel`.
        3. Enter the required basic information.
        4. After completion, there is a `Channel Secret` under `Basic Settings` -> click `Issue`, and the generated token will be `LINE_CHANNEL_SECRET` (to be used later).
        5. Under `Messaging API`, there is a `Channel access token` -> click `Issue`, and the generated token will be `LINE_CHANNEL_ACCESS_TOKEN` (to be used later).

### Project Setup
1. Fork the Github project:
    1. Register/login to [GitHub](https://github.com/).
    2. Go to [ChatGPT-Line-Bot](https://github.com/TheExplainthis/ChatGPT-Line-Bot).
    3. Click `Star` to support the developer.
    4. Click `Fork` to copy all the code to your own repository.
2. Deploy (free space):
    1. Go to [replit](https://replit.com/).
    2. Click `Sign Up` and log in with your `Github` account and authorize it -> click `Skip` to skip the initialization settings.
    3. On the main page in the middle, click `Create` -> a pop-up window will appear, click `Import from Github` on the upper right corner.
    4. If you have not added the Github repository, click the link `Connect GitHub to import your private repos.` -> check `Only select repositories` -> select `ChatGPT-Line-Bot`.
    5. Go back to step 4. At this point, the `Github URL` can select the `ChatGPT-Line-Bot` project -> click `Import from Github`.

### Project Execution
1. Environment variables setting:
    1. After completing the previous step of `Import`, click on `Tools` at the bottom left of the project management page in `Replit`, then click on `Secrets`.
    2. Click on `Got it` on the right side to add environment variables, which includes:
        1. OpenAI API Token:
            - key: `OPENAI_API`
            - value: `[obtained from step one]`
        2. Desired model:
            - key: `OPENAI_MODEL_ENGINE`
            - value: `gpt-3.5-turbo`
        3. ChatGPT wants the assistant to play the role of a keyword (currently, no further usage instructions have been officially released, and players can test it themselves).
            - key: `SYSTEM_MESSAGE`
            - value: `You are a helpful assistant.`
        4. Line Channel Secret:
            - key: `LINE_CHANNEL_SECRET`
            - value: `[obtained from step one]`
        5. Line Channel Access Token:
            - key: `LINE_CHANNEL_ACCESS_TOKEN`
            - value: `[obtained from step one]`
2. Start running:
    1. Click on `Run` on the top.
    2. After successful, the right-side screen will display `Hello World`, and the **URL** on the top of the screen should be copied down.
    3. Go back to Line Developer, paste the **URL** above `Webhook URL` under `Messaging API`, and add `/callback` to the end, for example: `https://ChatGPT-Line-Bot.explainthis.repl.co/callback`
    4. Turn on `Use webhook` below.
    5. Turn off `Auto-reply messages` below.
    - Note: if there is no request within an hour, the program will be interrupted, so the following steps are needed.
3. CronJob scheduled request sending:
    1. Register/Login to [cron-job.org](https://cron-job.org/en/)
    2. In the upper right corner of the panel, select `CREATE CRONJOB`
    3. Enter `ChatGPT-Line-Bot` in the Title field, and enter the URL from the previous step, for example: `https://ChatGPT-Line-Bot.explainthis.repl.co/`
    4. Send a request every `5 minutes` below
    5. Click on `CREATE`

## Commands
To start a conversation with ChatGPT, simply type your message in the text input box. Other available commands include:

| Command | Description |
| ------- | ----------- |
| `/imagine` |  Type `/imagine` followed by text in the input box to call the DALL·E 2 model and generate an image. |

## Related Projects
- [gpt-ai-assistant](https://github.com/memochou1993/gpt-ai-assistant)
- [ChatGPT-Discord-Bot](https://github.com/TheExplainthis/ChatGPT-Discord-Bot)

## License
[MIT](LICENSE)