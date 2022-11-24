#Utilizar os comandos a seguir no MySQL Workbench
#Inicio
"""
create database PetShop;          -- Cria o banco de dados
use PetShop;                      -- Seleciona o banco para os próximos comandos
/* As linhas acima não devem ser executas em serviços online como o sqlite oline*/
create table Raca (
	id		integer		primary key auto_increment,
    nome	varchar(60)	unique not null
);
create table Especies (
	id				integer 			primary key auto_increment,
	nome			varchar(50)			unique  not null,
	alimentacao		varchar(20),
    raca_id			integer				references Raca(id)
);
create table Animais (
	id				integer 			primary key auto_increment,
	nome			varchar(50) 		not null,
	data_nasc		date 				not null,
	peso			decimal(10,2)		check (peso > 0),
	pelagem			varchar(50)			not null,
    sexo			char(1)				not null,
    primeira_ida	date				not null, /* ver se eh ativo */
    ultima_ida		date				not null,
    castrado		boolean				not null,
	especie_id		integer				references Especies(id)
); /* curdate() */
create table Cliente (
	cpf			char(11)		primary key,
    nome		varchar(60) 	not null,
    logradouro	varchar(100)	not null,
    numero		varchar(8)		not null,
    bairro		varchar(30),
    cidade		varchar(50)		not null,
    estado		char(2)			not null, /* colocar em letra maiuscula (.upper)) */
	animal_id	integer			references Animais(id)
);
create table Telefone (
	cliente_id	char(11),
    ddd			char(2),
    telefone	char(9),
    
    primary key(cliente_id, ddd, telefone),
    foreign key(cliente_id) references Cliente(cpf)
);
create table Email (
	cliente_id	char(11),
    email		varchar(100),
    
    primary key(cliente_id, email),
    foreign key(cliente_id) references Cliente(cpf)
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
def insert_Raca_BD(nome):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql
	# colocar (nome_coluna) em todos os inserts, como no exemplo abaixo
    
    sql = "INSERT INTO Raca(nome) VALUES (%s)"
    data = (
        nome,

    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrada a raça {nome} do animal com ID:", userid)

def insert_Especies_BD(nome, raca_id, alimentacao=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    sql = "INSERT INTO Especies(nome, alimentacao, raca_id) VALUES (%s, %s, %s)"
    data = (
        nome, 
        alimentacao,
        raca_id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrada a espécie {nome} do animal com ID:", userid)


def insert_Animais_BD(nome, data_nasc, peso, pelagem, sexo, primeira_ida, ultima_ida, castrado, especie_id):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql

    sql = "INSERT INTO Animais(nome, data_nasc, peso, pelagem, sexo, primeria_ida, ultima_ida, castrado, especie_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (
        nome,
        data_nasc,
        peso,
        pelagem,
        sexo,
        primeira_ida,
        ultima_ida,
        castrado,
        especie_id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado o animal {nome} com ID:", userid)

def insert_Cliente_BD(cpf, nome, logradouro, numero, cidade, estado, animal_id, bairro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco
    if bairro == None:
        sql = "INSERT INTO Cliente(cpf, nome, logradouro, numero, cidade, estado, animal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
            cpf,
            nome,
            logradouro,
            numero,
            cidade,
            estado,
            animal_id
        )
    else:
        sql = "INSERT INTO Cliente(cpf, nome, logradouro, numero, bairro, cidade, estado, animal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
            cpf,
            nome,
            logradouro,
            numero,
            bairro,
            cidade,
            estado,
            animal_id
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado o cliente {nome} com ID:", userid)

def insert_Telefone_BD(cliente_id, ddd, telefone):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql

    sql = "INSERT INTO Telefone(cliente_id, ddd, telefone) VALUES (%s, %s, %s)"
    data = (
        cliente_id,
        ddd,
        telefone
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado o telefone {ddd}{telefone} do cliente com ID:", userid)

def insert_Email_BD(cliente_id, email):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    sql = "INSERT INTO Email(cliente_id, email) VALUES (%s, %s)"
    data = (
        cliente_id,
        email
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado o email {email} do cliente com ID:", userid)

###READ
# FAZER READS PARA CADA TABELA, arrumar dentro da funcao, adicionar funcoes agregadoras tbm
def read_Raca_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco
    
    if tipo == "nome":
        sql = "SELECT * FROM Raca WHERE nome like '%s%'"
        data = (
            filtro
        )
    elif tipo == "count_id":
        sql = "SELECT count(id) FROM Raca"
        data = (

        )
    elif tipo == "id":
        sql = "SELECT * FROM Raca WHERE id = %s"
        data = (
            filtro
        )
    else:
        sql = "SELECT * FROM Raca" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )

    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Especies_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tipo == "id":
        sql = "SELECT * FROM Especies WHERE id = %s"
        data = (
            filtro
        )
    elif tipo == "count_id":
        sql = "SELECT count(id) FROM Especies"
        data = (

        )
    elif tipo == "nome":
        sql = "SELECT * FROM Especies WHERE nome like '%s%'"
        data = (
            filtro
        )
    elif tipo == "alimentacao":
        sql = "SELECT * FROM Especies WHERE alimentacao like '%s%'"
        data = (
            filtro
        )
    elif tipo == "raca_id":
        sql = "SELECT * FROM Especies WHERE raca_id = %s"
        data = (
            filtro
        )
    else:
        sql = "SELECT * FROM Especies" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )

    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Animais_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tipo == "id":
        sql = "SELECT * FROM Animais WHERE id = %s"
        data = (
            filtro
        )
    elif tipo == "count_id":
        sql = "SELECT count(id) FROM Animais"
        data = (

        )
    elif tipo == "nome":
        sql = "SELECT * FROM Animais WHERE nome like '%s%'"
        data = (
            filtro
        )
    elif tipo == "data_nasc":
        sql = "SELECT * FROM Animais WHERE data_nasc = %s"
        data = (
            filtro
        )
    elif tipo == "peso":
        sql = "SELECT * FROM Animais WHERE peso = %s"
        data = (
            filtro
        )
    elif tipo == "media_peso":
        sql = "SELECT avg(peso) FROM Animais"
        data = (

        )
    elif tipo == "pelagem":
        sql = "SELECT * FROM Animais WHERE pelagem like '%s%'"
        data = (
            filtro
        )
    elif tipo == "count_pelagem":
        sql = "SELECT count(pelagem) FROM Animais GROUP BY pelagem"
        data = (

        )
    elif tipo == "sexo":
        sql = "SELECT * FROM Animais WHERE sexo = '%s'"
        data = (
            filtro
        )
    elif tipo == "count_sexo":
        sql = "SELECT count(sexo) FROM Animais GROUP BY sexo"
        data = (

        )
    elif tipo == "primeira_ida":
        sql = "SELECT * FROM Animais WHERE primeira_ida = %s"
        data = (
            filtro
        )
    elif tipo == "ultima_ida":
        sql = "SELECT * FROM Animais WHERE ultima_ida = %s"
        data = (
            filtro
        )
    elif tipo == "castrado":
        sql = "SELECT * FROM Animais WHERE castrado = %s"
        data = (
            filtro
        )
    elif tipo == "count_castrado":
        sql = "SELECT count(castrado) FROM Animais GROUP BY castrado"
        data = (

        )
    if tipo == "especie_id":
        sql = "SELECT * FROM Animais WHERE especie_id = %s"
        data = (
            filtro
        )
    else:
        sql = "SELECT * FROM Animais" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )

    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Cliente_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tipo == "cpf":
        sql = "SELECT * FROM Cliente WHERE cpf = %s"
        data = (
            filtro
        )
    elif tipo == "count_cpf":
        sql = "SELECT count(id) FROM Cliente"
        data = (

        )
    elif tipo == "nome":
        sql = "SELECT * FROM Cliente WHERE nome like '%s%'"
        data = (
            filtro
        )
    elif tipo == "logradouro":
        sql = "SELECT * FROM Cliente WHERE logradouro like '%s%'"
        data = (
            filtro
        )
    elif tipo == "numero":
        sql = "SELECT * FROM Cliente WHERE numero = %s"
        data = (
            filtro
        )
    elif tipo == "bairro":
        sql = "SELECT * FROM Cliente WHERE bairro like '%s%'"
        data = (
            filtro
        )
    elif tipo == "cidade":
        sql = "SELECT * FROM Cliente WHERE cidade like '%s%'"
        data = (
            filtro
        )
    elif tipo == "estado":
        sql = "SELECT * FROM Cliente WHERE estado = %s"
        data = (
            filtro.upper()
        )
    elif tipo == "endereco":
        filtro = filtro.split(" ")
        sql = "SELECT * FROM Cliente WHERE numero = %s and bairro = %s and logradouro = %s and cidade = %s and estado = %s"
        data = (
            filtro[1],
            filtro[2],
            filtro[0],
            filtro[3],
            filtro[4]
        )
    elif tipo == "animal_id":
        sql = "SELECT * FROM Cliente WHERE animal_id = %s"
        data = (
            filtro
        )
    else:
        sql = "SELECT * FROM Cliente" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )

    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Telefone_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tipo == "ddd":
        sql = "SELECT * FROM Telefone WHERE ddd = %s"
        data = (
            filtro
        )
    elif tipo == "count_ddd":
        sql = "SELECT count(ddd) FROM Telefone GROUP BY ddd"
        data = (

        )
    elif tipo == "cliente_id":
        sql = "SELECT * FROM Telefone WHERE cliente_id = %s"
        data = (
            filtro
        )
    elif tipo == "telefone":
        sql = "SELECT * FROM Telefone WHERE telefone = %s"
        data = (
            filtro
        )
    elif tipo == "cliente_ddd_telefone":
        filtro = filtro.split(" ")
        sql = "SELECT * FROM Telefone WHERE cliente_id = %s and ddd = %s and telefone = %s"
        data = (
            filtro
        )
    else:
        sql = "SELECT * FROM Telefone" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )
    
    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Email_BD(tipo=None, filtro=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tipo == "email":
        sql = "SELECT * FROM Email WHERE email = %s"
        data = (
            filtro
        )
    elif tipo == "cliente_id":
        sql = "SELECT * FROM Email WHERE cliente_id = %s"
        data = (
            filtro
        )
    elif tipo == "cliente_emial":
        filtro = filtro.split(" ")
        sql = "SELECT * FROM Email WHERE email = %s and cliente_id = %s"
        data = (
            filtro[1],
            filtro[0]
        )
    else:
        sql = "SELECT * FROM Email" #Realizando um select para mostrar todas as linhas e colunas da tabela
        data = (
            
        )
    
    cursor.execute(sql, data) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

#UPDATE
def update_Especies_BD(id, nome=None, alimentacao=None, raca_id=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco
    
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
    elif exclusividade == 'raca_id':
        sql = "UPDATE Especies SET raca_id = %s WHERE id = %s"
        data = (
            raca_id,
            id
        )
    else:
        sql = "UPDATE Especies SET nome = %s, alimentacao = %s, raca_id = %s WHERE id = %s"
        data = (
            nome, 
            alimentacao,
            raca_id,
            id
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

def update_Animais_BD(id, nome=None, data_nasc=None, peso=None, pelagem=None, sexo=None, primeira_ida=None, ultima_ida=None, castrado=None, especie_id=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

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
    elif exclusividade == 'pelagem':
        sql = "UPDATE Animais SET pelagem = %s WHERE id = %s"
        data = (
            pelagem,
            id
        )
    elif exclusividade == 'sexo':
        sql = "UPDATE Animais SET sexo = %s WHERE id = %s"
        data = (
            sexo,
            id
        )
    elif exclusividade == 'primeira_ida':
        sql = "UPDATE Animais SET primeira_ida = %s WHERE id = %s"
        data = (
            primeira_ida,
            id
        )
    elif exclusividade == 'ultima_ida':
        sql = "UPDATE Animais SET ultima_ida = %s WHERE id = %s"
        data = (
            ultima_ida,
            id
        )
    elif exclusividade == 'castrado':
        sql = "UPDATE Animais SET castrado = %s WHERE id = %s"
        data = (
            castrado,
            id
        )
    elif exclusividade == 'especie_id':
        sql = "UPDATE Animais SET especie_id = %s WHERE id = %s"
        data = (
            especie_id,
            id
        )
    else:
        sql = "UPDATE Animais SET nome = %s, data_nasc = %s, peso = %s, pelagem = %s, sexo = %s, primeira_ida= %s, ultima_ida = %s, castrado = %s, especie_id = %s WHERE id = %s"
        data = (
            nome,
            data_nasc,
            peso,
            pelagem,
            sexo,
            primeira_ida,
            ultima_ida,
            castrado,
            especie_id,
            id
        )

        cursor.execute(sql, data) #Executa o comando SQL
        connection.commit()

        recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

        cursor.close()
        connection.close() #Fecha a conexão com o banco

        print(recordsaffected, " registros alterados")

def update_Cliente_BD(cpf, nome=None, logradouro=None, numero=None, bairro=None, cidade=None, estado=None, animal_id=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if exclusividade == 'nome':
        sql = "UPDATE Cliente SET nome = %s WHERE cpf = %s"
        data = (
            nome,
            cpf
        )
    elif exclusividade == 'logradouro':
        sql = "UPDATE Cliente SET logradouro = %s WHERE cpf = %s"
        data = (
            logradouro,
            cpf
        )
    elif exclusividade == 'numero':
        sql = "UPDATE Cliente SET numero = %s WHERE cpf = %s"
        data = (
            numero,
            cpf
        )
    elif exclusividade == 'bairro':
        sql = "UPDATE Cliente SET bairro = %s WHERE cpf = %s"
        data = (
            bairro,
            cpf
        )
    elif exclusividade == 'cidade':
        sql = "UPDATE Cliente SET cidade = %s WHERE cpf = %s"
        data = (
            cidade,
            cpf
        )
    elif exclusividade == 'estado':
        sql = "UPDATE Cliente SET estado = %s WHERE cpf = %s"
        data = (
            estado,
            cpf
        )
    elif exclusividade == 'animal_id':
        sql = "UPDATE Cliente SET animal_id = %s WHERE cpf = %s"
        data = (
            animal_id,
            cpf
        )
    else:
        sql = "UPDATE Cliente SET nome = %s, logradouro = %s, numero = %s, bairro = %s, cidade = %s, estado = %s, animal_id = %s WHERE cpf = %s"
        data = (
            nome,
            logradouro,
            numero,
            bairro,
            cidade,
            estado,
            animal_id,
            cpf
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

def update_Raca_BD(id, nome=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    sql = "UPDATE Raca SET nome = %s WHERE id = %s"
    data = (
        nome,
        id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

def update_Telefone_BD(pk, cliente_id=None, ddd=None, telefone=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    cliente_id_pk, ddd_pk, telefone_pk = pk.split(" ")

    if exclusividade == 'cliente_id':
        sql = "UPDATE Telefone SET cliente_id = %s WHERE cliente_id = %s and ddd = %s and telefone = %s"
        data = (
            cliente_id,
            cliente_id_pk,
            ddd_pk,
            telefone_pk
        )
    elif exclusividade == 'ddd':
        sql = "UPDATE Telefone SET ddd = %s WHERE cliente_id = %s and ddd = %s and telefone = %s"
        data = (
            ddd,
            cliente_id_pk,
            ddd_pk,
            telefone_pk
        )
    elif exclusividade == 'telefone':
        sql = "UPDATE Telefone SET telefone = %s WHERE cliente_id = %s and ddd = %s and telefone = %s"
        data = (
            telefone,
            cliente_id_pk,
            ddd_pk,
            telefone_pk
        )
    else:
        sql = "UPDATE Telefone SET cliente_id = %s, ddd = %s, telefone = %s WHERE cliente_id = %s and ddd = %s and telefone = %s"
        data = (
            cliente_id,
            ddd,
            telefone,
            cliente_id_pk,
            ddd_pk,
            telefone_pk
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

def update_Email_BD(pk, cliente_id=None, email=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    cliente_id_pk, email_pk = pk.split(" ")

    if exclusividade == 'cliente_id':
        sql = "UPDATE Telefone SET cliente_id = %s WHERE cliente_id = %s and email = %s"
        data = (
            cliente_id,
            cliente_id_pk,
            email_pk,
        )
    elif exclusividade == 'email':
        sql = "UPDATE Telefone SET email = %s WHERE cliente_id = %s and email = %s"
        data = (
            email,
            cliente_id_pk,
            email_pk,
        )
    else:
        sql = "UPDATE Telefone SET cliente_id = %s, email = %s WHERE cliente_id = %s and email = %s"
        data = (
            cliente_id,
            email,
            cliente_id_pk,
            email_pk,
        )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros alterados")

#DELETE
def delete_Raca_BD(id):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Raca WHERE id = %s"
    data = ( 
        id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

def delete_Especies_BD(id):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Especies WHERE id = %s"
    data = (
        id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

def delete_Animais_BD(id):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Animais WHERE id = %s"
    data = (
        id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

def delete_Cliente_BD(cpf):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Cliente WHERE cpf = %s"
    data = (
        cpf
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

def delete_Telefone_BD(cliente_id, ddd, telefone):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Telefone WHERE cliente_id = %s and ddd = %s and telefone = %s"
    data = (
        cliente_id,
        ddd,
        telefone
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")

def delete_Email_BD(cliente_id, email):
    connection = conectarBD("localhost", "root", "admin", "PetShop")
    cursor = connection.cursor()

    sql = "DELETE FROM Email WHERE cliente_id = %s and email = %s"
    data = (
        cliente_id,
        email
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit()

    recordsaffected = cursor.rowcount #Obtém o número de linhas afetadas

    cursor.close()
    connection.close() #Fecha a conexão com o banco

    print(recordsaffected, " registros excluídos")
