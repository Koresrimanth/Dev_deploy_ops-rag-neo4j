from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_core.documents import Document


PERSIST_DIRECTORY = "./data/chroma"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


documents = [

    Document(
        page_content="""
        IMX-450 is a high-efficiency automotive
        power module.

        Operating temperature:
        -40°C to 125°C.

        Input voltage:
        12V to 48V.

        Maximum output current:
        30A.

        The module is designed for automotive
        power control applications.

        Supplier:
        Supplier Alpha.
        """,
        metadata={
            "component_id": "IMX-450",
            "document_type": "technical_specification",
            "domain": "power"
        }
    ),

    Document(
        page_content="""
        IMX-700 is an automotive power management
        controller.

        Operating temperature:
        -40°C to 150°C.

        Input voltage:
        24V to 60V.

        Maximum output current:
        45A.

        IMX-700 is primarily used in
        electric vehicle battery management systems.

        Supplier:
        Supplier Beta.
        """,
        metadata={
            "component_id": "IMX-700",
            "document_type": "technical_specification",
            "domain": "automotive"
        }
    ),

    Document(
        page_content="""
        PMX-100 is a compact charging power controller.

        Operating temperature:
        -20°C to 125°C.

        Input voltage:
        9V to 36V.

        Maximum output current:
        20A.

        PMX-100 is designed for charging
        controller applications.

        Suppliers:
        Supplier Alpha and Supplier Gamma.
        """,
        metadata={
            "component_id": "PMX-100",
            "document_type": "technical_specification",
            "domain": "charging"
        }
    ),

    Document(
        page_content="""
        SIC-300 is a silicon carbide power module
        designed for high-efficiency industrial
        motor control.

        Operating temperature:
        -40°C to 175°C.

        Input voltage:
        400V to 800V.

        Maximum output current:
        100A.

        SIC-300 is used in industrial motor
        controller systems.

        Suppliers:
        Supplier Beta and Supplier Gamma.
        """,
        metadata={
            "component_id": "SIC-300",
            "document_type": "technical_specification",
            "domain": "industrial"
        }
    ),

    Document(
        page_content="""
        IMX-450 installation guide.

        The component should be installed in a
        temperature-controlled environment.

        The recommended operating temperature
        range is -40°C to 125°C.

        Proper thermal management is required
        when operating close to the upper
        temperature limit.
        """,
        metadata={
            "component_id": "IMX-450",
            "document_type": "installation_guide",
            "domain": "power"
        }
    ),

    Document(
        page_content="""
        IMX-700 reliability documentation.

        IMX-700 supports operation up to 150°C.

        Thermal design should account for
        continuous operation at high temperature.

        Recommended use cases include EV battery
        management and high-voltage automotive
        power systems.
        """,
        metadata={
            "component_id": "IMX-700",
            "document_type": "reliability",
            "domain": "automotive"
        }
    ),

    Document(
        page_content="""
        Supplier Alpha experienced a temporary
        manufacturing delay during the current
        production cycle.

        Components affected by the delay include
        IMX-450 and PMX-100.

        Engineering teams should evaluate inventory
        availability for these components.
        """,
        metadata={
            "component_id": "IMX-450",
            "document_type": "supply_chain_notice",
            "supplier": "Supplier Alpha"
        }
    ),

    Document(
        page_content="""
        Supplier Beta production capacity has been
        reduced for a scheduled maintenance period.

        Components potentially affected include
        IMX-700 and SIC-300.
        """,
        metadata={
            "document_type": "supply_chain_notice",
            "supplier": "Supplier Beta"
        }
    )
]

def create_vector_store():

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="infineon_docs",
        persist_directory=PERSIST_DIRECTORY
    )

    return vector_store

from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = Chroma(
    collection_name="infineon_docs",
    embedding_function=embeddings,
    persist_directory="./data/chroma"
)


retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4
    }
)


if __name__ == "__main__":

    create_vector_store()

    print(
        "ChromaDB initialized successfully."
    )