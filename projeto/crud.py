#Utilizar os comandos a seguir no MySQL Workbench
#Inicio
"""
create database PetShop;          -- Cria o banco de dados
use PetShop;                      -- Seleciona o banco para os próximos comandos

/* As linhas acima não devem ser executas em serviços online como o sqlite oline*/


create table Especies (
	id				integer 			primary key auto_increment,
	nome			varchar(50)			unique  not null,
	alimentacao		varchar(20)
);

create table Animais (
	id				integer 			primary key auto_increment,
	nome			varchar(50) 		not null,
	data_nasc		date 				not null,
	peso			decimal(10,2)		check (peso > 0),
	cor				varchar(50),

	especie_id		int					references Especies(id)
);
"""
#Fim

import os #importa a biblioteca necessária para manipulação do S.O.
import mysql.connector #Importa o conector para o python se comunicar com o BD
import datetime #Importa a biblioteca datetime (data/hora)
import time

def conectarBD(host, usuario, senha, DB):
    connection = mysql.connector.connect( #Informando os dados para conexão com o BD
        host = host,
        user = usuario, #Usuário do MySQL 
        password = senha, #Senha do usuário do MySQL
        database = DB 
    ) #Define o banco de dados usado

    return connection

#INSERT
def insert_BD(nome, alimentacao=None, data_nasc=None, peso=None, cor=None, especie_id=None):
    connection = conectarBD("localhost", "root", "admin", "Login") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql

    if alimentacao != None:
        sql = "INSERT INTO Especies (nome, alimentacao) VALUES (%s, %s)"
        data = (
            nome,
            alimentacao
        )
    else:
        sql = "INSERT INTO Animais (nome, data_nasc, peso, cor, especie_id) VALUES (%s, %s, %s, %s, %s)"
        data = (
            nome,
            data_nasc,
            peso,
            cor,
            especie_id
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado {nome} de ID:", userid)

###READ
def read_BD(tabela):
    connection = conectarBD("localhost", "root", "admin", "Login") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    sql = "SELECT * FROM %s" #Realizando um select para mostrar todas as linhas e colunas da tabela
    data = (
        tabela
    )
    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

#UPDATE

def update_BD(id, nome, alimentacao=None, data_nasc=None, peso=None, cor=None, especie_id=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "Login") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if alimentacao != None:
        if exclusividade == 'nome':
            sql = "UPDATE Especies SET nome = %s WHERE id = %s"
            data = (
                nome,
                id
            )
        elif exclusividade == 'alimentacao':
            sql = "UPDATE Especies SET alimentacao = %s WHERE id = %s"
            data = (
                alimentacao,
                id
            )
        else:
            sql = "UPDATE Especies SET nome = %s, alimentacao = %s WHERE id = %s"
            data = (
                nome, 
                alimentacao,
                id
            )
    else:
        if exclusividade == 'nome':
            sql = "UPDATE Animais SET nome = %s WHERE id = %s"
            data = (
                nome,
                id
            )
        elif exclusividade == 'data_nasc':
            sql = "UPDATE Animais SET data_nasc = %s WHERE id = %s"
            data = (
                data_nasc,
                id
            )
        elif exclusividade == 'peso':
            sql = "UPDATE Animais SET peso = %s WHERE id = %s"
            data = (
                peso,
                id
            )
        elif exclusividade == 'cor':
            sql = "UPDATE Animais SET cor = %s WHERE id = %s"
            data = (
                cor,
                id
            )
        elif exclusividade == 'especie_id':
            sql = "UPDATE Animais SET especie_id = %s WHERE id = %s"
            data = (
                especie_id,
                id
            )
        else:
            sql = "UPDATE Animais SET nome = %s, data_nasc = %s, peso = %s, cor = %s, especie_id = %s WHERE id = %s"
            data = (
                nome,
                data_nasc,
                peso,
                cor,
                especie_id,
                id
            )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

#DELETE
def delete_BD(tabela, id):
    connection = conectarBD("localhost", "root", "admin", "Login")
    cursor = connection.cursor()

    sql = "DELETE FROM %s WHERE id = %s"
    data = (
        tabela, 
        id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

"""
while True:
    os.system("cls")
    print("\n ::::: APLICACA0 D3 GERENCI4MENT0 D0 BD MySQL ::::: \n")
    print(" Digite: ")
    print("1 - Inserir na tabela (INSERT)")
    print("2 - Leitura da tabela (SELECT)")
    print("3 - Atualizacao da tabela (UPDATE)")
    print("4 - Remocao da tabela (DELETE)")
    opcao = int(input("iex> "))

    if opcao == 1:
        print("\n Cadastrar ...\n1 - Animal \n ou \n2 -Especie?")
        opcao1 = int(input("iex> "))
        if opcao1 == 1:
            nome = input("Escreva o nome a ser cadastrado: ")
            data_nasc = input("Escreva a data de nescimento a ser cadastrada: ")
            peso = input("Escreva o peso a ser cadastrado: ")
            cor = input("Escreva a cor a ser cadastrada: ")
            especie_id = input("Escreva o id da especie a ser cadastrado: ")
            insert_BD(nome, data_nasc=data_nasc, peso=peso, cor=cor, especie_id=especie_id)
        elif opcao1 == 2:
            nome = input("Escreva o nome a ser cadastrado: ")
            alimentacao = input("Escreva a alimentacao a ser cadastrada: ")
            insert_BD(nome, alimentacao)
        else:
            print("Erro na digitacao! Retornar ao inicio.")
        time.sleep(3)

    elif opcao == 2:
        print("\n Qual tabela voce quer selecionar? ")
        print("1 - Animal \n2 - Especie")
        tabela = int(input("iex> "))
        if tabela == 1:
            read_BD("Animais")
        elif tabela == 2:
            read_BD("Especies")
        else:
            print("Erro na digitacao! Retornar ao inicio.")
        time.sleep(3)

    elif opcao == 3:
        print("\n ::: Voce quer atualizar o que? :::")
        print("1   - Apenas nome (Animais)")
        print("11  - Apenas nome (Especies)")
        print("2   - Apenas alimentacao")
        print("3   - Apenas data de nescimento")
        print("4   - Apenas peso")
        print("5   - Apenas cor")
        print("6   - Apenas id da especie")
        print("12  - Nome e alimentacao")
        print("136 - Nome, data de nescimento, peso, cor e id da especie")
        opcao3 = int(input("iex> "))

        if opcao3 == 1:
            IDd = input("ID que voce quer atualizar: ")
            nome = input("Escreva o nome a ser atualizado: ")
            update_BD(IDd, nome, exclusividade='nome')
            time.sleep(3)

        elif opcao3 == 11:
            IDd = input("ID que voce quer atualizar: ")
            nome = input("Escreva o nome a ser atualizado: ")
            update_BD(IDd, nome, alimentacao="", exclusividade='nome')
            time.sleep(3)

        elif opcao3 == 2:
            IDd = input("ID que voce quer atualizar: ")
            alimentacao = input("Escreva a alimentacao a ser atualizada: ")
            nome = ""

            update_BD(IDd, nome, alimentacao=alimentacao, exclusividade='alimentacao')
            time.sleep(3)

        elif opcao3 == 3:
            IDd = input("ID que voce quer atualizar: ")
            data_nasc = input("Escreva a data de nascimento a ser atualizada: ")
            nome = ""

            update_BD(IDd, nome, data_nasc=data_nasc, exclusividade='data_nasc')
            time.sleep(3)

        elif opcao3 == 4:
            IDd = input("ID que voce quer atualizar: ")
            peso = input("Escreva o peso a ser atualizado: ")
            nome = ""

            update_BD(IDd, nome, peso=peso, exclusividade='peso')
            time.sleep(3)
        
        elif opcao3 == 5:
            IDd = input("ID que voce quer atualizar: ")
            cor = input("Escreva a cor a ser atualizada: ")
            nome = ""

            update_BD(IDd, nome, peso=peso, exclusividade='peso')
            time.sleep(3)
        
        elif opcao3 == 6:
            IDd = input("ID que voce quer atualizar: ")
            id_especie = input("Escreva o id da especie a ser atualizado: ")
            nome = ""

            update_BD(IDd, nome, especie_id=id_especie, exclusividade='especie_id')
            time.sleep(3)

        elif opcao3 == 12:
            IDd = input("ID que voce quer atualizar: ")
            alimentacao = input("Escreva a alimentacao a ser atualizada: ")
            nome = input("Escreva o nome a ser atualizado: ")

            update_BD(IDd, nome, alimentacao=alimentacao)
            time.sleep(3)

        elif opcao3 == 136:
            IDd = input("ID que voce quer atualizar: ")
            nome = input("Escreva o nome a ser atualizado: ")
            data_nasc = input("Escreva a data de nascimento a ser atualizada: ")
            peso = input("Escreva o peso a ser atualizado: ")
            cor = input("Escreva a cor a ser atualizada: ")
            id_especie = input("Escreva o id da especie a ser atualizado: ")

            update_BD(IDd, nome, data_nasc=data_nasc, peso=peso, cor=cor, especie_id=id_especie)
            time.sleep(3)

        else:
            print("Numero digitado errado")
            time.sleep(3)
        
    elif opcao == 4:
        print("Escreva a tabela que contem o que voce quer apagar:")
        tabela = int(input("iex> "))
        print("Escreva o id que voce quer apagar:")
        IDd = int(input("iex> "))
        
        delete_BD(tabela, IDd)
        time.sleep(3)

    else:
        print("Numero digitado errado")
        time.sleep(3)

    opcao2 = input("Quer realizar mais alguma acao? [y/n] ").lower()
    if opcao2 == 'y':
        pass
    else:
        break
"""
