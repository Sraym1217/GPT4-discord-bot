import discord
import openai
import nest_asyncio
import os
import tiktoken
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# Discord BotのトークンとOpenAI APIキーを環境変数から取得
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Discord Botのクライアントを作成
client = discord.Client(intents=discord.Intents.all())

# tiktokenエンコーダを初期化
enc = tiktoken.get_encoding("cl100k_base")

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

    # スレッドIDをキーとして会話の履歴を管理
    thread_id = message.channel.id
    conversation_history = os.environ.get(f"CONVERSATION_HISTORY_{thread_id}", "")

    conversation_history += f"User: {message.content}\n"

    # トークン数を確認
    token_count = len(enc.encode(conversation_history))
    if token_count > 7500:
        # トークン数が7500を超えている場合、古い会話履歴を削除
        tokens_to_remove = token_count - 7500 + 1000  # 保持するトークン数を調整
        tokens = enc.encode(conversation_history)
        new_start_index = tokens_to_remove
        # トークンのインデックスを文字のインデックスに変換
        char_index = sum(len(token) for token in tokens[:new_start_index])
        conversation_history = conversation_history[char_index:]

    # OpenAI APIを使用して、メッセージに対する応答を生成する
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": conversation_history},
        ]
    )

    # OpenAIからの応答を会話の履歴に追加し、環境変数を更新
    conversation_history += f"Assistant: {response['choices'][0]['message']['content']}\n"
    os.environ[f"CONVERSATION_HISTORY_{thread_id}"] = conversation_history

    # 応答を送信する
    await message.channel.send(response['choices'][0]['message']['content'])

# Discord Botを起動する
nest_asyncio.apply()
client.run(TOKEN)
