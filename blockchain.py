import asyncio
import json
import datetime
from web3 import Web3
from web3.exceptions import InvalidAddress
from dotenv import load_dotenv
import os

load_dotenv()


AMOY_RPC_URL = os.getenv("AMOY_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
bnb_token_contract_address = os.getenv("BNB_TOKEN_CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(AMOY_RPC_URL))

def load_contract_abi(file_path: str):
    try:
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


async def get_balance(SOURCE_ADDRESS):
    try:
        balance = await asyncio.to_thread(token_contract.functions.balanceOf(SOURCE_ADDRESS).call)
        return balance / (10 ** token_decimals)  
    except InvalidAddress:
        print("Error: The Ethereum address provided is invalid.")
    except Exception as e:
        print(f"An unexpected error occurred while checking the balance: {e}")
    return None

async def transfer_token(SOURCE_ADDRESS,TARGET_ADDRESS):
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