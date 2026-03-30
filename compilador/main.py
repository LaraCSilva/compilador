from analisadorLexico import analisador

with open('codigo_fonte.txt', 'r') as arq:
    codigo_fonte = arq.read()
    analisador(codigo_fonte)