import discord
import openai
from openai import OpenAI
import nest_asyncio
import asyncio
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import logging
import datetime

# 環境変数をロード
load_dotenv()

# Discord BotのトークンとOpenAI APIキーを環境変数から取得
TOKEN = os.getenv('DISCORD_TOKEN')
client_open = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
ORG_ID = os.getenv('OPENAI_ORG_ID')

# Discord Botのクライアントを作成する
client = discord.Client(intents=discord.Intents.all())

async def keep_typing(channel):
    while True:
        await channel.typing()
        await asyncio.sleep(4)

# Botが起動したときの処理
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# メッセージが送信されたときの処理
@client.event
async def on_message(message):
    timestamp = datetime.datetime.now().isoformat()
    # メッセージがBot自身によるもの、またはスレッド外のメッセージであれば無視
    if message.author == client.user or not isinstance(message.channel, discord.Thread):
        return

    typing_task = asyncio.create_task(keep_typing(message.channel))

    try:
        # スレッドの会話履歴を取得（最新の20件のみ）
        conversation_history = ""
        async for message_in_thread in message.channel.history(limit=20, oldest_first=False):
            author = "User" if message_in_thread.author != client.user else "Assistant"
            conversation_history = f"{author}: {message_in_thread.content}\n" + conversation_history

        # OpenAI APIを使用して、メッセージに対する応答を生成する
        response = await client.loop.run_in_executor(
            None,
            lambda: client_open.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{conversation_history} \n Assistant:"},
                ],
            )
        )
        # 応答を送信する
        await message.channel.send(response.choices[0].message.content)

    except discord.errors.HTTPException as e:
        if e.status == 429:
            # レートリミット情報の取得
            rate_limit_scope = e.response.headers.get('X-RateLimit-Scope', 'unknown')
            rate_limit_remaining = e.response.headers.get('X-RateLimit-Remaining')
            rate_limit_reset_after = e.response.headers.get('X-RateLimit-Reset-After')
            print(f"Rate limit scope: {rate_limit_scope}")
            print(f"Remaining: {rate_limit_remaining}, Reset after: {rate_limit_reset_after} seconds")
    finally:
        typing_task.cancel()

# Discord Botを起動する
keep_alive()
client.run(TOKEN)
