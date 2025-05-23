from interface import *
from re import match
from datetime import datetime
import sqlite3

DB_NAME = "controle_acessorios.db"

s_cor = '\033[m'
ng = '\033[1m'
vermelho = '\033[1;31m'
azul = '\033[1;34m'
azul_c = '\033[1;36m'

def leiaint(msg):
    while True:
        try:
            num = input(msg)
            if num == '':
                num = 0
            num = int(num)
        except:
            print(f'{vermelho}Erro! Digite um número válido{s_cor}')
        else:
            return num

def leiaplaca_opcional(msg):
    while True:
        antigo = r'[A-Z]{3}[0-9]{4}$'
        novo = r'[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$'
        plc = str(input(msg)).upper().strip().replace(' ', '').replace('-', '')
        if plc == '':
            return '----'
        if match(antigo, plc) or match(novo, plc):
            return plc
        else:
            print(f'{vermelho}Formato de placa inválido. Tente novamente.{s_cor}')

def leiaplaca(msg):
    while True:
        antigo = r'[A-Z]{3}[0-9]{4}$'
        novo = r'[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$'
        plc = str(input(msg)).upper().strip().replace(' ', '').replace('-', '')
        if match(antigo, plc) or match(novo, plc):
            return plc
        else:
            print(f'{vermelho}Formato de placa inválido. Tente novamente.{s_cor}')

def verificar_saida_permitida(placa_principal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status FROM informacoes_gerais_viagem
        WHERE placa_principal = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (placa_principal,))
    resultado = cursor.fetchone()
    conn.close()
    return not resultado or resultado[0] == 'Retornado'

def verificar_retorno_permitido(placa_principal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM informacoes_gerais_viagem
        WHERE placa_principal = ? AND status = "Em curso"
        ORDER BY id DESC
        LIMIT 1
    ''', (placa_principal,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def ler_dados_saida():
    motorista = str(input('Nome do motorista: ')).strip().capitalize()
    if motorista == '':
        return None
    data = datetime.now().strftime('%d/%m/%Y %H:%M')
    operacao = str(input('Operação: ')).strip()
    rota = str(input('Rota: ')).strip()
    placa1 = leiaplaca('Placa 1 (obrigatória): ')
    if verificar_retorno_permitido(placa1):
        print('\n❌ Este veículo já está em viagem.\n')
        return None
    placa2 = leiaplaca_opcional('Placa 2 (opcional): ')
    placa3 = leiaplaca_opcional('Placa 3 (opcional): ')
    itens_saida = {
        'varoes': leiaint('Varoes: '),
        'calco': leiaint('Calço: '),
        'rede': leiaint('Rede: '),
        'madeirite': leiaint('Madeirite: '),
        'cadeado': leiaint('Cadeado: '),
        'travas': leiaint('Travas: '),
        'lonado': leiaint('Lonado: '),
        'carrinho': leiaint('Carrinho: ')
    }
    return {
        'Data_saida': data,
        'Motorista': motorista,
        'Operação': operacao,
        'Rota': rota,
        'Placas': [placa1, placa2, placa3],
        'itens_saida': itens_saida
    }

def exibir_dados_saida(dados):
    print(lin())
    print(f'{ng}Dados da saída{s_cor}')
    print(f"Data       : {dados['Data_saida']}")
    print(f"Motorista  : {dados['Motorista']}")
    print(f"Operação   : {dados['Operação']}")
    print(f"Rota       : {dados['Rota']}")
    print(f"Placas     : {', '.join(dados['Placas'])}")
    print(f'{ng}Itens Saída{s_cor}')
    for item, qtd in dados['itens_saida'].items():
        print(f"  {item.capitalize():<10}: {qtd}")

def ler_dados_retorno():
    placa = leiaplaca('Placa do veículo retornando: ')
    if not verificar_retorno_permitido(placa):
        return None
    data = datetime.now().strftime('%d/%m/%Y %H:%M')
    itens_retorno = {
        'varoes': leiaint('Varoes: '),
        'calco': leiaint('Calço: '),
        'rede': leiaint('Rede: '),
        'madeirite': leiaint('Madeirite: '),
        'cadeado': leiaint('Cadeado: '),
        'travas': leiaint('Travas: '),
        'lonado': leiaint('Lonado: '),
        'carrinho': leiaint('Carrinho: ')
    }
    return {
        'Data_retorno': data,
        'placa_principal': placa,
        'itens_retorno': itens_retorno
    }

def exibir_dados_retorno(dados):
    print(lin())
    print('Dados do retorno:')
    print(f"Data Retorno : {dados['Data_retorno']}")
    print(f"Placa        : {dados['placa_principal']}")
    print('Itens Retorno:')
    for item, qtd in dados['itens_retorno'].items():
        print(f"  {item.capitalize():<10}: {qtd}")

def verificar_status_placa(placa):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status FROM informacoes_gerais_viagem
        WHERE placa_principal = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (placa.upper(),))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        print(f"Status   : {resultado[0]}")
        return resultado[0]
    else:
        print(f"\n>> Nenhum registro encontrado para a placa {placa.upper()}.")
        return None




def buscar_por_placa():
    placa = input("Digite a placa principal: ").upper()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    validar_pesquisa_id = True

    cursor.execute("""
        SELECT * FROM informacoes_gerais_viagem WHERE placa_principal = ?
    """, (placa,))
    registros = cursor.fetchall()
    limpar_tela()
    if registros:
        # Cabeçalho
        print("=" * 120)
        print(f"{'ID':<4} | {'Saída':<16} | {'Placa Principal':<14} | {'Placa 1':<10} | {'Placa 2':<10} | "
              f"{'Motorista':<15} | {'Operação':<15} | {'Rota':<6} | {'Status':<10} | {'Retorno':<16}")
        print("=" * 120)

        # Conteúdo
        for r in registros:
            id, data_saida, placa_principal, placa_1, placa_2, motorista, operacao, rota, status, data_retorno = r
            print(
                f"{id:<4} | {data_saida:<16} | {placa_principal:<14} | {placa_1 or '----':<10} | {placa_2 or '----':<10} | "
                f"{motorista:<15} | {operacao:<15} | {rota:<6} | {status:<10} | {data_retorno or '----':<16}")
        print("=" * 120)

    else:
        cabeçalho('Consultar')
        menu_consulta()
        console("❌ Nenhum registro encontrado com essa placa.")
        validar_pesquisa_id = False
    if validar_pesquisa_id:
        while True:
            print(f'  << {vermelho}1{s_cor} >> - {azul}Ver Detalhes - Itens de Viagem{s_cor} ')
            print(f'  << {vermelho}2{s_cor} >> - {azul}Voltar{s_cor} ')
            ler = leiaint('Opção: ')
            if ler == 1:
                try:
                    id = leiaint('Digite o ID da viagem: ')
                    exibir_detalhes_viagem(id)
                except:
                    print('Viagem não encontrada')
            elif ler == 2:
                limpar_tela()
                cabeçalho('Consultar')
                menu_consulta()
                break
            else:
                print(f'{vermelho}Opção inválida!{s_cor}')
    conn.close()


def buscar_por_data():
    print("Buscar por:")
    print(f"  << {vermelho}1{s_cor} >> - {azul}Data de saída{s_cor}")
    print(f"  << {vermelho}2{s_cor} >> - {azul}Data de retorno{s_cor}")
    opcao = input("Opção: ")
    while opcao != '1' and opcao != '2':
        print(f'{vermelho}Opção inválida. Tente Novamente!{s_cor}')
        opcao = input('Opção: ')
    

    data = input("Digite a data (ex: 15/05/2025): ")

    campo = 'data_hora_saida' if opcao == '1' else 'data_hora_retorno'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM informacoes_gerais_viagem
        WHERE {campo} LIKE ?
    """, (f"%{data}%",))
    registros = cursor.fetchall()
    validar_consulta = True
    limpar_tela()
    if registros:
        # Cabeçalho
        print("=" * 120)
        print(f"{'ID':<4} | {'Saída':<16} | {'Placa Principal':<14} | {'Placa 1':<10} | {'Placa 2':<10} | "
              f"{'Motorista':<15} | {'Operação':<15} | {'Rota':<6} | {'Status':<10} | {'Retorno':<16}")
        print("=" * 120)

        # Conteúdo
        for r in registros:
            id, data_saida, placa_principal, placa_1, placa_2, motorista, operacao, rota, status, data_retorno = r
            print(
                f"{id:<4} | {data_saida:<16} | {placa_principal:<14} | {placa_1 or '----':<10} | {placa_2 or '----':<10} | "
                f"{motorista:<15} | {operacao:<15} | {rota:<6} | {status:<10} | {data_retorno or '----':<16}")
        print("=" * 120)
    else:
        validar_consulta = False
        limpar_tela()
        cabeçalho('Consultar')
        menu_consulta()
        console("❌ Nenhum registro encontrado com essa data.")
    if validar_consulta:
        while True:
            print(f'  << {vermelho}1{s_cor} >> - {azul}Ver Detalhes - Itens de Viagem{s_cor} ')
            print(f'  << {vermelho}2{s_cor} >> - {azul}Voltar{s_cor} ')
            ler = leiaint('Opção: ')
            if ler == 1:
                try:
                    id = leiaint('Digite o ID da viagem: ')
                    exibir_detalhes_viagem(id)
                except:
                    print('Viagem não encontrada')
            elif ler == 2:
                limpar_tela()
                cabeçalho('Consultar')
                menu_consulta()
                break
            else:
                print(f'{vermelho}Opção inválida!{s_cor}')
    conn.close()


def buscar_por_status():
    print(f'  << {vermelho}1{s_cor} >> - {azul}Status: Em curso{s_cor}')
    print(f'  << {vermelho}2{s_cor} >> - {azul}Status: Retornado{s_cor}')

    while True:
        status = leiaint("Opção: ")
        if status == 1:
            status = 'Em curso'
            break
        elif status == 2:
            status = 'Retornado'
            break
        else:
            print(f'{vermelho}Opção Inválida. Tente Novamente!{s_cor}')

    if status not in ['Em curso', 'Retornado']:
        print("❌ Status inválido.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM informacoes_gerais_viagem WHERE status = ?
    """, (status,))
    registros = cursor.fetchall()
    validar_consulta = True
    limpar_tela()
    if registros:
        # Cabeçalho
        print("=" * 120)
        print(f"{'ID':<4} | {'Saída':<16} | {'Placa Principal':<14} | {'Placa 1':<10} | {'Placa 2':<10} | "
              f"{'Motorista':<15} | {'Operação':<15} | {'Rota':<6} | {'Status':<10} | {'Retorno':<16}")
        print("=" * 120)

        # Conteúdo
        for r in registros:
            id, data_saida, placa_principal, placa_1, placa_2, motorista, operacao, rota, status, data_retorno = r
            print(
                f"{id:<4} | {data_saida:<16} | {placa_principal:<14} | {placa_1 or '----':<10} | {placa_2 or '----':<10} | "
                f"{motorista:<15} | {operacao:<15} | {rota:<6} | {status:<10} | {data_retorno or '----':<16}")
        print("=" * 120)
    else:
        validar_consulta = False
        limpar_tela()
        cabeçalho('Consultar')
        menu_consulta()
        console("❌ Nenhum registro encontrado com esse status.")
    if validar_consulta:
        while True:
            print(f'  << {vermelho}1{s_cor} >> - {azul}Ver Detalhes - Itens de Viagem{s_cor} ')
            print(f'  << {vermelho}2{s_cor} >> - {azul}Voltar{s_cor} ')
            ler = leiaint('Opção: ')
            if ler == 1:
                try:
                    id = leiaint('Digite o ID da viagem: ')
                    exibir_detalhes_viagem(id)
                except:
                    print('Viagem não encontrada')
            elif ler == 2:
                limpar_tela()
                cabeçalho('Consultar')
                menu_consulta()
                break
            else:
                print(f'{vermelho}Opção inválida!{s_cor}')
    conn.close()


def buscar_por_motorista():
    nome = input("Digite o nome (ou parte do nome) do motorista: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM informacoes_gerais_viagem
        WHERE motorista LIKE ?
    """, (f"%{nome}%",))
    registros = cursor.fetchall()
    validar_consulta = True
    limpar_tela()
    if registros:
        # Cabeçalho
        print("=" * 120)
        print(f"{'ID':<4} | {'Saída':<16} | {'Placa Principal':<14} | {'Placa 1':<10} | {'Placa 2':<10} | "
              f"{'Motorista':<15} | {'Operação':<15} | {'Rota':<6} | {'Status':<10} | {'Retorno':<16}")
        print("=" * 120)

        # Conteúdo
        for r in registros:
            id, data_saida, placa_principal, placa_1, placa_2, motorista, operacao, rota, status, data_retorno = r
            print(
                f"{id:<4} | {data_saida:<16} | {placa_principal:<14} | {placa_1 or '----':<10} | {placa_2 or '----':<10} | "
                f"{motorista:<15} | {operacao:<15} | {rota:<6} | {status:<10} | {data_retorno or '----':<16}")
        print("=" * 120)
    else:
        validar_consulta = False
        limpar_tela()
        cabeçalho('Consultar')
        menu_consulta()
        console("❌ Nenhum motorista encontrado com esse nome.")
    if validar_consulta:
        while True:
            print(f'  << {vermelho}1{s_cor} >> - {azul}Ver Detalhes - Itens de Viagem{s_cor} ')
            print(f'  << {vermelho}2{s_cor} >> - {azul}Voltar{s_cor} ')
            ler = leiaint('Opção: ')
            if ler == 1:
                try:
                    id = leiaint('Digite o ID da viagem: ')
                    exibir_detalhes_viagem(id)
                except:
                    print('Viagem não encontrada')
            elif ler == 2:
                limpar_tela()
                cabeçalho('Consultar')
                menu_consulta()
                break
            else:
                print(f'{vermelho}Opção inválida!{s_cor}')
    conn.close()


import sqlite3

import sqlite3

DB_NAME = "controle_acessorios.db"


def exibir_detalhes_viagem(viagem_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Buscar dados principais da viagem
    cursor.execute("""
        SELECT id, placa_principal, placa_1, placa_2, operacao, rota, status,
               data_hora_saida, data_hora_retorno
        FROM informacoes_gerais_viagem
        WHERE id = ?
    """, (viagem_id,))
    dados = cursor.fetchone()

    if not dados:
        print("❌ Viagem não encontrada.")
        conn.close()
        return

    dados_viagem = {
        "id": dados[0],
        "placa_principal": dados[1],
        "placa_1": dados[2] or '----',
        "placa_2": dados[3] or '----',
        "operacao": dados[4],
        "rota": dados[5],
        "status": dados[6],
        "data_hora_saida": dados[7],
        "data_hora_retorno": dados[8] or ''
    }

    # Buscar itens de saída
    cursor.execute("""
        SELECT varoes, calcos, rede, madeirite, cadeado, travas, lonado, carrinho
        FROM itens_saida
        WHERE id_viagem = ?
    """, (viagem_id,))
    saida = cursor.fetchone()
    colunas = ['varoes', 'calcos', 'rede', 'madeirite', 'cadeado', 'travas', 'lonado', 'carrinho']
    dados_viagem['itens_saida'] = dict(zip(colunas, saida)) if saida else {}

    # Buscar itens de retorno (se houver)
    cursor.execute("""
        SELECT varoes, calcos, rede, madeirite, cadeado, travas, lonado, carrinho
        FROM itens_retorno
        WHERE id_viagem = ?
    """, (viagem_id,))
    retorno = cursor.fetchone()
    dados_viagem['itens_retorno'] = dict(zip(colunas, retorno)) if retorno else {}

    conn.close()

    # Exibição formatada
    print("\n" + "=" * 60)
    print(f"Viagem ID: {dados_viagem['id']} | Placas: {dados_viagem['placa_principal']}, "
          f"{dados_viagem['placa_1']}, {dados_viagem['placa_2']}")
    print(f"Operação: {dados_viagem['operacao']}")
    print(f"Rota: {dados_viagem['rota']}")
    print(f"Status: {dados_viagem['status']}")
    print(f"Data saída: {dados_viagem['data_hora_saida']}")

    if dados_viagem['status'] == 'Retornado':
        print(f"Data retorno: {dados_viagem['data_hora_retorno']}")

    print("\nItens:")
    print("-" * 60)

    for item in colunas:
        enviado = dados_viagem['itens_saida'].get(item, 0)
        retornado = dados_viagem['itens_retorno'].get(item, None)

        if retornado is not None:
            status = "✅" if enviado == retornado else "❌"
            obs = "" if enviado == retornado else "divergência"
            print(f"- {item:<10}: enviado = {enviado:<3} | retornado = {retornado:<3} | {status} {obs}")
        else:
            print(f"- {item:<10}: enviado = {enviado}")
    print("=" * 60 + "\n")
