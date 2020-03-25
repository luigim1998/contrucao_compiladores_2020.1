import re

class lexical_analyser:
    def __init__(self):
        with open("patterns.json") as js_file:
            data = json.load(js_file)
        self.keywords = data["keywords"]
        self.operators = data['operators']
        self.IDENTIFIER = data['regex']["IDENTIFIER"]
        self.INTEGER = data['regex']['INTEGER']
        self.FLOAT = data['regex']['FLOAT']
        self.STRING = data['regex']['STRING']
        self.delimit = data['delimit']
    
    def isKeyword(self, tok):
        return tok in self.keywords
    
    def isOperator(self, tok):
        for i in self.operators.values():
            if(tok in i):
                return True
        return False

    def isIdentifier(self, tok):
        r = re.compile(self.IDENTIFIER)
        m = r.match(tok)
        if(m == None):
            return False
        if(m.end() - m.start() == len(tok)):
            return True
        return False

    def isInteger(self, tok):
        r = re.compile(self.INTEGER)
        m = r.match(tok)
        if(m == None):
            return False
        if(m.end() - m.start() == len(tok)):
            return True
        return False
    
    def isFloat(self, tok):
        r = re.compile(self.FLOAT)
        m = r.match(tok)
        if(m == None):
            return False
        if(m.end() - m.start() == len(tok)):
            return True
        return False
    
    def isString(self, tok):
        r = re.compile(self.STRING)
        m = r.match(tok)
        if(m == None):
            return False
        if(m.end() - m.start() == len(tok)):
            return True
        return False
    
    def isDelimit(self, tok):
        return tok in self.delimit