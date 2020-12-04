from treelib import *

def combina_prod(pilha, producoes):
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
            if(prod[1][cont2] != pilha[cont2]): # percorre da direita para esquerda
                combina = False
                break
        if(combina):
            return cont1
    return -1

def automatoM(sentenca):
    """
    E -> E+M
    E -> M
    M -> MxP
    M -> P
    P -> (E)
    P -> v
    """

    # delimitador
    sentenca += "$"
    simbolo_sentencial = 'E'

    # tabela sintática
    # Linhas E M P + x ( ) v $
    # Colunas +   x   (   )   v   $
    m =    [['D','E','E','D','E','E'],
            ['R','D','E','R','E','R'],
            ['R','R','E','R','E','R'],
            ['E','E','D','E','D','E'],
            ['E','E','D','E','D','E'],
            ['E','E','D','E','D','E'],
            ['R','R','E','R','E','R'],
            ['R','R','E','R','E','R'],
            ['E','E','D','E','D','E']]

    # declarando a pilha
    pilha = []

    # colocando o delimitador na pilha
    pilha.append("$")

    # produções
    producoes = [['E','E+M'],
                 ['E','M'  ],
                 ['M','MxP'],
                 ['M','P'  ],
                 ['P','(E)'],
                 ['P','v'  ]]

    # símbolos não terminais
    terminais    = ['+', 'x', '(', ')', 'v']
    no_terminais = ['E','M','P']

    # variavel aux para montagem da árvore
    cont_identificador = 0
    nodos_filhos = [] # pilha que guarda os identificadores
    identificador_parente = 0
    tree.create_node('root', 0)
    # variaveis para indexação na matriz
    c = 0
    l = 0
    i = 0

    # receberá as produções
    prod = ''

    for i in sentenca:

        # Escolha da coluna
        if   i == '+':
            c = 0
        elif i == 'x':
            c = 1
        elif i == '(':
            c = 2
        elif i == ')':
            c = 3
        elif i == 'v':
            c = 4
        elif i == '$':
            c = 5
        else:
            print("Erro: '{}' na entrada nao eh um terminal valido".format(i))
            return False

        while(1):
            if(i == '$' and pilha == ['$', simbolo_sentencial]):
                return True
            # pilha[-1] == topo da pilha
            # Escolha da linha
            if pilha[-1] == 'E': 
                l = 0
            elif pilha[-1] == 'M': 
                l = 1
            elif pilha[-1] == 'P':
                l = 2
            elif pilha[-1] == '+': 
                l = 3
            elif pilha[-1] == 'x':
                l = 4
            elif pilha[-1] == '(': 
                l = 5
            elif pilha[-1] == ')':
                l = 6
            elif pilha[-1] == 'v': 
                l = 7
            elif pilha[-1] == '$':
                l = 8
            else:
                print("Erro: entrada nao reconhecida, -> '{}'".format(pilha[-1]))
                return False

            # escolhendo a produção a ser aplicada pela tabela sintatica
            n_prod = m[l][c]
            
            # o símbolo no início da sentença é removido, inserido no topo da pilha e passa para o próximo símbolo
            if(n_prod == 'D'): 
                pilha.append(i)
                cont_identificador += 1
                tree.create_node(i, cont_identificador, parent=0)
                # tree.show(key=lambda x : x.identifier)
                nodos_filhos.append(cont_identificador)
                break # passa para o próximo símbolo

            # todos os símbolos no topo da pilha que combinam com o lado direito da produção são removidos da pilha e substituídos pelo símbolo do lado esquerdo, que é empilhado.
            elif(n_prod == 'R'):
                # busca produção que combine com a pilha
                prod_index = combina_prod(pilha, producoes)

                if prod_index == -1:
                    print("Erro: Não existe produção que combine com os dados na pilha")
                    return False
                prod = producoes[prod_index]

                # adiciona o lado esquerdo da produção
                cont_identificador += 1
                tree.create_node(prod[0], cont_identificador, parent=0)
                # tree.show(key=lambda x : x.identifier, idhidden=False)
                identificador_parente = cont_identificador

                # analisa da esquerda para a direita
                for iterator in prod[1][::-1]:
                    # move os nodos do lado direito da produção para serem filhos do nodo da produção a esquerda
                    tree.move_node(nodos_filhos[-1], identificador_parente)
                    nodos_filhos.pop()
                    # tree.show(key=lambda x : x.identifier, idhidden=False)
                nodos_filhos.append(identificador_parente)
                # desempilha a quantidade de símbolos que existem no lado direito da produção
                for cont in range(len(prod[1])): pilha.pop()
                # empilha o lado esquerdo
                pilha.append(prod[0]) 

            else:
                print("Erro: Tabela sintática não reconhece a gramática, célula[{0}][{1}] da tabela sintática está vazia".format(pilha[-1], i))
                return False


if __name__ == "__main__":
    # arvore sintática que ira armazenar as produções
    tree = Tree()

    print("|----> Digite a sentenca para reconhecimento:")
    sentenca = input()

    # resposta do autômato
    res = automatoM(sentenca)

    if res == True:
        print("|----> O automato reconheceu a sentenca")
    else:
        print("|----> O automato NAO reconheceu a sentenca ")

    tree.show(key=lambda x : x.identifier)
