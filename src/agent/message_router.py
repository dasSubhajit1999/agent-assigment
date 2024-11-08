import asyncio
from agent import Agent

class MessageRouter:

    def __init__(self, agent1: Agent, agent2: Agent):
        self.agent1 = agent1
        self.agent2 = agent2

    async def route_messages(self) -> None:
        while True:
            if not self.agent1.outbox.empty():
                message = await self.agent1.outbox.get()
                await self.agent2.inbox.put(message)
                
            if not self.agent2.outbox.empty():
                message = await self.agent2.outbox.get()
                await self.agent1.inbox.put(message)
            await asyncio.sleep(1)