# GPT4-discord-bot
1`pip install -r requirements.txt`でパッケージのインポート。
2`.env`にDiscord token,OpenAI API key,organization API keyを書き込む。
3. `python discoed_GPT_bot.py`を使用してボットを実行。

## 環境変数
- `DISCORD_TOKEN`: Your Discord bot token.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_ORG_ID`:Your organization API key.
## 使い方
通常のメッセージには応答せずスレッド上のメッセージにしか応答しません。各スレッドごとに履歴を取得して会話をします。
