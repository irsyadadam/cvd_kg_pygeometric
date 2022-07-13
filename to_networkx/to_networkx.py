import neo4j
from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os
from tqdm import tqdm


from edge_list import *


if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    password = "heart"

    hello = edge_list(uri, password)
    edge_list = hello.get_edge_list()

    G = hello.nx_graph_from_cypher(edge_list)
    print('   %d nodes.'% G.number_of_nodes())
    print('   %d edges.'% G.number_of_edges())
