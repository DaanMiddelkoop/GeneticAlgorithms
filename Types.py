from enum import Enum
import random


class Type(Enum):
    INT = 0
    BOOL = 1

    def generate_random_value(self):
        if self == Type.INT:
            return random.choice([
                0,
                1,
                random.randint(0, 100)
            ])

        if self == Type.BOOL:
            return random.choice([
                True,
                False
            ])

    @staticmethod
    def generate_random_type():
        return random.choice([
            Type.INT,
            Type.BOOL
        ])


class Operator(Enum):
    PLUS = 0
    MINUS = 1
    MULT = 2
    DIV = 3
    MOD = 4

    GT = 5
    LT = 6
    EQ = 7
    LE = 8
    GE = 9
    NE = 10

    TILDE = 11

    def get_string(self):
        switcher = {
            Operator.PLUS: " + ",
            Operator.MINUS: " - ",
            Operator.MULT: " * ",
            Operator.DIV: " // ",
            Operator.MOD: " % ",

            Operator.GT: " > ",
            Operator.LT: " < ",
            Operator.EQ: " == ",
            Operator.LE: " <= ",
            Operator.GE: " >= ",
            Operator.NE: " != ",

            Operator.TILDE: " ~"
        }
        return switcher[self]
