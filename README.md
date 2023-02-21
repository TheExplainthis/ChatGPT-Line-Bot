# ChatGPT Discord Bot

中文 | [English](README.en.md)

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-Discord-Bot)](https://github.com/TheExplainthis/ChatGPT-Discord-Bot/releases/)


ChatGPT 串接到 Discord 上面，使得團隊在協作、溝通、效率上都能夠快速的提升，根據下面的安裝步驟，你也能在自己的 Discord 當中去導入 ChatGPT。


## 介紹
在 Discord 裡的每個頻道中導入 ChatGPT Bot，只要在輸入框輸入 `/chat` 就會 有一個 `/chat message` 的關鍵字自動帶入，直接輸入文字即可與 ChatGPT 互動，如下圖所示：
![Demo](https://github.com/TheExplainthis/ChatGPT-Discord-Bot/blob/main/demo/chatgpt-discord-bot.gif)


## 安裝步驟
### Token 取得
- 取得 OpenAI 給的 API Token：
    1. [OpenAI](https://beta.openai.com/) 平台中註冊/登入帳號
    2. 右上方有一個頭像，點入後選擇 `View API keys`
    3. 點選中間的 `Create new secret key`
    - 注意：每隻 API 有免費額度，也有其限制，詳情請看 [OpenAI Pricing](https://openai.com/api/pricing/)
- 取得 Discord Token：
    1. 登入 [Discord Developer](https://discord.com/developers/applications)
    2. 創建機器人：
        1. 進入左方 `Applications`
        2. 點擊右上方 `New Application` 並輸入 Bot 的名稱 > 確認後進入新頁面。
        3. 點擊左方 `Bot`
        4. 點擊右方 `Add Bot`
        5. 下方 `MESSAGE CONTENT INTENT` 需打開 
        6. 按下 `Save Change`
        7. Token 在上方選擇 `View Token` 或已申請過則會是 `Reset Token` 的按鈕。
    3. 設定 OAuth2
        1. 點擊左欄 `OAuth2`
        2. 點擊左欄 `URL Generator`
        3. 右欄 `SCOPES` 選擇 `bot`、右欄下方 `BOT PERMISSIONS` 選擇 `Administrator`
        4. 複製最下方網址到瀏覽器中
        5. 選擇欲加入的伺服器
        6. 按下 `繼續` > `授權`

### 專案設置
1. Fork Github 專案：
    1. 註冊/登入 [GitHub](https://github.com/)
    2. 進入 [ChatGPT-Discord-Bot](https://github.com/TheExplainthis/ChatGPT-Discord-Bot)
    3. 點選 `Star` 支持開發者
    4. 點選 `Fork` 複製全部的程式碼到自己的倉庫
2. 部署（免費空間）：
    1. 進入 [replit](https://replit.com/)
    2. 點選 `Sign Up` 直接用 `Github` 帳號登入並授權 -> 按下 `Skip` 跳過初始化設定
    3. 進入後中間主頁的部分點選 `Create` -> 跳出框，點選右上角 `Import from Github`
    4. 若尚未加入 Github 倉庫，則點選連結 `Connect GitHub to import your private repos.` -> 勾選 `Only select repositories` -> 選擇 `ChatGPT-Discord-Bot`
    5. 回到第四步，此時 `Github URL` 可以選擇 `ChatGPT-Discord-Bot` 專案 -> 點擊 `Import from Github`。

### 專案執行
1. 環境變數設定
    1. 接續上一步 `Import` 完成後在 `Replit` 的專案管理頁面左下方 `Tools` 點擊 `Secrets`。
    2. 右方按下 `Got it` 後，即可新增環境變數，需新增：
        1. OpenAI API Token：
            - key: `OPENAI_API`
            - value: `[由上方步驟一取得] sk-FoXXXX`
        2. 欲選擇的模型：
            - key: `OPENAI_MODEL_ENGINE`
            - value: `text-davinci-003`  
        3. ChatGPT 回傳的文字限制
            - key: `OPENAI_MAX_TOKENS`
            - value: `128`
        4. Discord Token:
            - key: `DISCORD_TOKEN`
            - value: `[由上方步驟一取得] MTA3NXXX`
2. 開始執行
    1. 點擊上方的 `Run`
    2. 成功後右邊畫面會顯示 `Hello. I am alive!`，並將畫面中上方的**網址複製**下來，下一步驟會用到
    - 注意：若一小時內沒有任何請求，則程式會中斷，因此需要下步驟
3. CronJob 定時發送請求
    1. 註冊/登入 [cron-job.org](https://cron-job.org/en/)
    2. 進入後面板右上方選擇 `CREATE CRONJOB`
    3. `Title` 輸入 `ChatGPT-Discord-Bot`，網址輸入上一步驟的網址
    4. 下方則每 `5 分鐘` 打一次
    5. 按下 `CREATE`


## 指令
| 指令 | 別名 | 說明 |
| --- | ---- |----- |
| `文字生成` | `/chat` | 在輸入框直接輸入 `/chat` 會後綴 `message` 直接輸入文字，即可調用 ChatGPT 模型。|
| `刪除紀錄` | `/reset` | ChatGPT 會記住前十次的問答紀錄，調用此指令則會清除。|
|`圖像生成` | `/imagine` | 在輸入框輸入 `/imagine` 會後綴 `prompt` 直接輸入文字，會調用 DALL·E 2 模型，即可生成圖像。|


## 相關專案
- [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)

## 授權
[MIT](LICENSE)