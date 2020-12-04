from treelib import *

class WeakPrecedenceAnalyzer:
    def __init__(self):
        self.tree = Tree()

    def combina_prod(self, pilha, producoes):
        """
        Retorna -1 se nenhuma produção combinar ou o índice da produção que combina.
        """
        for cont1 in range(len(producoes)):
            combina = True
            prod = producoes[cont1]
            if(len(pilha)-1 < len(prod[1])): # a pilha (desconsidere $) não tem quantidade de símbolos
                combina = False
                continue
            for cont2 in range(-1, -len(prod[1])-1, -1):
                if(pilha[cont2][1] == 'STATE' or
                   pilha[cont2][1] == 'OPERATOR' or
                   pilha[cont2][1] == 'DELIMITER'): # Verifica se é estado
                    if(prod[1][cont2] != pilha[cont2][0]):
                        combina = False
                elif(pilha[cont2][1] == 'IDENTIFIER'):
                    if(prod[1][cont2] != 'id'):
                        combina = False
                elif(pilha[cont2][1] == 'NUMBER'):
                    if(prod[1][cont2] != 'num'):
                        combina = False
                else:
                    combina = False
                
                if(not combina): break
                
            if(combina): return cont1
        return -1

    def verifica_atribuicao(self, sentenca):
        '''
        Reconhecimento de atribuição
        '''
        if(len(sentenca) < 3):
            return False
        if(sentenca[0][1] != 'IDENTIFIER'):
            return False
        if(sentenca[1][0] != '='):
            return False
        if(self.automato_op_arit(sentenca[2:])):
            print(self.tree.root)
            print(self.tree.children(self.tree.root))
            print(self.tree.children(self.tree.root)[0].identifier)
            print()
            root_children = self.tree.children(self.tree.root)[0].identifier
            self.tree.create_node(str(sentenca[1]), -1, parent=0, data=sentenca[1])
            self.tree.create_node(str(sentenca[0]), -2, parent=-1, data=sentenca[0])
            self.tree.move_node(root_children, -1)

            self.tree.root = -1
            self.tree.show(key=lambda x : x.identifier, idhidden=False)
            return True
        else:
            return False

    def escolher_linha(self, pilha_topo):
        l = -1
        if pilha_topo[1] == 'STATE':
            if   pilha_topo[0] == 'E': 
                l = 0
            elif pilha_topo[0] == 'M': 
                l = 1
            elif pilha_topo[0] == 'P': 
                l = 2
        elif pilha_topo[1] == 'OPERATOR':
            if   pilha_topo[0] == '+': 
                l = 3
            elif pilha_topo[0] == '-':
                l = 4
            elif pilha_topo[0] == '*': 
                l = 5
            elif pilha_topo[0] == '/':
                l = 6
        elif pilha_topo[1] == 'DELIMITER':
            if   pilha_topo[0] == '(': 
                l = 7
            elif pilha_topo[0] == ')':
                l = 8
        elif pilha_topo[1] == 'IDENTIFIER': 
            l = 9
        elif pilha_topo[1] == 'NUMBER':
            l = 10
        elif pilha_topo[1] == '$_DELIMITADOR':
            l = 11
        return l

    def escolher_coluna(self, token):
        c = -1
        if token[1] == 'OPERATOR':
            if   token[0] == '+': 
                c = 0
            elif token[0] == '-':
                c = 1
            elif token[0] == '*': 
                c = 2
            elif token[0] == '/':
                c = 3
        elif token[1] == 'DELIMITER':
            if   token[0] == '(': 
                c = 4
            elif token[0] == ')':
                c = 5
        elif token[1] == 'IDENTIFIER': 
            c = 6
        elif token[1] == 'NUMBER':
            c = 7
        elif token[1] == '$_DELIMITADOR':
            c = 8
        return c
    
    def is_concluded(self, last_token, pilha, simbolo_sentencial):
        print(last_token)
        print(pilha)
        if(last_token[1] == '$_DELIMITADOR' and len(pilha) == 2):
            if(pilha[0] == ['$', '$_DELIMITADOR'] and 
               pilha[1] == [simbolo_sentencial, 'STATE']):
                return True
        return False

    def automato_op_arit(self, sentenca):
        """
        Autômato para operação aritmética
        E -> E+M
        E -> E-M
        E -> M
        M -> M*P
        M -> M/P
        M -> P
        P -> (E)
        P -> id
        P -> num
        """

        self.tree = Tree()

        # delimitador
        sentenca_copy = sentenca.copy()
        sentenca_copy.append( ["$", '$_DELIMITADOR'])
        simbolo_sentencial = 'E'

        # produções
        producoes = [['E',['E','+','M']],
                     ['E',['E','-','M']],
                     ['E',['M'        ]],
                     ['M',['M','*','P']],
                     ['M',['M','/','P']],
                     ['M',['P'        ]],
                     ['P',['(','E',')']],
                     ['P',['id'       ]],
                     ['P',['num'      ]]]

        # tabela sintática
        # Linhas E M P + - * / ( ) id num $
        # Colunas +   -   *   /   (   )  id  num  $
        m = [['D','D','E','E','E','D','E','E','E'], # E
             ['R','R','D','D','E','R','E','E','R'], # M
             ['R','R','R','R','E','R','E','E','R'], # P
             ['E','E','E','E','D','E','D','D','E'], # +
             ['E','E','E','E','D','E','D','D','E'], # -
             ['E','E','E','E','D','E','D','D','E'], # *
             ['E','E','E','E','D','E','D','D','E'], # /
             ['E','E','E','E','D','E','D','D','E'], # (
             ['R','R','R','R','E','R','E','E','R'], # )
             ['R','R','R','R','E','R','E','E','R'], # id
             ['R','R','R','R','E','R','E','E','R'], # num
             ['E','E','E','E','D','E','D','D','E']] # $

        # declarando a pilha
        pilha = []

        # colocando o delimitador na pilha
        pilha.append(["$", '$_DELIMITADOR'])

        # símbolos não terminais
        terminais    = ['+', '-','x', '/', '(', ')', 'id', 'num']
        no_terminais = ['E','M','P']

        # variavel aux para montagem da árvore
        cont_identificador = 0
        nodos_filhos = [] # pilha que guarda os identificadores
        identificador_parente = 0
        self.tree.create_node('root', 0)

        # receberá as produções
        prod = ''

        for i in sentenca_copy:

            # Escolha da coluna
            c = self.escolher_coluna(i)
            if(c == -1):
                print("Erro: '{}' na entrada nao eh um terminal valido".format(i))
                return False

            while(1):
                if(self.is_concluded(i, pilha, simbolo_sentencial)):
                    return True

                # pilha[-1] == topo da pilha
                # Escolha da linha
                l = self.escolher_linha(pilha[-1])
                if(l == -1): 
                    print("Erro: entrada nao reconhecida, -> '{}'".format(pilha[-1]))
                    return False

                # escolhendo a produção a ser aplicada pela tabela sintatica
                n_prod = m[l][c]
                
                # o símbolo no início da sentença é removido, inserido no topo da pilha e passa para o próximo símbolo
                if(n_prod == 'D'): 
                    pilha.append(i)
                    cont_identificador += 1
                    self.tree.create_node(str(i), cont_identificador, parent=0, data=i)
                    self.tree.show(key=lambda x : x.identifier)
                    nodos_filhos.append(cont_identificador)
                    break # passa para o próximo símbolo

                # todos os símbolos no topo da pilha que combinam com o lado direito da produção são removidos da pilha e substituídos pelo símbolo do lado esquerdo, que é empilhado.
                elif(n_prod == 'R'):
                    # busca produção que combine com a pilha
                    prod_index = self.combina_prod(pilha, producoes)

                    if prod_index == -1:
                        print("Erro: Não existe produção que combine com os dados na pilha")
                        return False
                    prod = producoes[prod_index]

                    # adiciona o lado esquerdo da produção
                    cont_identificador += 1
                    self.tree.create_node([prod[0], 'STATE'], cont_identificador, parent=0, data=[prod[0], 'STATE'])
                    self.tree.show(key=lambda x : x.identifier, idhidden=False)
                    identificador_parente = cont_identificador

                    # analisa da esquerda para a direita
                    for iterator in prod[1][::-1]:
                        # move os nodos do lado direito da produção para serem filhos do nodo da produção a esquerda
                        self.tree.move_node(nodos_filhos[-1], identificador_parente)
                        nodos_filhos.pop()
                        self.tree.show(key=lambda x : x.identifier, idhidden=False)
                    nodos_filhos.append(identificador_parente)
                    # desempilha a quantidade de símbolos que existem no lado direito da produção
                    for cont in range(len(prod[1])): pilha.pop()
                    # empilha o lado esquerdo
                    pilha.append([prod[0], 'STATE']) 

                else:
                    print("Erro: Tabela sintática não reconhece a gramática, célula[{0}][{1}] da tabela sintática está vazia".format(pilha[-1], i[0]))
                    return False

    def analyse_sentence(self, sentence):
        if (self.verifica_atribuicao(sentence)):
            return True
        else:
            return False
