# Importando a biblioteca
import sqlite3


def inicia_conexao():
    try:
        # Inciando a conexão com o banco de dados
        connection = sqlite3.connect("exercicio_estacio.db")

        # Instanciando um cursor para o banco
        cursor = connection.cursor()

        # Criando a tabela TB_PESSOA
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS TB_PESSOAS (
                    id INTEGER PRIMARY KEY,
                    nome VARCHAR(50),
                    idade INTEGER,
                    cpf VARCHAR(14)
        );"""
        )
    except sqlite3.DatabaseError as error:
        print("Ocorreu um erro ao tentar realizar conexão com banco:", error)
        raise

    return connection, cursor


def select_dados(cursor):
    pessoas = cursor.execute("""SELECT * FROM TB_PESSOAS;""")

    for pessoa in pessoas:
        print("-" * 50)
        print(
            f"ID: {pessoa[0]}\nNome: {pessoa[1]}\n"
            + f"Idade: {pessoa[2]}\nCPF: {pessoa[3]}"
        )
    print()


def inserir_dados(cursor, id, dados_pessoa):
    try:
        cursor.execute("""INSERT INTO TB_PESSOAS (id, nome, idade, cpf) VALUES
                        (?, ?, ?, ?);""",
                       (id, dados_pessoa[0], dados_pessoa[1], dados_pessoa[2]))
    # Capturar erros possíveis
    except sqlite3.IntegrityError:
        print(
            "O registro com id:",
            id,
            "já existe. Tentando inserir próximo registro...",
        )
    except sqlite3.DatabaseError as error:
        print(
            "Ocorreu um erro ao inserir os dados no banco.\nMensagem do erro:",
            error,
        )


def atualiza_dados(cursor, connection):
    try:
        cursor.execute("""UPDATE TB_PESSOAS SET idade = 50 WHERE id = 1;""")
    except sqlite3.DatabaseError as error:
        print("Ocorreu um erro ao tentar atualizar o dado no banco:", error)
    connection.commit()


def deleta_quinto_registro(cursor, connection):
    cursor.execute("""DELETE FROM TB_PESSOAS WHERE id = 5""")
    connection.commit()


connection, cursor = inicia_conexao()

# Ler o arquivo de texto dados.txt

with open("./dados.txt", "r", encoding="utf8") as arquivo:
    texto_arquivo = arquivo.read()

# Tratar o arquivo de texto dados.txt
# Separar as linhas do arquivo
lista_pessoas = texto_arquivo.split("\n")

id = 1
for pessoa in lista_pessoas:
    # Separar os campos de cada linha
    dados_pessoa = pessoa.split(", ")
    # Tentar inserir o registro
    inserir_dados(cursor, id, dados_pessoa)
    id += 1

connection.commit()

# Visualizar registros inseridos
select_dados(cursor)

print("Alterando idade do primeiro registro para 50...")

atualiza_dados(cursor, connection)

# Visualizar registros inseridos
select_dados(cursor)

print("Excluindo o último registro")

deleta_quinto_registro(cursor, connection)

# Visualizar registros restantes
select_dados(cursor)
