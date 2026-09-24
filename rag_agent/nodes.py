from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate
)

from rag_agent.chroma_store import vector_store
from dotenv import load_dotenv

# 1. ALWAYS LOAD THIS FIRST
load_dotenv() 


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

################### Retrieval nodes ##################
async def retrieve_node(state):

    query = state["query"]

    component_ids = state.get(
        "component_ids",
        []
    )

    if component_ids:

        documents = []

        for component_id in component_ids:

            docs = vector_store.similarity_search(
                query,
                k=4,
                filter={
                    "component_id": component_id
                }
            )

            documents.extend(docs)

    else:

        documents = (
            vector_store
            .similarity_search(
                query,
                k=4
            )
        )

    return {
        "documents": documents
    }

###########context node ############
async def context_node(state):

    documents = state["documents"]

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    sources = [
        doc.metadata
        for doc in documents
    ]

    return {
        "context": context,
        "sources": sources
    }




#answer node
async def answer_node(state):

    query = state["query"]

    context = state["context"]

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
            You are an Infineon technical
            documentation assistant.

            Answer only using the supplied
            documentation.

            Never invent specifications.

            If information is missing,
            explicitly say that it is not
            available in the retrieved documents.
            """
        ),

        (
            "human",
            """
            Question:
            {query}

            Documentation:
            {context}
            """
        )
    ])

    chain = prompt | llm

    response = await chain.ainvoke({
        "query": query,
        "context": context
    })

    return {
        "answer": response.content
    }

