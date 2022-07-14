import os
import shutil
import argparse
import time


from to_networkx.edge_list import edge_list
from utils.cypher_projection import projection

from embeddings.neo4j_fastRP import FastRP
from embeddings.neo4j_node2vec import node2vec



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="pygeom GCN on neo4j kg database")

    parser.add_argument("--test_embedding", default=False, action="store_true", help = "train the test data!")
    parser.add_argument("--test_model", default=False, action="store_true", help = "train the test data!")

    parser.add_argument("--uri", type=str, help="neo4j dbms uri", default="bolt://localhost:7687")
    parser.add_argument("--password", type=str, help="neo4j dbms password", default="heart")

    parser.add_argument("--embed", type=str, help="fastrp or node2vec", default="node2vec")

    args = parser.parse_args()

    print("\n============================================\n")
    
    if args.uri and args.password:
        hello = edge_list(args.uri, args.password)
        neo4j_edge_list = hello.get_edge_list()
        print("connected to %s" % args.uri)
    
    else:
        print("invalid args: no uri or password specified")
        exit()

    print("generating nx graph...")

    G = hello.nx_graph_from_cypher(neo4j_edge_list)

    print("nx graph creation success")
    print('   %d nodes.'% G.number_of_nodes())
    print('   %d edges.'% G.number_of_edges())

    print("\n============================================\n")

    if args.embed == "fastrp":
        print("generating embeddings using neo4j fastRP")
    
    elif args.embed == "node2vec":
        print("generating embeddings using (neo4j) node2vec")
    
    print("connected to %s" % args.uri)
    print("sweeping available cypher projections...")
    hello = projection(args.uri, args.password)
    result = hello.sweep_projections()

    flag = False

    #if there are projections present
    if result:
        for graph in result:
            if graph["graphName"] == "entire_kg":
                flag = True

    if flag:
        print("cypher projection found: overwriting projection ['entire_kg']")
        result = hello.overwrite_projections()

    else:
        print("cypher projection not found: creating new projection ['entire_kg']")

    
    if args.embed == "fastrp":
        result = hello.run_undirected_projection()

        embeddings_cls = FastRP(args.uri, args.password)
        embeddings = embeddings_cls.run_algo()
    
    elif args.embed == "node2vec":
        result = hello.run_directed_projection()

        embeddings_cls = node2vec(args.uri, args.password)
        embeddings = embeddings_cls.run_algo()
        print("\nWARNING: gdsl.beta.node2vec is version BETA. feature will be changed in future iterations")

    print("\nembedding successful")

    print("\n============================================\n")

    print("model training")







