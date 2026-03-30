import re

#Cria uma classe token para guardar todas as informações do token
class Token:
    def __init__(self, id, lexema, classe, linha, coluna):
        self.id =id
        self.lexema = lexema
        self.classe = classe
        self.linha = linha
        self.coluna = coluna
    
    def printaToken(self):
        print(f'| {self.id:<4} | {self.lexema:<15} | {self.classe:<18} | {self.linha:<6} | {self.coluna:<6} |')

def analisador(codigo_fonte):
    #Variáveis
    lista_tokens = []
    comeco_linha = 0
    linha_atual = 1
    id = 0
    
    #Organiza as classes e seus padrões dentro de uma lista para ficar melhor de vizualisar e mudar
    lista_padroes = [('COMENTARIO', r'/\*[\s\S]*?\*/|//.*'),
                     ('PALAVRA_RESERVADA', r'\b(int|for|if|bool|string|float)\b'), 
                     ('SEPARADOR', r'\(|\)|\{|\}|;'), 
                     ('OPERADOR', r'\+\+|--|/|\*|\+|-|<=|>=|==|!=|<|>|=|&&|\|\|'),
                     ('NUMERO', r'[0-9]+(\.[0-9]+)?'),
                     ('IDENTIFICADOR', r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*'),
                     ('LITERAL', r'"(?:[^"\\]|\\.)*"'),
                     ('ESPACO', r'[ \t]+'),
                     ('QUEBRA_LINHA', r'\n'),
                     ('ERRO', r'.')]
    
    #Cria a Regex a partir da lista
    regex = '|'.join(f'(?P<{nome}>{padrao})'for nome, padrao in lista_padroes)
    regex = re.compile(regex)
    
    #Passa por todo o texto identificando os tokens e os erros e colocando tudo em uma lista de tokens
    for match in regex.finditer(codigo_fonte):
        lexema = match.group()
        classe = match.lastgroup
        posicao = match.start()
        coluna = posicao - comeco_linha + 1
        
        if classe == 'ESPACO':
            continue
        elif classe == 'QUEBRA_LINHA':
            linha_atual += 1
            comeco_linha = match.end()
        elif classe == 'ERRO':
            print(f"Erro Léxico: Caractere inválido '{lexema}' na linha: {linha_atual} e coluna: {coluna}")
        elif classe == 'COMENTARIO':
            linha_atual += lexema.count('\n')
            if'\n' in lexema:
                comeco_linha = posicao + lexema.rfind('\n') + 1
        else:
            novo_token = Token(id, lexema, classe, linha_atual, coluna)
            lista_tokens.append(novo_token)
            id += 1
    
    #Printa a tabela de tokens
    print("\n" + "-"*70)
    print(f"| {'ID':<4} | {'LEXEMA':<15} | {'CLASSE':<18} | {'LINHA':<6} | {'COLUNA':<6} |")
    print("-"*70)
    
    for t in lista_tokens:
        t.printaToken()
        
    return lista_tokens