import discord
import openai
import nest_asyncio
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# Discord BotのトークンとOpenAI APIキーを環境変数から取得
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')
ORG_ID = os.getenv('OPENAI_ORG_ID')  # organization IDを環境変数から取得

# Discord Botのクライアントを作成
client = discord.Client(intents=discord.Intents.all())

# Botが起動したときの処理
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# メッセージが送信されたときの処理
@client.event
async def on_message(message):
    # メッセージがBot自身によるもの、またはスレッド外のメッセージであれば無視
    if message.author == client.user or not isinstance(message.channel, discord.Thread):
        return

    # スレッドの会話履歴を取得
    conversation_history = ""
    async for message_in_thread in message.channel.history(oldest_first=True):
        author = "User" if message_in_thread.author != client.user else "Assistant"
        conversation_history += f"{author}: {message_in_thread.content}\n"

     # 文字数を確認
    char_count = len(conversation_history)
    if char_count > 7900:
        # 文字数が7900を超えている場合、古い会話履歴を削除
        char_to_remove = char_count - 7900  # 保持する文字数を調整
        conversation_history = conversation_history[char_to_remove:]

    # タイピングインジケータを表示する
    typing_task = None
    try:
        # タイピングインジケータを表示する（非同期タスクとして）
        typing_task = client.loop.create_task(message.channel.typing())

        # OpenAI APIを使用して、メッセージに対する応答を生成する
        response = await openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": conversation_history},
            ],
            headers={"OpenAI-Organization": ORG_ID}  # organization IDをヘッダーに追加
        )

        # 応答を送信する
        await message.channel.send(response['choices'][0]['message']['content'])
    finally:
        if typing_task:
            typing_task.cancel()

# Discord Botを起動する
nest_asyncio.apply()
client.run(TOKEN)
