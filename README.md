# Sistema de Controle de Acessórios

Este sistema foi pensado e desenvolvido sob demanda da empresa de logistica, Rota Freitas, com o objetivo de gerenciar de forma eficiente a saída e retorno de acessórios utilizados em viagens de transporte. Desenvolvido em Python, o softwere conta com opções de saída e retorno de acessórios utilizados em viagens de transporte, com registro automatizado e consulta dinâmica dos dados. O sistema foi criado para otimizar o fluxo de controle de itens, garantindo precisão, histórico e comparações entre saída e retorno.


📋 Funcionalidades

✅ Registro de Saída:

Cadastro de informações principais (placa, motorista, operação, rota).

Registro de acessórios enviados.

Data de saída registrada automaticamente.

✅ Registro de Retorno:

Atualização do status da viagem para "Retornado".

Registro dos acessórios devolvidos.

Data de retorno registrada automaticamente.

✅ Consulta:

Pesquisa detalhada por placa, motorista, data ou status da viagem.

Comparação visual dos itens enviados e devolvidos, destacando possíveis divergências.

✅ Backup:

Opção presente no menu, mas indisponível nesta versão ("Opção indisponível no momento").

✅ Encerramento:

Finaliza a execução do sistema com segurança.

🗄️ Estrutura do Banco de Dados
O sistema utiliza um banco de dados SQLite com três tabelas principais:

informacoes_gerais_viagem:
Armazena dados da viagem (placa, motorista, operação, rota, status, data de saída e retorno).

itens_saida:
Armazena o detalhamento dos acessórios enviados na saída.

itens_retorno:
Armazena o detalhamento dos acessórios devolvidos no retorno.

Este modelo permite:

Histórico completo das operações.

Comparação entre itens enviados e devolvidos, identificando perdas ou divergências.

🖥️ Tecnologias Utilizadas
Python 3.12

SQLite (banco de dados local)

PyInstaller (para geração do executável)


