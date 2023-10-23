from pyswip import Prolog


class PrologController:
    def __init__(self, file: str):
        self.prolog = Prolog()
        self.prolog.consult(file)

    def query(self, query):
        self.prolog.query(query)

    def pull_query(self, query):
        return list(self.prolog.query(query))

    def assertz(self, assertz):
        self.prolog.assertz(assertz)

    def retract(self, clause):
        self.prolog.retract(clause)

    def retractall(self, clause):
        self.prolog.retractall(clause)
