import neo4j
from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os
from tqdm import tqdm



class edge_list():
    """Class to gather the edge list and create dgl graph"""
    def __init__(self, uri: str, password: str) -> None:
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    def close(self) -> None:
        self.driver.close()

    @classmethod
    def edge_list(cls, tx) -> any:
        query = ("""
                    MATCH path=(m)--(n)
                    RETURN ID(m) AS u, ID(n) AS v
                """)
        result = tx.run(query)
        #return a dataframe
        return result.data() 

    def get_edge_list(self) -> any:
        result = self.driver.session().write_transaction(self.edge_list)
        return pd.DataFrame(result)

    def nx_graph_from_cypher(self, data: pd.DataFrame):
        """
        Takes the whole graph and creates dgl graph
        ARGS:
            data is the edge list in a pandas df
            
        RETURNS: dgl graph
        """
        edge_list = []
        u = data["u"].to_numpy()
        v = data["v"].to_numpy()

        for i, j in zip(u, v):
            edge_list.append(str(i) + " " + str(j))

        # print(edge_list)
        return nx.parse_edgelist(edge_list, nodetype=str)

    def true_labels(cls, tx):
        query = ("""
                    MATCH (n)
                    RETURN ID(n) as id, n.team as team
        """)
        result = tx.run(query)
        #return a dataframe
        return result.data() 
    
    def get_true_labels(self) -> any:
        result = self.driver.session().write_transaction(self.true_labels)
        return pd.DataFrame(result)
