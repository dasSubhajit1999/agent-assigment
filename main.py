import asyncio
from agent import Agent
from message_router import MessageRouter

async def run_agents():

    agent1 = Agent("ALICE")
    agent2 = Agent("BOB")
    router = MessageRouter(agent1, agent2)
    try:
        await asyncio.gather(
            router.route_messages(),
            agent1.generate_random_messages(),
            # agent2.generate_random_messages(),
            agent1.check_erc20_balance(),
            # agent2.check_erc20_balance(),
            # agent1.handle_messages(),
            agent2.handle_messages()
        )
    except asyncio.CancelledError:
        print("Tasks were cancelled.☠️")

async def main():
    try:
        await run_agents()
    except KeyboardInterrupt:
        
        tasks = [t for t in asyncio.all_tasks() if not t.done()]
        for task in tasks:
            task.cancel()
        
        print("All tasks cancelled gracefully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted. Exiting gracefully.")