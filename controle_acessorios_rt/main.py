from operadores import *
from  interface import *
from database import *
from init_db import criar_banco_de_dados


s_cor = '\033[m'
ng = '\033[1m'
vermelho = '\033[1;31m'
azul = '\033[1;34m'
azul_c = '\033[1;36m'


limpar_tela()
criar_banco_de_dados()
menu()

while True:
    res = leiaint('Opção: ')
    while res < 0 or res > 4:
        print(f'{vermelho}Opcão inválida. Tente novamente!{s_cor}')
        res = leiaint('Opção: ')
    if res == 1:
        limpar_tela()
        cabeçalho('Registro de Saída')
        while True:
            dados_saida = ler_dados_saida()
            if dados_saida:
                limpar_tela()
                cabeçalho('Registro de Saída')
                exibir_dados_saida(dados_saida)
                print(lin())
                print('Atenção! Deseja confirmar esse registro de saída?')
                print(f' << {vermelho}1{s_cor} >> - {azul}CONFIRMAR SAÍDA{s_cor}\n << {vermelho}2{s_cor} >> - {azul}REFAZER REGISTRO DE SAÍDA{s_cor}\n << {vermelho}3{s_cor} >> - {azul}CANCELAR SAÍDA{s_cor}')
                print(lin())
                while True:
                    confirmar_dados = leiaint('Digite: ')
                    if confirmar_dados in [1, 2, 3]:
                        break
                    print(f'{vermelho}Opção inválida! Tente novamente{s_cor}')

                if confirmar_dados == 1:
                    salvar_saida_no_banco(dados_saida)
                    limpar_tela()
                    menu()
                    console('✅ Registro de SAÍDA salvo com sucesso!')
                    break
                elif confirmar_dados == 2:
                    limpar_tela()
                    cabeçalho('Registro de Saída')
                else:
                    limpar_tela()
                    menu()
                    console('Registro de SAÍDA cancelado.')
                    break
            else:
                limpar_tela()
                menu()
                console('Registro de saída cancelado ou inválido.')
                break

    elif res == 2:
        limpar_tela()
        cabeçalho('Registro de Retorno')
        while True:
            dados_retorno = ler_dados_retorno()
            if dados_retorno:
                limpar_tela()
                cabeçalho('Registro de Retorno')
                exibir_dados_retorno(dados_retorno)
                print('Atenção! Deseja confirmar esse registro de saída?')
                print(f' << {vermelho}1{s_cor} >> - {azul}CONFIRMAR SAÍDA{s_cor}\n << {vermelho}2{s_cor} >> - {azul}REFAZER REGISTRO DE SAÍDA{s_cor}\n << {vermelho}3{s_cor} >> - {azul}CANCELAR SAÍDA{s_cor}')
                print(lin())
                while True:
                    confirmar_dados = leiaint('Digite: ')
                    if confirmar_dados in [1, 2, 3]:
                        break
                    print(f'{vermelho}Opção inválida! Tente novamente{s_cor}')

                if confirmar_dados == 1:
                    salvar_retorno_no_banco(dados_retorno)
                    limpar_tela()
                    menu()
                    console('✅ Registro de RETORNO salvo com sucesso!')
                    break
                elif confirmar_dados == 2:
                    limpar_tela()
                    cabeçalho('Registro de Retorno')
                else:
                    limpar_tela()
                    menu()
                    console('Registro de RETORNO cancelado')
            else:
                limpar_tela()
                menu()
                console('❌ Veículo não está em viagem ou placa inválida.')
                break
    elif res == 3:
        limpar_tela()
        cabeçalho('Consultar')
        menu_consulta()
        while True:
            res_consulta = leiaint('Opção: ')
            while res_consulta < 1 or res_consulta > 5:
                print(f'{vermelho}Opção inválida! Tente novamente.{s_cor}')
                res_consulta = leiaint('Opção: ')
            if res_consulta == 1:
                cabeçalho('Busca Por Placa Principal')
                buscar_por_placa()
            elif res_consulta == 2:
                cabeçalho('Buscar Por Data')
                buscar_por_data()
            elif  res_consulta == 3:
                cabeçalho('Buscar Por Status')
                buscar_por_status()
            elif res_consulta == 4:
                cabeçalho('Buscar por Condutor')
                buscar_por_motorista()
            else:
                limpar_tela()
                menu()
                break
    elif res == 4:
        limpar_tela()
        menu()
        console('Opção indisponíel no momento! ')

    elif res == 0:
        cabeçalho('Encerrado!')
        break