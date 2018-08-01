from Scope import Scope, ScopeHandler, Variable
from Types import Type
from Graph import Block
from copy import deepcopy
import traceback
import random



class Pool:
    trees = None
    best_tree = None
    smallest_error = None

    def __init__(self):
        self.trees = []
        self.smallest_error = 9999999999999999999999999999999999999999999999999999
        for i in range(0, 10):
            scope = Scope(ScopeHandler())
            scope.add_var(Variable("arg1", Type.INT))
            scope.add_var(Variable("arg2", Type.INT))
            scope.add_var(Variable("boolvar", Type.BOOL))
            # add initial variables to scope.

            tree = Block(None, scope)
            self.trees.append(tree)

        self.best_tree = None

    def execute_trees(self):
        for tree in self.trees:
            error = 0
            for i in range(0, 10):
                for j in range(0, 10):

                    program = ""
                    for line in tree.lines():
                        program += line + "\n"
                    try:
                        #exec(program)
                        ldict = {"arg1": i, "arg2": j, "boolvar": True}
                        exec(program, globals(), ldict)
                        #print(ldict["arg1"], i)
                        arg1 = ldict["arg1"]
                        error += pow(arg1 - (i + j), 2)
                    except Exception:
                        traceback.print_exc()
                        error += 999999999999999999999999999999999999999999999999999999999999999999999999999999999
            if error < self.smallest_error:
                self.best_tree = tree
                self.smallest_error = error
        return self.smallest_error

    def alter_best_tree(self):
        if self.best_tree is not None:
            for i in range(len(self.trees)):
                self.trees[i] = random.choice([
                    deepcopy(self.best_tree),
                    self.trees[i]
                ])
                for i in range(0, 10):
                    self.trees[i].randomize()


