from WeakPrecedenceAnalyzer import WeakPrecedenceAnalyzer
from LexicalAnalyser import LexicalAnalyser

if __name__ == "__main__":
    print("|----> Digite a sentenca para reconhecimento:")
    sentenca = input()

    # resposta do autômato
    lex_analyser = LexicalAnalyser()
    lex_analyser.read_code(sentenca)
    tabela_lexica = lex_analyser.get_table()

    weak_analyser = WeakPrecedenceAnalyzer()
    res = weak_analyser.analyse_sentence(tabela_lexica)

    if res == True:
        print("|----> O automato reconheceu a sentenca")
    else:
        print("|----> O automato NAO reconheceu a sentenca ")

    weak_analyser.tree.show(key=lambda x : x.identifier)