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

    def separate_text_delimits(self, text):
        cont = 0
        m = re.compile(self.DELIMIT)
        delimiters = list(m.finditer(text))
        out = []

        for i in delimiters:
            if(cont != i.start()): #existe algo antes do delimitador
                out.append(text[cont:i.start()])
            out.append(text[i.start()]) #adiciona o delimitador
            cont = i.start()+1
        
        if(cont != len(text)): #existe texto após o último delimitador
            out.append(text[cont:])
        
        return out

    def separate_text_whitespace(self, text):
        m = re.compile("[\S]+")
        # delimiters = list(m.finditer(text))
        # out = []
        # for i in delimiters:
        #     out.append(i.group())
        # return out
        return m.findall(text)

    def separate_whitespace(self, table):
        out = []

        for i in table:
            words = self.separate_text_whitespace(i)
            if(len(words) != 0): # não há texto
                out.extend(words)
        
        return out

    def separate_text_operators(self, text):
        out = [text]

        for i in ["relational", "logical", "assignment", "arithmetic", "inc_dec"]:
            for j in self.operators[i]:
                cont = 0
                while(cont < len(out)):
                    if(out[cont].find(j) != -1):
                        out = out[:cont] + list(out[cont].partition(j)) + out[cont+1:]
                        cont += 2
                    else:
                        cont += 1
        return out
    
    def separate_operators(self, table):
        out = []

        for i in table:
            words = self.separate_text_operators(i)
            if(len(words) != 0): # não há texto
                out.extend(words)
        
        return out

    def analyse_token(self, text):
        label = ''
        if(self.isKeyword(text)):
            label = 'KEYWORD'
        elif(self.isIdentifier(text)):
            label = 'IDENTIFIER'
        elif(self.isString(text)):
            label = 'STRING'
        elif(self.isDelimit(text)):
            label = 'DELIMITER'
        elif(self.isOperator(text)):
            label = 'OPERATOR'
        elif(self.isInteger(text)):
            label = 'NUMBER'
        elif(self.isFloat(text)):
            label = 'NUMBER'
        else:
            label = 'INVALID'
        return label

    def classify_tokens(self, table):
        out = []

        for i in table:
            out.append([i, self.analyse_token(i)])
        
        return out

    def readCode(self, text):
        self.table = self.separate_text_delimits(text)
        print(self.get_table())
        self.table = self.separate_operators(self.table)
        print(self.get_table())
        self.table = self.separate_whitespace(self.table)
        print(self.get_table())
        self.table = self.classify_tokens(self.table)
        print(self.get_table())
    
    def get_table(self):
        return self.table

lex = LexicalAnalyser()
ex = "void main() {\nint a, b, c;\n c = a + b; }"
ex2 = "void main() {\nint a, b, c;\n c = a + b;\n a=c-b;}"
lex.readCode(ex2)