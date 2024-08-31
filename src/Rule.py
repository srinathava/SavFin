import re

class SimpleRule:
    def __init__(self, pattern='', accountFrom=None, accountTo=None, setDuplicate=None):
        self.pattern = pattern.lower()
        self.accountFrom = accountFrom
        self.accountTo = accountTo
        self.setDuplicate = setDuplicate

    def __setstate__(self, state):
        # calling __init__ ensures that newly added properties since the
        # pickle was saved also exist.
        self.__init__()
        for it in state:
            self.__dict__[it] = state[it]

    @property
    def fromPath(self):
        if self.accountFrom:
            return self.accountFrom.path
        else:
            return ''

    @property
    def toPath(self):
        if self.accountTo:
            return self.accountTo.path
        else:
            return ''

    def run(self, trans):
        if not (self.pattern in trans.desc.lower()):
            return False

        if self.accountFrom:
            # only check that accountFrom matches if the rule specifies an
            # account.
            if self.accountFrom != trans.accountFrom:
                return False

        if self.accountTo and (not trans.accountTo):
            trans.accountTo = self.accountTo

        if self.setDuplicate:
            trans.isDuplicate = True

        return True

class AdvancedRule:
    ITEMS_TO_SAVE = ['patternText', 'accountFrom', 'accountTo', 'setDuplicate']

    def __init__(self, patternText='', accountFrom=None, accountTo=None):
        self.patternText = patternText
        self.accountFrom = accountFrom
        self.accountTo = accountTo
        self.setDuplicate = None

        self.pattern = None

        if self.patternText:
            self.compilePattern()

    def __setstate__(self, state):
        self.__init__()
        for it in state:
            self.__dict__[it] = state[it]

        self.compilePattern()

    def __getstate__(self):
        dict = {}
        for it in self.ITEMS_TO_SAVE:
            dict[it] = self.__dict__[it]
        return dict

    def compilePattern(self):
        self.pattern = compilePattern(self.patternText)

    def run(self, trans):
        if self.pattern.match(trans):
            if self.accountFrom and (not trans.accountFrom):
                trans.accountFrom = self.accountFrom

            if self.accountTo and (not trans.accountTo):
                trans.accountTo = self.accountTo

            if self.setDuplicate is not None:
                trans.isDuplicate = self.setDuplicate

            return True
        else:
            return False

class Rule:
    def __init__(self, evalstr='', category=''):
        self.evalstr = evalstr
        self.category = category

    def matches(self, trans):
        return eval(self.evalstr, trans.__dict__)

PAT_RULE_START = re.compile(r'(\w+)\s*:\s*$')
PAT_EVAL_RULE = re.compile(r'(\w+):\s*(.*)\s*')

def loadRules(simpleRuleFile, evalRuleFile):
    lines = open(simpleRuleFile).readlines()
    rules = []
    for line in lines:
        m = PAT_RULE_START.match(line)
        if m:
            r = Rule()
            rules.append(r)
            r.category = m.group(1)
        elif line.strip() and rules:
            r[-1].evalstr = r'''r"""%s""" in desc''' % line.strip()

    lines = open(evalRuleFile).readlines()
    for line in lines:
        m = PAT_EVAL_RULE.match(line)
        if m:
            rules.append(Rule(m.group(2), m.group(1)))

    return rules
