# ChatGPT Line Bot

中文 | [English](README.en.md)

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-Line-Bot)](https://github.com/TheExplainthis/ChatGPT-Line-Bot/releases/)


## 更新
- 2023/03/03 模型換成 chat completion: `gpt-3.5-turbo`


## 介紹
在 Line 中去導入 ChatGPT Bot，只要在輸入框直接輸入文字，即可與 ChatGPT 開始互動，除了 ChatGPT 以外，也直接串上了 DALL·E 2 的模型，輸入 `/imagine + 文字`，就會回傳相對應的圖片，如下圖所示：

![Demo](https://github.com/TheExplainthis/ChatGPT-Line-Bot/blob/main/demo/chatgpt-line-bot.gif)

## 安裝步驟
### Token 取得
1. 取得 OpenAI 給的 API Token：
    1. [OpenAI](https://beta.openai.com/) 平台中註冊/登入帳號
    2. 右上方有一個頭像，點入後選擇 `View API keys`
    3. 點選中間的 `Create new secret key` -> 生成後即為 `OPENAI_API` （稍晚會用到）
    - 注意：每隻 API 有免費額度，也有其限制，詳情請看 [OpenAI Pricing](https://openai.com/api/pricing/)
2. 取得 Line Token：
    1. 登入 [Line Developer](https://developers.line.biz/zh-hant/)
    2. 創建機器人：
        1. 創建 `Provider` -> 按下 `Create`
        2. 創建 `Channel` -> 選擇 `Create a Messaging API channel`
        3. 輸入完必填的基本資料
        4. 輸入完成後，在 `Basic Settings` 下方，有一個 `Channel Secret` -> 按下 `Issue`，生成後即為 `LINE_CHANNEL_SECRET` （稍晚會用到）
        5. 在 `Messaging API` 下方，有一個 `Channel access token` -> 按下 `Issue`，生成後即為 `LINE_CHANNEL_ACCESS_TOKEN` （稍晚會用到）

### 專案設置
1. Fork Github 專案：
    1. 註冊/登入 [GitHub](https://github.com/)
    2. 進入 [ChatGPT-Line-Bot](https://github.com/TheExplainthis/ChatGPT-Line-Bot)
    3. 點選 `Star` 支持開發者
    4. 點選 `Fork` 複製全部的程式碼到自己的倉庫
2. 部署（免費空間）：
    1. 進入 [replit](https://replit.com/)
    2. 點選 `Sign Up` 直接用 `Github` 帳號登入並授權 -> 按下 `Skip` 跳過初始化設定
    3. 進入後中間主頁的部分點選 `Create` -> 跳出框，點選右上角 `Import from Github`
    4. 若尚未加入 Github 倉庫，則點選連結 `Connect GitHub to import your private repos.` -> 勾選 `Only select repositories` -> 選擇 `ChatGPT-Line-Bot`
    5. 回到第四步，此時 `Github URL` 可以選擇 `ChatGPT-Line-Bot` 專案 -> 點擊 `Import from Github`。

### 專案執行
1. 環境變數設定
    1. 接續上一步 `Import` 完成後在 `Replit` 的專案管理頁面左下方 `Tools` 點擊 `Secrets`。
    2. 右方按下 `Got it` 後，即可新增環境變數，需新增：
        1. OpenAI API Token：
            - key: `OPENAI_API`
            - value: `[由上方步驟一取得]`
        2. 欲選擇的模型：
            - key: `OPENAI_MODEL_ENGINE`
            - value: `gpt-3.5-turbo`  
        3. ChatGPT 要讓助理扮演的角色詞（目前官方無釋出更多的使用方法，由玩家自行測試）
            - key: `SYSTEM_MESSAGE`
            - value: `You are a helpful assistant.`
        4. Line Channel Secret:
            - key: `LINE_CHANNEL_SECRET`
            - value: `[由步驟一取得]`
        5. Line Channel Access Token:
            - key: `LINE_CHANNEL_ACCESS_TOKEN`
            - value: `[由步驟一取得]`
2. 開始執行
    1. 點擊上方的 `Run`
    2. 成功後右邊畫面會顯示 `Hello World`，並將畫面中上方的**網址複製**下來
    3. 回到 Line Developer，在 `Messaging API` 下方的 `Webhook URL` 江上方網址貼過來，並加上 `/callback` 例如：`https://ChatGPT-Line-Bot.explainthis.repl.co/callback`
    4. 打開下方的 `Use webhook`
    5. 將下方 `Auto-reply messages` 關閉
    - 注意：若一小時內沒有任何請求，則程式會中斷，因此需要下步驟
3. CronJob 定時發送請求
    1. 註冊/登入 [cron-job.org](https://cron-job.org/en/)
    2. 進入後面板右上方選擇 `CREATE CRONJOB`
    3. `Title` 輸入 `ChatGPT-Line-Bot`，網址輸入上一步驟的網址，例如：`https://ChatGPT-Line-Bot.explainthis.repl.co/`
    4. 下方則每 `5 分鐘` 打一次
    5. 按下 `CREATE`

## 指令
在文字輸入框中直接輸入文字，即可與 ChatGPT 開始對話，而其他指令如下：

| 指令 | 說明 |
| --- | ----- |
| `/imagine` | 在輸入框輸入 `/imagine` + 文字，就會調用 DALL·E 2 模型，即可生成圖像。|

## 相關專案
- [gpt-ai-assistant](https://github.com/memochou1993/gpt-ai-assistant)
- [ChatGPT-Discord-Bot](https://github.com/TheExplainthis/ChatGPT-Discord-Bot)

## 授權
[MIT](LICENSE)