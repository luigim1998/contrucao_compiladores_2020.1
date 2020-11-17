from treelib import *

def automatoM(sentenca):
    """
    E -> MF
    F -> +MF
    F -> &
    M -> PN
    N -> xPN
    N -> &
    P -> (E)
    P -> v
    """

    # delimitador
    sentenca += "$"

    # tabela sintática
    m = [[9, 9, 1, 9, 1, 9],
         [2, 9, 9, 3, 9, 3],
         [9, 9, 4, 9, 4, 9],
         [6, 5, 9, 6, 9, 6],
         [9, 9, 7, 9, 8, 9]]

    # declarando a pilha
    pilha = []

    # colocando o delimitador na pilha
    pilha.append("$")

    # colocando o simbolo sentencial na pilha
    pilha.append("E")

    # símbolos não terminais
    terminais = ['v', '+', '*', '(', ')', '&']
    no_terminais = ['E', 'F', 'M', 'N', 'P']

    # colocando o simbolo sentencial como raiz da arvore
    tree.create_node("E", 0)

    # variavel aux para montagem da árvore
    cont_producao = 0
    cont_identificador = 0
    mais_a_esquerda = [0]  # pilha de não-terminais
    parente = 'E'  # símbolo sentencial
    identificador_parente = 0
    # variaveis para indexação na matriz
    c = 0
    l = 0
    i = 0

    # receberá as produções
    prod = ''

    for i in sentenca:

        if i == '+':
            c = 0
        elif i == '*':
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
            return False

        while(1):
            # pilha[-1] == topo da pilha
            if pilha[-1] == 'E':
                l = 0
            elif pilha[-1] == 'F':
                l = 1
            elif pilha[-1] == 'M':
                l = 2
            elif pilha[-1] == 'N':
                l = 3
            elif pilha[-1] == 'P':
                l = 4
            else:
                return False

			# escolhendo a produção a ser aplicada pela tabela sintatica
            n_prod = m[l][c]

			# fazendo equivalência entre a produção e ordem inversa e o seu número da tabela
            if n_prod == 1:
                prod = "MF"
            elif n_prod == 2:
                prod = "+MF"
            elif n_prod == 3:
                prod = "&"
            elif n_prod == 4:
                prod = "PN"
            elif n_prod == 5:
                prod = "*PN"
            elif n_prod == 6:
                prod = "&"
            elif n_prod == 7:
                prod = "(E)"
            elif n_prod == 8:
                prod = "v"
            else:
                return False

			# aplicando a produção que leva para a string vazia
            if prod[0] == '&':
                pilha.pop()
            # aplicando outros tipos de produções
            else:
                pilha.pop()
                for j in prod[::-1]:  # insere da direita a esquerda
                    pilha.append(j)

			# Adicionar produção na árvore sintática

            for iterator in prod[::-1]:  # analisa da esquerda para a direita
                cont_identificador += 1
                cont_producao += 1
                tree.create_node(iterator, cont_identificador,
                                 parent=identificador_parente)

                if iterator not in terminais:
                    # insere o não-terminal na pilha
                    mais_a_esquerda.insert(0, cont_identificador)

                if cont_producao == len(prod):
                    # remove o nodo parente porque não tem mias filhos para inserir na árvore
                    mais_a_esquerda.remove(identificador_parente)
                    cont_producao = 0

                    # quando a pilha mais_a_esquerda está vazia
                    if(len(mais_a_esquerda) == 0): break

                    # obter símbolo do próximo não-terminal a ser analisado
                    parente = tree.get_node(mais_a_esquerda[0]).tag
                    # obter identificador do próximo não-terminal a ser analisado
                    identificador_parente = mais_a_esquerda[0]
                tree.show()

			# verificando se há igualdade no topo da pilha e o caractere em analise
            if pilha[-1] == i:
                # reconhecimento da sentença
                if pilha[-1] == '$':
                    return True
                # mudança de estado do automato
                else:
                    pilha.pop()
                    break


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
