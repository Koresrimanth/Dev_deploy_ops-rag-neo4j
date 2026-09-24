from neo4j import AsyncGraphDatabase

import os

from dotenv import load_dotenv


load_dotenv()


driver = AsyncGraphDatabase.driver(

    os.getenv("NEO4J_URI"),

    auth=(

        os.getenv(
            "NEO4J_USERNAME"
        ),

        os.getenv(
            "NEO4J_PASSWORD"
        )
    )
)


#cypher execution

async def execute_query(
    cypher: str,
    parameters: dict = None
):

    async with driver.session() as session:

        result = await session.run(
            cypher,
            parameters or {}
        )

        records = await result.data()

        return records



#cypher generation


from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate
)

# from .neo4j_client import execute_query


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)



async def execute_query_node(state):

    cypher = state["cypher"]

    result = await execute_query(
        cypher
    )

    return {
        "db_result": result
    }





async def generate_cypher_node(state):

    query = state["query"]

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
            You are a Neo4j Cypher expert.

            Database schema:

            Supplier:
                name

            Component:
                id
                name

            Product:
                name

            Relationships:

            Supplier
              -[:MANUFACTURES]->
            Component

            Component
              -[:USED_IN]->
            Product

            Component
              -[:DEPENDS_ON]->
            Component

            Generate a READ-ONLY Cypher query.

            Do not generate:
            CREATE
            DELETE
            DROP
            SET
            MERGE
            REMOVE

            Return only Cypher.
            """
        ),

        (
            "human",
            "{query}"
        )
    ])

    chain = prompt | llm

    response = await chain.ainvoke({
        "query": query
    })

    cypher = response.content

    cypher = (
        cypher
        .replace("```cypher", "")
        .replace("```", "")
        .strip()
    )

    return {
        "cypher": cypher
    }



async def answer_node(state):

    query = state["query"]

    db_result = state["db_result"]

    prompt = f"""
    You are a supply-chain assistant.

    User question:
    {query}

    Neo4j query result:
    {db_result}

    Answer using only the database result.

    Do not invent relationships.
    """

    response = await llm.ainvoke(
        prompt
    )

    return {
        "answer": response.content
    }
