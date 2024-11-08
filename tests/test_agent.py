import asyncio
import unittest
import os
from unittest.mock import patch
from src.agent.agent import Agent
from src.agent.message_router import MessageRouter
from src.blockchain.blockchain import get_balance,transfer_token

class TestAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = Agent("Test Agent")
        self.SOURCE_ADDRESS = os.getenv("SOURCE_ADDRESS")

    
    async def test_generate_random_messages(self):
        message_task = asyncio.create_task(self.agent.generate_random_messages())
        # giving some time so that process can run
        await asyncio.sleep(1)  
        message_task.cancel()
        # generated message should be present in agent outbox
        self.assertFalse(self.agent.outbox.empty(), "Outbox should contain at least one message")
        

    @patch('src.blockchain.blockchain.token_contract')
    async def test_check_erc20_balance(self, mock_token_contract):
        mock_token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
        token_balance_task = asyncio.create_task(get_balance(self.SOURCE_ADDRESS))
        await asyncio.sleep(1)  
        token_balance_task.cancel()
        #for checking token balance the balanceOf function will get invoked once
        mock_token_contract.functions.balanceOf.assert_called_once_with(self.SOURCE_ADDRESS)
    
    async def test_handle_messages_hello(self):
        await self.agent.inbox.put("hello agent")
        handle_messages_task=asyncio.create_task(self.agent.handle_messages())
        await asyncio.sleep(1)  
        # message present in the inbox should get processed and the queue should get empty
        self.assertTrue(self.agent.inbox.empty())
        handle_messages_task.cancel()

    @patch('src.blockchain.blockchain.token_contract')
    @patch('src.blockchain.blockchain.web3')
    async def test_handle_token_transfer(self,mock_web3, mock_token_contract):
        mock_token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
        mock_web3.eth.get_transaction_count.return_value = 1
        mock_web3.to_wei.return_value = 1000000000000000000
        mock_transfer = mock_token_contract.functions.transfer.return_value.build_transaction.return_value = {
            'from': self.SOURCE_ADDRESS,
            "to" : self.SOURCE_ADDRESS,
            'nonce': 1,
            'gas': 2000000,
            'gasPrice': 5000000000,
            'value': 1000000000000000000,
        }
       
        handle_transfer_token_task=asyncio.create_task(transfer_token(self.SOURCE_ADDRESS,self.SOURCE_ADDRESS))
        await asyncio.sleep(1)  
        self.assertTrue(self.agent.inbox.empty())
        handle_transfer_token_task.cancel()
        # as we have the "crypto" word in the message so the token transfer should get invoked
        mock_token_contract.functions.transfer.assert_called_once()

class TestMessageRouter(unittest.IsolatedAsyncioTestCase):

    async def test_route_messages(self):
        agent1 = Agent("ALICE")
        agent2 = Agent("BOB")
        router = MessageRouter(agent1, agent2)
        # adding some message in agent1 outbox now the message router should deliver this message into agent2's inbox
        await agent1.outbox.put("Test Message from ALICE")
        route_messages_task=asyncio.create_task(router.route_messages())
        await asyncio.sleep(1) 
        route_messages_task.cancel() 
        self.assertTrue(agent2.inbox.qsize() > 0, "Agent2's inbox should contain the message.")
        received_message = await agent2.inbox.get()
        self.assertEqual(received_message, "Test Message from ALICE", "Agent2 should receive the routed message.")


class TestAgentIntegration(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.agent1 = Agent("ALICE")
        self.agent2 = Agent("BOB")
        self.router = MessageRouter(self.agent1, self.agent2)
        self.SOURCE_ADDRESS = os.getenv("SOURCE_ADDRESS")

    @patch('src.blockchain.blockchain.token_contract')
    @patch('src.blockchain.blockchain.web3')
    async def test_agent_message_flow(self,mock_web3, mock_token_contract):
        #  agent1 message generation
        message_gen_task = asyncio.create_task(self.agent1.generate_random_messages())
        
        # Start the message router to transfer messages from agent1 to agent2
        router_task = asyncio.create_task(self.router.route_messages())
        
        # Prepare agent2 to handle messages
        handle_task = asyncio.create_task(self.agent2.handle_messages())
        mock_token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
        mock_web3.eth.get_transaction_count.return_value = 1
        mock_web3.to_wei.return_value = 1000000000000000000
        mock_transfer = mock_token_contract.functions.transfer.return_value.build_transaction.return_value = {
            'from': self.SOURCE_ADDRESS,
            "to" : self.SOURCE_ADDRESS,
            'nonce': 1,
            'gas': 2000000,
            'gasPrice': 5000000000,
            'value': 1000000000000000000,
        }
        # giving some time so that process can run
        await asyncio.sleep(4) 

        #in coming and outgoing messages from queue should be proceed
        self.assertTrue(self.agent1.outbox.empty())
        self.assertTrue(self.agent2.inbox.empty())
        # stop  the background tasks
        message_gen_task.cancel()
        router_task.cancel()
        handle_task.cancel()
        
        


if __name__ == "__main__":
    unittest.main()
