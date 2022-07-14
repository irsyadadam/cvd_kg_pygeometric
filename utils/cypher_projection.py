from neo4j import GraphDatabase
import pandas as pd



class projection:
    def __init__(self, uri, password) -> None:
        self.driver = self.driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    @classmethod
    def write_directed_projection(cls, tx) -> any:
        query = ("""
            CALL gds.graph.project(
            'entire_kg',
            ['Document', 'Drug', 'MeSH', 'Pathway', 'Protein'],
            {
                ASSIGNS: {orientation: 'NATURAL'},
                CANDIDATE: {orientation: 'NATURAL'},
                MENTIONS: {orientation: 'NATURAL'},
                TARGET: {orientation: 'NATURAL'}
            })
        """)
        result = tx.run(query)
        return result.data()

    @classmethod
    def write_undirected_projection(cls, tx) -> any:
        query = ("""
            CALL gds.graph.project(
            'entire_kg',
            ['Document', 'Drug', 'MeSH', 'Pathway', 'Protein'],
            {
                ASSIGNS: {orientation: 'UNDIRECTED'},
                CANDIDATE: {orientation: 'UNDIRECTED'},
                MENTIONS: {orientation: 'UNDIRECTED'},
                TARGET: {orientation: 'UNDIRECTED'}
            })
        """)
        result = tx.run(query)
        return result.data()
    

    @classmethod
    def check_projections(cls, tx) -> any:
        query = ("""
            CALL gds.graph.list
        """)
        result = tx.run(query)
        return result.data()

    @classmethod
    def drop_projections(cls, tx) -> any:
        query = ("""
            CALL gds.graph.drop('entire_kg') YIELD graphName;
        """)
        result = tx.run(query)
        return result.data()

    def overwrite_projections(self) -> None:
        result = self.driver.session().write_transaction(self.drop_projections)
        return result


    def sweep_projections(self) -> None:
        #check all projectsions
        projection_list = self.driver.session().write_transaction(self.check_projections)
        return projection_list






    def run_directed_projection(self) -> any:
        new_projection = self.driver.session().write_transaction(self.write_directed_projection)
        return new_projection

    def run_undirected_projection(self) -> any:
        new_projection = self.driver.session().write_transaction(self.write_undirected_projection)
        return new_projection

