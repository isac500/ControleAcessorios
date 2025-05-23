import os
import sqlite3

def criar_banco_de_dados():
    if not os.path.exists('controle_acessorios.db'):
        print("Banco de dados não encontrado. Criando novo banco...")
        conexao = sqlite3.connect('controle_acessorios.db')
        cursor = conexao.cursor()

        # Tabela principal
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS informacoes_gerais_viagem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora_saida TEXT NOT NULL,
                placa_principal TEXT NOT NULL,
                placa_1 TEXT,
                placa_2 TEXT,
                motorista TEXT NOT NULL,
                operacao TEXT NOT NULL,
                rota TEXT NOT NULL,
                status TEXT NOT NULL,
                data_hora_retorno TEXT
            );
        ''')

        # Itens de saída
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_saida (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_viagem INTEGER NOT NULL,
                varoes INTEGER,
                calcos INTEGER,
                rede INTEGER,
                madeirite INTEGER,
                cadeado INTEGER,
                travas INTEGER,
                lonado INTEGER,
                carrinho INTEGER,
                FOREIGN KEY(id_viagem) REFERENCES informacoes_gerais_viagem(id)
            );
        ''')

        # Itens de retorno
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_retorno (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_viagem INTEGER NOT NULL,
                varoes INTEGER,
                calcos INTEGER,
                rede INTEGER,
                madeirite INTEGER,
                cadeado INTEGER,
                travas INTEGER,
                lonado INTEGER,
                carrinho INTEGER,
                FOREIGN KEY(id_viagem) REFERENCES informacoes_gerais_viagem(id)
            );
        ''')

        conexao.commit()
        conexao.close()
        print("Banco de dados criado com sucesso.")


