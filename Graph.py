from Scope import Scope, Variable
import random
from abc import abstractmethod
from Types import Type, Operator


class Node:
    parent = None
    scope = None

    def __init__(self, parent, scope: Scope = None):

        self.parent = parent
        self.randomize()

    def randomize(self):
        pass

    def collect_variables(self, type: Type) -> [Variable]:
        variables = list(filter(lambda x: x.get_type() == type, self.scope.get_vars()))

        if self.parent is not None:
            variables.extend(self.parent.collect_variables(type))
        return variables

    @abstractmethod
    def lines(self):
        return []


class Block(Node):
    definitions = None
    alterations = None

    def __init__(self, parent, scope: Scope = None):
        self.definitions = []
        self.alterations = []

        if scope is None:
            scope = Scope(parent.scope.scope_handler)

        self.scope = scope
        super().__init__(parent, scope)


    def add_child(self, child):
        self.children.append(child)

    def lines(self):
        lines = []
        for i in self.definitions:
            lines.append(i.lines() + " #definition")

        for i in self.alterations:
            lines.append(i.lines() + " #alteration")
        return lines

    def add_random_child(self):
        child = generate_statement_node(self)
        if type(child) is Definition:
            self.definitions.append(child)
        else:
            self.alterations.append(child)

    def remove_random_child(self):
        if len(self.alterations) > 0:
            self.alterations.remove(random.choice(self.alterations))

    def randomize(self):
        random.choice([
            #self.remove_random_child,
            self.add_random_child,
            self.randomize_child,
            self.randomize_order,
            self.add_random_child,
            self.randomize_child,
            self.randomize_order,
            self.add_random_child,
            self.randomize_child,
            self.randomize_order,
        ])()

    def randomize_child(self):
        choice = random.choice([
            self.alterations,
            self.definitions
        ])
        if len(choice) > 0:
            random.choice(choice).randomize()

    def randomize_order(self):
        if len(self.alterations) > 0:
            random.shuffle(self.alterations)



class Definition(Node):
    target = None
    expression = None
    type = None

    def __init__(self, parent: Node):
        self.scope = parent.scope
        self.target = self.scope.create_new_var(Type.generate_random_type())
        self.type = self.target.get_type()
        super().__init__(parent)

        self.expression = generate_expression_node(self)
        self.scope.add_var(self.target)

    def randomize(self):
        pass

    def lines(self):
        a = self.scope.getTabs()
        b = self.target.name
        c = self.expression.lines()

        return a + b + " = " + c

    def get_type(self):
        return self.type

class Alteration(Node):
    target = None
    expression = None
    type = None

    def __init__(self, parent: Node):
        self.scope = parent.scope
        self.target = random.choice(self.collect_variables(Type.generate_random_type()))
        self.type = self.target.get_type()


        super().__init__(parent)

        self.type = self.target.get_type()
        self.expression = generate_expression_node(self)

    def randomize(self):
        random.choice([
            self.randomize_target,
            self.randomize_expression
        ])()

    def randomize_target(self):
        self.target = random.choice(self.collect_variables(Type.generate_random_type()))
        self.type = self.target.get_type()
        self.expression = generate_expression_node(self)


    def randomize_expression(self):
        self.expression = generate_expression_node(self)

    def lines(self):
        a = self.scope.getTabs()
        b = self.target.name
        c = self.expression.lines()

        return a + b + " = " + c

    def get_type(self):
        return self.type


class Expression(Node):
    type = None

    def __init__(self, parent):
        self.type = parent.get_type()
        self.scope = parent.scope
        super().__init__(parent)

    def get_type(self):
        return self.type

    def lines(self):
        return ""


class BinaryOperator(Expression):
    operator = None
    expr1 = None
    expr2 = None
    type = None

    def __init__(self, parent: Expression):
        super().__init__(parent)
        self.expr1 = generate_expression_node(self)
        self.expr2 = generate_expression_node(self)

        self.expr1.type = Type.INT
        self.expr2.type = Type.INT

        self.expr1.randomize()
        self.expr2.randomize()

    def randomize(self):
        if self.get_type() == Type.INT:
            self.operator = random.choice([
                Operator.MULT,
                Operator.MINUS,
                Operator.PLUS,
            ])
        elif self.get_type() == Type.BOOL:
            self.operator = random.choice([
                Operator.GE,
                Operator.LE,
                Operator.GT,
                Operator.LT,
                Operator.EQ,
                Operator.NE
            ])

    def lines(self):
        return "(" + self.expr1.lines() + self.operator.get_string() + self.expr2.lines() + ")"


class UnaryOperator(Expression):
    operator = None
    expr1 = None

    def __init__(self, parent):
        super().__init__(parent)
        self.expr1 = generate_expression_node(self)

    def randomize(self):
        self.operator = random.choice([
            Operator.MINUS,
            Operator.TILDE
        ])

    def lines(self):
        return "(" + self.operator.get_string() + self.expr1.lines() + ")"


class Constant(Expression):
    value = None

    def __init__(self, parent: Expression):
        self.type = parent.get_type()
        super().__init__(parent)

    def randomize(self):
        self.value = self.type.generate_random_value()

    def get_type(self):
        return self.value.get_type()

    def lines(self):
        return str(self.value)


class VariableNode(Expression):
    value = None

    def randomize(self):
        self.type = self.parent.get_type()
        self.value = random.choice(self.collect_variables(self.get_type()))

    def lines(self):
        return self.value.name


def generate_statement_node(parent):
    child = random.choice([
        Definition,
        Alteration,
        Alteration,
        Alteration,
        Alteration
    ])(parent)
    return child

def generate_expression_node(parent):
    child = random.choice([
        BinaryOperator,
        UnaryOperator,
        Constant,
        VariableNode
    ])(parent)

    return child