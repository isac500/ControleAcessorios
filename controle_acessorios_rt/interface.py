import platform
from os import system
s_cor = '\033[m'
ng = '\033[1m'
vermelho = '\033[1;31m'
azul = '\033[1;34m'
azul_c = '\033[1;36m'

def lin(tam = 60):
    return f'=' * tam


def cabeçalho(msg):
    print(lin())
    print(f'<< {msg} >>'.center(60))
    print(lin())


def menu():
    cabeçalho('Controle de Acessórios - RF - GUARULHOS SP')
    opc = ['Saída', 'Retorno', 'Consultar', 'Backup','Fechar Sistema']

    for c, i in enumerate (opc):
        print(f'  << {vermelho}{c + 1 if not c == 4 else 0}{s_cor} >> - {azul}{i}{s_cor}')
    print(lin())

def menu_consulta():

    opc = ['Buscar Por Placa Principal', 'Buscar Por Data (Saída/Retorno)', 'Buscar Por Status (Em curso/Retorno)', 'Buscar Por NOME do Condutor','Voltar Ao Menu Principal']

    for c, i in enumerate (opc):
        print(f'  << {vermelho}{c + 1 if not c == 6 else 0}{s_cor} >> - {azul}{i}{s_cor}')
    print(lin())

def limpar_tela():
    if platform.system() == 'Windows':
        system('cls')
    else:
        system('clear')


def console(*dado):
    print(lin())
    for i in dado:
        print(i)
    print(lin())


