import re
import json

class LexicalAnalyser:
    def __init__(self):
        with open("patterns.json") as js_file:
            data = json.load(js_file)
        self.keywords = data["keywords"]
        self.operators = data['operators']
        self.IDENTIFIER = data['regex']["IDENTIFIER"]
        self.INTEGER = data['regex']['INTEGER']
        self.FLOAT = data['regex']['FLOAT']
        self.STRING = data['regex']['STRING']
        self.DELIMIT = data['regex']['DELIMIT']
        self.table = []
    
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
        r = re.compile(self.DELIMIT)
        m = r.match(tok)
        if(m == None):
            return False
        if(m.end() - m.start() == len(tok)):
            return True
        return False

    def separate_delimits(self, text):
        m = re.compile(self.DELIMIT)
        delimiters = list(m.finditer(text))
        cont = 0

        for i in delimiters:
            if(cont != i.start()): #existe algo antes do delimitador
                self.table.append(text[cont:i.start()])
            self.table.append(text[i.start()]) #adiciona o delimitador
            cont = i.start()+1
        
        if(cont != len(text)): #existe texto após o último delimitador
            self.table.append(text[cont:])

    def separate_whitespace(self):
        cont = 0
        p = re.compile("[\S]+")
        while(cont < len(self.table)):
            delimiters = list(p.finditer(self.table[cont]))
            if(len(delimiters) == 0): # não há texto
                self.table.pop(cont)
                cont += 1
                # print("Cont: {}, Texto: {}, lista: {}".format(cont, self.table[cont], self.table))
            else:
                self.table.pop(cont)
                for i in delimiters:
                    self.table.insert(cont, i.group())
                    cont += 1


    def readCode(self, text):
        self.separate_delimits(text)
        print(self.get_table())
        self.separate_whitespace()
        print(self.get_table())
    
    def get_table(self):
        return self.table

lex = LexicalAnalyser()
ex = "void main() {\nint a, b, c;\n c = a + b; }"
lex.readCode(ex)