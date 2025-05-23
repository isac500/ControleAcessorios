# database.py
import sqlite3
import json

DB_NAME = "controle_acessorios.db"

def salvar_retorno_no_banco(dados):
    # Use a chave correta 'Placa' (no singular)

    placa = dados['placa_principal']
    data_retorno = dados['Data_retorno']
    itens = dados['itens_retorno']

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obter o id_viagem com status "Em curso" para essa placa
        cursor.execute("""
            SELECT id FROM informacoes_gerais_viagem
            WHERE placa_principal = ? AND status = 'Em curso'
            ORDER BY id DESC LIMIT 1
        """, (placa,))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"❌ Nenhuma viagem em curso encontrada para a placa {placa}.")
            return

        id_viagem = resultado[0]

        # Atualizar data de retorno e status
        cursor.execute("""
            UPDATE informacoes_gerais_viagem
            SET data_hora_retorno = ?, status = 'Retornado'
            WHERE id = ?
        """, (data_retorno, id_viagem))

        # Inserir itens de retorno na tabela itens_retorno
        cursor.execute("""
            INSERT INTO itens_retorno (
                id_viagem, varoes, calcos, rede, madeirite,
                cadeado, travas, lonado, carrinho
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_viagem,
            itens.get('varoes', 0),
            itens.get('calco', 0),
            itens.get('rede', 0),
            itens.get('madeirite', 0),
            itens.get('cadeado', 0),
            itens.get('travas', 0),
            itens.get('lonado', 0),
            itens.get('carrinho', 0)
        ))

        conn.commit()
        conn.close()
        print("✅ Retorno registrado com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao registrar retorno: {e}")


import sqlite3

DB_NAME = 'controle_acessorios.db'

def salvar_saida_no_banco(dados):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Inserir na tabela informacoes_gerais_viagem
    cursor.execute("""
        INSERT INTO informacoes_gerais_viagem (
            data_hora_saida, placa_principal, placa_1, placa_2,
            motorista, operacao, rota, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados['Data_saida'],
        dados['Placas'][0],
        dados['Placas'][1] if len(dados['Placas']) > 1 else None,
        dados['Placas'][2] if len(dados['Placas']) > 2 else None,
        dados['Motorista'],
        dados['Operação'],
        dados['Rota'],
        'Em curso'
    ))

    id_viagem = cursor.lastrowid

    # Pega os itens corretamente (usando a chave 'itens_saida')
    itens = dados.get('itens_saida', {})

    cursor.execute("""
        INSERT INTO itens_saida (
            id_viagem, varoes, calcos, rede, madeirite,
            cadeado, travas, lonado, carrinho
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_viagem,
        itens.get('varoes', 0),
        itens.get('calco', 0),
        itens.get('rede', 0),
        itens.get('madeirite', 0),
        itens.get('cadeado', 0),
        itens.get('travas', 0),
        itens.get('lonado', 0),
        itens.get('carrinho', 0)
    ))

    conn.commit()
    conn.close()
    print("✅ Saída registrada com sucesso no banco de dados!")