import random


class Scope:
    variables = None
    scope_handler = None
    depth = 0

    def __init__(self, scope_handler):
        self.variables = []
        self.scope_handler = scope_handler
        self.depth = 0

    def add_var(self, item):
        self.variables.append(item)

    def get_vars(self):
        return self.variables

    def create_new_var(self, type):
        var = self.scope_handler.create_new_var(type)
        return var

    def get_random_var(self):
        return random.choice(self.variables)

    def getTabs(self):
        tabs = ""
        for i in range(self.depth):
            tabs += "\t"
        return tabs

class ScopeHandler:
    next_value = 0

    def __init__(self):
        self.next_value = 0

    def create_new_var(self, type):
        new_var = Variable("v" + str(self.next_value), type)
        self.next_value += 1
        return new_var


class Variable:
    name = None
    type = None

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_type(self):
        return self.type
