# GPT4-discord-bot
1`pip install -r requirements.txt`。
2`.env`にDiscord and OpenAI APIを書き込みます。
3. `python bot.py`を使用してボットを実行します。

## 環境変数
- `DISCORD_TOKEN`: Your Discord bot token.
- `OPENAI_API_KEY`: Your OpenAI API key.
## 使い方
招待したチャンネルのスレッド上のメッセージにしか応答しません。各スレッドごとに履歴を取得して会話を続けます。
