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


