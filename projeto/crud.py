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
create table Raca (
	id		    integer		primary key auto_increment,
    nome	    varchar(60)	unique not null
    especie_id  integer	    references Especies(id)
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
#os.system("pip install mysql-connector-python")
import mysql.connector #Importa o conector para o python se comunicar com o BD
import datetime #Importa a biblioteca datetime (data/hora)
import time

def conectarBD(host, usuario, senha, DB):
    """Retorna coneccao com o banco de dados.

    Argumentos:
    string -- host do banco de dados mysql.
    string -- usuario do host.
    string -- senha do host, para poder acessar.
    string -- nome do banco de dados, definido pelo comando: create database _.
    """

    connection = mysql.connector.connect( #Informando os dados para conexão com o BD
        host = host,
        user = usuario, #Usuário do MySQL 
        password = senha, #Senha do usuário do MySQL
        database = DB 
    ) #Define o banco de dados usado

    return connection

#INSERT
def insert_Raca_BD(nome, especie_id):
    """Imprime no cmd o id da raca cadastrada no BD.

    Argumentos:
    string -- nome da raca a ser cadastrada.
    int -- numero do id da especie que tem essa raca.
    """

    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql
	# colocar (nome_coluna) em todos os inserts, como no exemplo abaixo
    
    sql = "INSERT INTO Raca(nome, especie_id) VALUES (%s, %s)"
    data = (
        nome,
        especie_id
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrada a raça {nome} do animal com ID:", userid)

def insert_Especies_BD(nome, alimentacao=None):
    """Imprime no cmd o id da especie cadastrada no BD.

    Argumentos:
    string -- nome da especie a ser cadastrada.
    string -- alimentacao da especie cadastrada.
    """

    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    sql = "INSERT INTO Especies(nome, alimentacao, raca_id) VALUES (%s, %s)"
    data = (
        nome, 
        alimentacao
    )

    cursor.execute(sql, data) #Executa o comando SQL
    connection.commit() #Efetua as modificacoes

    userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrada a espécie {nome} do animal com ID:", userid)

def insert_Animais_BD(nome, data_nasc, peso, pelagem, sexo, primeira_ida, ultima_ida, castrado, especie_id):
    """Imprime no cmd o id do animal cadastrado no BD.

    Argumentos:
    string -- nome do animal a ser cadastrado.
    date -- data de nascimento do animal.
    int -- peso do animal, tem de ser maior  que zero.
    string -- cor da pelagem do animal cadastrado.
    string -- de tamanho 1, para definir o sexo do animal.
    date -- data da primeira ida do animal ao petshop.
    date -- data de ultima ida do animal ao petshop, pode ser utilizada com a primeira ida para verificar se é ativo ou não, ou se é novo ou veterano a animal no petshop.
    booleano -- True para castrado, False para nao castrado.
    int -- numero do id da especie que pertence o animal.
    """

    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco, o cursor sabe o que o mysql precisa e o que o mysql retorna, fazendo o meio de campo entre o python e o mysql

    sql = "INSERT INTO Animais(nome, data_nasc, peso, pelagem, sexo, primeira_ida, ultima_ida, castrado, especie_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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

def insert_Cliente_BD(cpf, nome, logradouro, numero, cidade, estado, animal_id, bairro):
    """Imprime no cmd o id do cliente/dono cadastrado no BD.

    Argumentos:
    string -- CPF do cliente/dono do animal a ser cadastrado.
    string -- nome do cliente/dono a ser cadastrado.
    string -- rua do endereco do cliente/dono a ser cadastrado.
    string -- numero do endereco do cliente/dono a ser cadastrado.
    string -- cidade do endereco do cliente/dono a ser cadastrado.
    string -- de tamanho 2, sigla do estado do endereco do cliente/dono a ser cadastrado.
    int -- numero do id do animal que pertence ao cliente/dono.
    string -- bairro do endereco do cliente/dono a ser cadastrado.
    """

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

    #userid = cursor.lastrowid #Obtém o último ID cadastrado

    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão com o BD, boa pratica para economizar os recursos do BD

    print(f"Foi cadastrado o cliente {nome} com CPF:", cpf)

def insert_Telefone_BD(cliente_id, ddd, telefone):
    """Imprime no cmd o id do telefone cadastrado no BD do cliente.

    Argumentos:
    string -- CPF do cliente/dono do telefone a ser cadastrado.
    string -- ddd do telefone a ser cadastrado.
    string -- numero de telefone do telefone a ser cadastrado.
    """

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

    print(f"Foi cadastrado o telefone {ddd}{telefone} do cliente com CPF:", cliente_id)

def insert_Email_BD(cliente_id, email):
    """Imprime no cmd o id do email cadastrado no BD do cliente.

    Argumentos:
    string -- CPF do cliente/dono do email a ser cadastrado.
    string -- email a ser cadastrado.
    """

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

    print(f"Foi cadastrado o email {email} do cliente com CPF:", cliente_id)

###READ
# FAZER READS PARA CADA TABELA, arrumar dentro da funcao, adicionar funcoes agregadoras tbm
def read_Raca_BD(tabela=None, valor=None, group=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco
    
    if tabela == "nome":
        sql = "SELECT * FROM Raca WHERE nome like '" + str(valor) + "%'"

    elif tabela == "count":
        if group == None:
            sql = "SELECT count(" + str(valor) + ") FROM Raca"
        else:
            sql = "SELECT count(" + str(valor) + ") FROM Raca GROUP BY " + str(group)

    elif tabela == "id" or tabela == "especie_id":
        sql = "SELECT * FROM Raca WHERE " + str(tabela) + " = " + str(valor)

    else:
        sql = "SELECT * FROM Raca" #Realizando um select para mostrar todas as linhas e colunas da tabela

    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Especies_BD(tabela=None, valor=None, group=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if tabela == "id":
        sql = "SELECT * FROM Especies WHERE id = " + str(valor)

    elif tabela == "count":
        if group == None:
            sql = "SELECT count("+ str(valor) +") FROM Especies"
        else:
            sql = "SELECT count(" + str(valor) + ") FROM Especies GROUP BY" + str(group)

    elif (tabela == "nome") or (tabela == "alimentacao"):
        sql = "SELECT * FROM Especies WHERE " + str(tabela) + " like '" + str(valor) + "%'"

    else:
        sql = "SELECT * FROM Especies" #Realizando um select para mostrar todas as linhas e colunas da tabela

    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Animais_BD(tabela=None, valor=None, group=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if (tabela == "id") or (tabela == "peso")  or (tabela == "castrado") or (tabela == "especie_id"):
        sql = "SELECT * FROM Animais WHERE " + str(tabela) + " = " + str(valor)
    elif (tabela == "data_nasc") or (tabela == "primeira_ida") or (tabela == "ultima_ida"):
        sql = "SELECT * FROM Animais WHERE " + str(tabela) + " = '" + str(valor) + "'"
    elif tabela == "count":
        if group == None:
            sql = "SELECT count(" + str(valor) + ") FROM Animais"
        else:
            sql = "SELECT count(" + str(valor) + ") FROM Animais GROUP BY " + str(group)

    elif (tabela == "nome") or (tabela == "pelagem"):
        sql = "SELECT * FROM Animais WHERE " + str(tabela) + " like '" + str(valor) + "%'"

    elif tabela == "media":
        if group == None:
            sql = "SELECT avg(" + str(valor) + ") FROM Animais"
        else:
            sql = "SELECT avg(" + str(valor) + ") FROM Animais GROUP BY " + str(group)

    elif tabela == "sexo":
        sql = "SELECT * FROM Animais WHERE sexo = '" + str(valor) + "'"

    else:
        sql = "SELECT * FROM Animais" #Realizando um select para mostrar todas as linhas e colunas da tabela

    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Cliente_BD(tabela=None, valor=None, group=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if (tabela == "cpf") or (tabela == "numero") or (tabela == "animal_id"):
        sql = "SELECT * FROM Cliente WHERE cpf = " + str(valor)

    elif tabela == "count":
        if group == None:
            sql = "SELECT count(" + str(valor) + ") FROM Cliente"
        else:
            sql = "SELECT count(" + str(valor) + ") FROM Cliente GROUP BY " + str(group)

    elif (tabela == "nome") or (tabela == "logradouro") or (tabela == "bairro") or (tabela == "cidade"):
        sql = "SELECT * FROM Cliente WHERE " + str(tabela) + " like '" + str(valor) + "%'"

    elif tabela == "estado":
        sql = "SELECT * FROM Cliente WHERE estado = " + str(valor.upper())

    elif tabela == "endereco":
        valor = valor.split(" ")
        sql = "SELECT * FROM Cliente WHERE numero = " + str(valor[1]) + " and bairro = " + str(valor[2]) + " and logradouro = " + str(valor[0]) + " and cidade = " + str(valor[3]) + " and estado = " + str(valor[4])
    
    else:
        sql = "SELECT * FROM Cliente" #Realizando um select para mostrar todas as linhas e colunas da tabela

    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Telefone_BD(tabela=None, valor=None, group=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if (tabela == "ddd") or (tabela == "cliente_id") or (tabela == "telefone"):
        sql = "SELECT * FROM Telefone WHERE " + str(tabela) + " = " + str(valor)

    elif tabela == "count":
        if group == None:
            sql = "SELECT count(" + str(valor) + ") FROM Telefone"
        else:
            sql = "SELECT count(" + str(valor) + ") FROM Telefone GROUP BY " + str(group)

    elif tabela == "cliente_ddd_telefone":
        valor = valor.split(" ")
        sql = "SELECT * FROM Telefone WHERE cliente_id = " + str(valor[0]) + " and ddd = " + str(valor[1]) + " and telefone = " + str(valor[2])

    else:
        sql = "SELECT * FROM Telefone" #Realizando um select para mostrar todas as linhas e colunas da tabela
    
    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco

    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

def read_Email_BD(tabela=None, valor=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if (tabela == "email") or (tabela == "cliente_id"):
        sql = "SELECT * FROM Email WHERE " + str(tabela) + " = " + str(valor)

    elif tabela == "cliente_email":
        valor = valor.split(" ")
        sql = "SELECT * FROM Email WHERE email = '" + str(valor[1]) + "' and cliente_id = " + str(valor[0])

    elif tabela == "count":
        sql = "SELECT count(" + str(valor) + ") FROM Email"

    else:
        sql = "SELECT * FROM Email" #Realizando um select para mostrar todas as linhas e colunas da tabela
    cursor.execute(sql) #Executa o comando SQL
    results = cursor.fetchall() #Obtém todas as linhas no conjunto de resultados da consulta

    cursor.close() #
    connection.close() #Fecha a conexão com o banco
    for result in results: #Ler os registros existentes com o select
        print(result) #imprime os registros existentes

#UPDATE
def update_Especies_BD(id, nome=None, alimentacao=None, exclusividade=None):
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
    else:
        sql = "UPDATE Especies SET nome = %s, alimentacao = %s WHERE id = %s"
        data = (
            nome, 
            alimentacao,
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

def update_Raca_BD(id, nome=None, especie_id=None, exclusividade=None):
    connection = conectarBD("localhost", "root", "admin", "PetShop") #Recebe a conexão estabelecida com o banco
    cursor = connection.cursor() #Cursor para comunicação com o banco

    if exclusividade == "nome":
        sql = "UPDATE Raca SET nome = %s WHERE id = %s"
        data = (
            nome,
            id
        )
    elif exclusividade == 'especie_id':
        sql = "UPDATE Raca SET especie_id = %s WHERE id = %s"
        data = (
            especie_id,
            id
        )
    else:
        sql = "UPDATE Raca SET nome = %s, especie_id = %s WHERE id = %s"
        data = (
            nome,
            especie_id,
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
    pk = pk.split(" ")
    cliente_id_pk = pk[0]
    ddd_pk = pk[1]
    telefone_pk = pk[2]

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
    pk = pk.split(" ")
    cliente_id_pk = pk[0]
    email_pk = pk[1]

    if exclusividade == 'cliente_id':
        sql = "UPDATE Email SET cliente_id = %s WHERE cliente_id = %s and email = %s"
        data = (
            cliente_id,
            cliente_id_pk,
            email_pk,
        )
    elif exclusividade == 'email':
        sql = "UPDATE Email SET email = %s WHERE cliente_id = %s and email = %s"
        data = (
            email,
            cliente_id_pk,
            email_pk,
        )
    else:
        sql = "UPDATE Email SET cliente_id = %s, email = %s WHERE cliente_id = %s and email = %s"
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
        id,
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
        id,
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
        id,
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
        cpf,
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



#insert_Raca_BD("PUG")
#insert_Especies_BD("salamndra", 2)
#insert_Animais_BD("catatau", "2022-11-24", "35", "ruivo", "m", "2022-11-24", "2022-11-24", False, "1")
#insert_Cliente_BD("12345678911", "Cliento", "Paraty", "365", "pirapora", "AL", "1", "vila amora")
#insert_Telefone_BD("12345678911", 21, 99999999)
#insert_Email_BD("12345678911", "cliento@gmail.com")

#update_Raca_BD(2, "pormessa")
#update_Especies_BD(1, alimentacao = "meu", exclusividade = "alimentacao")
#update_Animais_BD(1, pelagem = "ruiv", exclusividade = 'pelagem')
#update_Cliente_BD('12345678911', estado = "SP", exclusividade = "estado")
#update_Telefone_BD("12345678911 21 99999999", ddd = "44", exclusividade = "ddd")
#update_Email_BD("12345678911 cliento@gmail.com", email = "clientao@gmail.com", exclusividade = "email")


#read_Raca_BD("id", 1)
#read_Raca_BD()
#read_Especies_BD("nome", "s")
#read_Especies_BD()
#read_Animais_BD("data_nasc", "2022-11-24")
#read_Animais_BD()
#read_Cliente_BD("logradouro", "P")
#read_Cliente_BD()
#read_Telefone_BD("ddd", "21")
#read_Telefone_BD()
#read_Email_BD("cliente_email", "12345678911 cliento@gmail.com")
#read_Email_BD()

#delete_Raca_BD("1")
#delete_Especies_BD("1")
#delete_Animais_BD("3")
#delete_Cliente_BD("12345678911")
#delete_Telefone_BD("12345678911", 21, 99999999)
#delete_Email_BD("12345678911", "cliento@gmail.com")
