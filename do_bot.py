from flask import Flask
import threading
import discord_GPT_bot  # あなたのDiscordボットのコードをインポートする

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

def run_bot():
    # あなたのDiscordボットの起動コードをここに配置する
    discord_GPT_bot.run()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=80)  # Renderはポート80を推奨しています
