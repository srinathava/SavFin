import operator
from pyparsing import *
from datetime import datetime

__all__ = ['compilePattern']

globalStack = []
parserObj = []

OPMAP = {
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne
        }

def lookupOp(opstr):
    return OPMAP[opstr]

class OrPattern:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def match(self, t):
        return self.lhs.match(t) or self.rhs.match(t)

    @staticmethod
    def push(string_, loc, tokens):
        r = OrPattern(globalStack.pop(), globalStack.pop())
        globalStack.append(r)

class AndPattern:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def match(self, t):
        return self.lhs.match(t) and self.rhs.match(t)

    @staticmethod
    def push(string_, loc, tokens):
        r = AndPattern(globalStack.pop(), globalStack.pop())
        globalStack.append(r)

class DescPattern:
    def __init__(self, desc):
        self.desc = desc

    def match(self, t):
        return self.desc.lower() in t.desc.lower()

    @staticmethod
    def push(string_, loc, tokens):
        r = DescPattern(tokens[2])
        globalStack.append(r)

class AmountPattern:
    def __init__(self, opstr, amount):
        self.op = lookupOp(opstr)
        self.amount = float(amount)

    def match(self, t):
        return self.op(t.amount, self.amount)

    @staticmethod
    def push(string_, loc, tokens):
        r = AmountPattern(tokens[1], tokens[2])
        globalStack.append(r)

class AccountPattern:
    def __init__(self, tofrom, pattern):
        self.fcn = lambda obj: operator.attrgetter(tofrom + 'Path')(obj).lower()
        self.pattern = pattern

    def match(self, t):
        return self.pattern.lower() in self.fcn(t)

    @staticmethod
    def push(string_, loc, tokens):
        r = AccountPattern(tokens[0], tokens[2])
        globalStack.append(r)

class DatePattern:
    def __init__(self, opstr, datestr):
        self.op = lookupOp(opstr)
        self.date = datetime.strptime(datestr, '%m/%d/%y')

    def match(self, t):
        return self.op(t.date, self.date)

    @staticmethod
    def push(string_, loc, toks):
        r = DatePattern(toks[1], toks[2])
        globalStack.append(r)

def getParser():
    lpar = Literal('(').suppress()
    rpar = Literal(')').suppress()

    descString = QuotedString('"')
    descRule = (Literal("desc") + Literal("contains") + descString('string')).setParseAction(DescPattern.push)

    cmpOp = oneOf(OPMAP.keys())
    amountRule = (Literal("amount") + cmpOp + Regex(r'[-+]?(\d+)(\.\d+)?')).setParseAction(AmountPattern.push)

    accountRule = (oneOf(('from', 'to')) + 'contains' + descString).setParseAction(AccountPattern.push)

    dateString = Regex(r'(\d\d?)/(\d\d?)/(\d\d)')
    dateRule = (Literal('date') + cmpOp + dateString).setParseAction(DatePattern.push)

    expr = Forward()

    lpar = Literal('(').suppress()
    rpar = Literal(')').suppress()

    atom = (amountRule | descRule | accountRule | dateRule) | (lpar + expr.suppress() + rpar)

    andExpr = atom + ZeroOrMore( (Literal('and') + atom).setParseAction(AndPattern.push) )
    expr << andExpr + ZeroOrMore( (Literal('or') + andExpr).setParseAction(OrPattern.push) )

    return expr

parserObj = getParser()

def compilePattern(string_):
    global globalStack
    global parserObj
    globalStack = []
    results = parserObj.parseString(string_, parseAll=True)
    return globalStack.pop()

def test():
    class Transaction:
        def __init__(self):
            pass

    t = Transaction()
    t.date = datetime(2011, 3, 3)
    t.toPath = 'foo di ba'
    t.fromPath = 'blah di ba'

    print compilePattern('(date > 01/01/11) and ( (accountTo contains "blah") or (accountFrom contains "blah") )').match(t)

if __name__ == "__main__":
    test()

