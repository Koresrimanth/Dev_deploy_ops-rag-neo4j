from neo4j import GraphDatabase

import os
from dotenv import load_dotenv


load_dotenv()


driver = GraphDatabase.driver(

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


def create_database():

    with driver.session() as session:

        session.run("""
        MATCH (n)
        DETACH DELETE n
        """)

        session.run("""
        CREATE
        (sa:Supplier {
            name: 'Supplier Alpha'
        }),

        (sb:Supplier {
            name: 'Supplier Beta'
        }),

        (sg:Supplier {
            name: 'Supplier Gamma'
        }),

        (imx450:Component {
            id: 'IMX-450',
            name: 'IMX-450'
        }),

        (imx700:Component {
            id: 'IMX-700',
            name: 'IMX-700'
        }),

        (pmx100:Component {
            id: 'PMX-100',
            name: 'PMX-100'
        }),

        (sic300:Component {
            id: 'SIC-300',
            name: 'SIC-300'
        }),

        (pcu:Product {
            name: 'Automotive Power Control Unit'
        }),

        (bms:Product {
            name: 'EV Battery Management System'
        }),

        (charger:Product {
            name: 'Charging Controller'
        }),

        (motor:Product {
            name: 'Industrial Motor Controller'
        })
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Alpha'}),
            (c:Component {id: 'IMX-450'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Alpha'}),
            (c:Component {id: 'PMX-100'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Beta'}),
            (c:Component {id: 'IMX-700'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Beta'}),
            (c:Component {id: 'SIC-300'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Gamma'}),
            (c:Component {id: 'PMX-100'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (s:Supplier {name: 'Supplier Gamma'}),
            (c:Component {id: 'SIC-300'})
        CREATE
            (s)-[:MANUFACTURES]->(c)
        """)

        session.run("""
        MATCH
            (c:Component {id: 'IMX-450'}),
            (p:Product {
                name: 'Automotive Power Control Unit'
            })
        CREATE
            (c)-[:USED_IN]->(p)
        """)

        session.run("""
        MATCH
            (c:Component {id: 'IMX-700'}),
            (p:Product {
                name: 'EV Battery Management System'
            })
        CREATE
            (c)-[:USED_IN]->(p)
        """)

        session.run("""
        MATCH
            (c:Component {id: 'PMX-100'}),
            (p:Product {
                name: 'Charging Controller'
            })
        CREATE
            (c)-[:USED_IN]->(p)
        """)

        session.run("""
        MATCH
            (c:Component {id: 'SIC-300'}),
            (p:Product {
                name: 'Industrial Motor Controller'
            })
        CREATE
            (c)-[:USED_IN]->(p)
        """)

        # Component dependencies

        session.run("""
        MATCH
            (a:Component {id: 'IMX-450'}),
            (b:Component {id: 'PMX-100'})
        CREATE
            (a)-[:DEPENDS_ON]->(b)
        """)

        session.run("""
        MATCH
            (a:Component {id: 'IMX-700'}),
            (b:Component {id: 'SIC-300'})
        CREATE
            (a)-[:DEPENDS_ON]->(b)
        """)

    print(
        "Neo4j database initialized."
    )


if __name__ == "__main__":

    create_database()