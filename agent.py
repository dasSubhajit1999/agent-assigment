import asyncio
import random
import json
import datetime
from web3 import Web3
from web3.exceptions import InvalidAddress
from dotenv import load_dotenv
import os

load_dotenv()


AMOY_RPC_URL = os.getenv("AMOY_RPC_URL")
SOURCE_ADDRESS = os.getenv("SOURCE_ADDRESS")
TARGET_ADDRESS = os.getenv("TARGET_ADDRESS")
PRIVATE_KEY= os.getenv("PRIVATE_KEY")
bnb_token_contract_address = os.getenv("BNB_TOKEN_CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(AMOY_RPC_URL))


def load_contract_abi(file_path: str):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")

        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON data.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the ABI: {e}")

bnb_token_abi = load_contract_abi('contracts_abi/bnb_token.json')
token_contract = web3.eth.contract(address=bnb_token_contract_address, abi=bnb_token_abi)
token_decimals = token_contract.functions.decimals().call()
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
            try:
                balance =await asyncio.to_thread(token_contract.functions.balanceOf(SOURCE_ADDRESS).call)
                print(f"{datetime.datetime.now().time()} ----> {SOURCE_ADDRESS} ERC-20 Balance: {balance/ (10 ** token_decimals)} tokens")
            except InvalidAddress:
                print("Error: The Ethereum address provided is invalid.")
            except Exception as e:
                print(f"An unexpected error occurred while checking the balance: {e}")
            await asyncio.sleep(10)
             


    async def __transferToken(self):
        try:
            print(f"{datetime.datetime.now().time()} ----> {SOURCE_ADDRESS} Transferring 1 token to {TARGET_ADDRESS}")
            balance = await asyncio.to_thread(token_contract.functions.balanceOf(SOURCE_ADDRESS).call)
            required_amount = 1 * (10 ** token_decimals)
            if balance >= required_amount:
               
                nonce = await asyncio.to_thread(web3.eth.get_transaction_count, SOURCE_ADDRESS,'pending')
                tx = await asyncio.to_thread(
                token_contract.functions.transfer(TARGET_ADDRESS, required_amount).build_transaction,
                {
                    'from': SOURCE_ADDRESS,
                    'nonce': nonce,
                    'gas': 2000000,
                    'gasPrice': web3.to_wei('50', 'gwei')
                }
            )
               
                signed_tx = await asyncio.to_thread(web3.eth.account.sign_transaction, tx, PRIVATE_KEY)
                
                tx_hash = await asyncio.to_thread(web3.eth.send_raw_transaction, signed_tx.raw_transaction)
                
                print(f"{datetime.datetime.now().time()}  ----> Transaction sent: 0x{tx_hash.hex()}")
               
            else:
                print(f"{datetime.datetime.now().time()} ----> Insufficient funds to complete the transaction")
        except InvalidAddress:
            print("Error: One of the Ethereum addresses provided is invalid.")
        except ValueError as e:
            print(f"Transaction Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during the transaction: {e}")



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
    

