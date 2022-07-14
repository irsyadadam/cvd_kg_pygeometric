from neo4j import GraphDatabase
import pandas as pd

class FastRP():
    """Class to run Node Embedding"""
    def __init__(self, uri, password) -> None:
        self.driver = self.driver = GraphDatabase.driver(uri, auth=("neo4j", password))


    def close(self) -> None:
        self.driver.close()

    @classmethod
    def run_RP(cls, tx) -> any:
        """
        :param cls: is the class
        :param tx: is the transaction (documented in neo4j)
        :return: result.data() is the embeddings
        """
        query = ("""
        CALL gds.fastRP.stream('entire_kg',
            {
                embeddingDimension: 64
            }
        )
        YIELD nodeId, embedding
        RETURN gds.util.asNode(nodeId).name AS name, LABELS(gds.util.asNode(nodeId)) AS Type, gds.util.asNode(nodeId) AS NodeID, embedding AS Embedding
        """)
        result = tx.run(query)
        return result.data()

    def run_algo(self) -> any:
        """
        :param self:
        :return: result is the dataframe from the degree centrality
        """
        result = self.driver.session().write_transaction(self.run_RP)
        result = pd.DataFrame(result)
        return result