import asyncio

from orchestrator.executor import call_agent


async def main():

    result = await call_agent(
        "rag_agent",
        {
            "query":"What is the operating temperature of IMX-450?"
        }
    )

    print(result)


if __name__ == "__main__":

    asyncio.run(main())