from PyQT5 import uic, QtWidgets
import sys
import os
from datetime import datetime, date
import mysql.connector
import crud as Crud # importa as funcoes do documento crud.py
# os.system("pip install mysql-connector-python")

#-- INICIO ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD -------------------
def valida_data(data):
    """Retorna booleano.

    Argumentos:
    string -- data, 'ano-mes-dia'
    """
    data = data.split("-")
    if datetime.date(data[0], data[1], data[2]) >= date.today():
        return False
    else:
        return True

def acha_id(tabela, coluna, valor):
    query = []
    id = 0
    if tabela == "Raca":
        query = Crud.read_Raca_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Especie":
        query = Crud.read_Especies_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Animal":
        query = Crud.read_Animais_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Cliente":
        query = Crud.read_Cliente_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Telefone":
        query = Crud.read_Telefone_BD(coluna=coluna, valor=valor)
        id = query
    elif tabela == "Email":
        query = Crud.read_Email_BD(coluna=coluna, valor=valor)
        id = query
    else:
        print("Algo deu errado")

    return id

def delete_id(tabela, id):
    query = []
    if tabela == "Raca":
        query = Crud.delete_Raca_BD(id)
    elif tabela == "Especie":
        query = Crud.delete_Especies_BD(id)
    elif tabela == "Animal":
        query = Crud.delete_Animais_BD(id)
    elif tabela == "Cliente":
        query = Crud.delete_Cliente_BD(id)
    elif tabela == "Telefone":
        cliente_id = id[0]
        ddd = id[1]
        telefone = id[2]
        query = Crud.delete_Telefone_BD(cliente_id, ddd, telefone)
    elif tabela == "Email":
        cliente_id = id[0]
        email = id[1]
        query = Crud.delete_Email_BD(cliente_id, email)
    else:
        print("Algo deu errado")

    print(query)

def update_id(tabela, id, exclusividade=None, **colunas):
    contador = 0
    if tabela == "Raca":
        for chave in colunas:
            Crud.update_Raca_BD(id, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    elif tabela == "Especie":
        for chave in colunas:
            Crud.update_Especies_BD(id, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    elif tabela == "Animal":
        for chave in colunas:
            Crud.update_Animais_BD(id, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    elif tabela == "Cliente":
        for chave in colunas:
            Crud.update_Cliente_BD(id, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    elif tabela == "Telefone":
        cliente_id = id[0]
        ddd = id[1]
        telefone = id[2]
        for chave in colunas:
            Crud.update_Telefone_BD(cliente_id, ddd, telefone, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    elif tabela == "Email":
        cliente_id = id[0]
        email = id[1]
        for chave in colunas:
            Crud.update_Email_BD(cliente_id, email, chave:colunas[chave], exclusividade=exclusividade)
            contador += 1
    else:
        print("Algo deu errado")

    print(f"{contador} colunas alteradas")

#delete_id("Cliente", achar_id("Cliente", "nome", "Matteo"))

#-- FIM ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD ----------------------


#-- INICIO ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -----------------------------

# app = QtWidgets.QApplication(sys.argv)
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_s = uic.loadUi('nome_tela.ui')
# tela_inicial = uic.loadUi('nome_tela_inicial.ui')

# tela_inicial.show()

#-- FIM ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -------------------------------

# app.exec()


