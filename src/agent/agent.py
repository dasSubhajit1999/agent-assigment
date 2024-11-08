import asyncio
import random
import datetime
from dotenv import load_dotenv
import os
from blockchain import get_balance, transfer_token

load_dotenv()



SOURCE_ADDRESS = os.getenv("SOURCE_ADDRESS")
TARGET_ADDRESS = os.getenv("TARGET_ADDRESS")


class Agent:
    def __init__(self,name):
        self.name = name
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe","human"]

    async def generate_random_messages(self):
        while True:
            message = f"{random.choice(self.words)} {random.choice(self.words)}"
            await self.outbox.put(message)
            print(f"{datetime.datetime.now().time()} ----> {self.name} Sent message: {message}")
            await asyncio.sleep(2)


    async def check_erc20_balance(self):
        while True:
            balance = await get_balance(SOURCE_ADDRESS)
            print(f"{datetime.datetime.now().time()} ----> {SOURCE_ADDRESS} ERC-20 Balance: {balance} tokens")
            await asyncio.sleep(10)
             


    async def __transferToken(self):
        await transfer_token(SOURCE_ADDRESS,TARGET_ADDRESS)



    async def handle_messages(self):
        while True:
            message = await self.inbox.get()
            asyncio.create_task(self.__process_message(message))
            await asyncio.sleep(0.2)

    async def __process_message(self,message):
        print(f"{datetime.datetime.now().time()} ----> {self.name} Received message: {message}")
        if "hello" in message:
            print(f"{datetime.datetime.now().time()} ----> {self.name} Message contains 'hello': {message}")
        elif "crypto" in message:
            # Schedule __transferToken to run as a separate task
            asyncio.create_task(self.__transferToken())
    

