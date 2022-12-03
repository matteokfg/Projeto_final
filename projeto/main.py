from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, 
    QTableWidgetItem, 
    QLabel
)
from PySide6.QtCore import QSize
import sys
import os
from datetime import datetime, date
import mysql.connector
import crud as Crud # importa as funcoes do documento crud.py
# os.system("pip install mysql-connector-python")

coluna = ""
valor = ""
id = 0

#-- INICIO ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD -------------------
def valida_data(data):
    """Retorna booleano.

    Argumentos:
    string -- data, 'ano-mes-dia'
    """

    ano, mes, dia = [int(i) for i in data.split("-")]
    if (date(ano, mes, dia) >= date.today()) and (date(ano, mes, dia) <= datetime.date(1822, 11, 29)):
        return False
    else:
        return True

def valida_numero(numero):
    """Retorna booleano.

    Argumentos:
    int -- numero que sera validado como inteiro.
    """

    if type(numero) == type(1):
        return True
    else:
        return False

def valida_frase(frase):
    """Retorna booleano.

    Argumentos:
    string -- frase que sera validada como string.
    """

    if type(frase) == type("a"):
        return True
    else:
        return False

def valida_sexo(sexo):
    """Retorna booleano.

    Argumentos:
    string -- sigla que representa macho ou femea.
    """

    if (valida_frase(sexo)) and (len(sexo) == 1) and (sexo in ('M', 'F')):
        return True
    else:
        return False

# def valida_estado(estado):
#     """Retorna booleano.

#     Argumentos:
#     string -- sigla que representa estado brasileiro.
#     """

#     if (valida_frase(estado)) and (len(estado) == 2):
#         estado = estado.upper()
#         if estado in ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'):
#             return True
#         else:
#             return False
#     else:
#         return False

# def createTable(query):
#     tableWidget = QTableWidget()

#     if tabela == "Animal":
#         tableWidget.setColumnCount(10)
#     # elif tabela == "Cliente":
#         # tableWidget.setColumnCount(8)
#     # elif tabela == "Email":
#     #     tableWidget.setColumnCount(2)
#     # elif tabela == "Telefone":
#     #     tableWidget.setColumnCount(3)
#     elif tabela == "Raça":
#         tableWidget.setColumnCount(3)
#     elif tabela == "Especie":
#         tableWidget.setColumnCount(3)
#     else:
#         pass

#     for i in range(len(query)):
#         tableWidget.setItem(0, i, QTableWidgetItem(query[i]))

#     tableWidget.horizontalHeader().setStrechLastSection(True)
#     tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Scretch)

def mostra(frase):
    sub_window = QMainWindow()
    # layout = QVBoxLayout()
    # sub_window.setLayout(layout)
    sub_window.setFixedSize(100, 100)

    # createTable(query)
    label = QLabel("")
    label.setText(frase)

    sub_window.setCentralWidget(label)

    sub_window.show()

def read(): # funcao que pega valores da tela_filtrar e passa como parametros e usa o read_ _BD correto
    busca = []
    if valida_frase(tabela):
        if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
            busca = Crud.read_Animais_BD(coluna=coluna, valor=valor)
        # elif tabela == "Cliente":
        #     if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
        #         busca = Crud.read_Cliente_BD(coluna=coluna, valor=valor)
        # elif tabela == "Email":
        #     if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
        #         busca = Crud.read_Email_BD(coluna=coluna, valor=valor)
        # elif tabela == "Telefone":
        #     if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
        #         busca = Crud.read_Telefone_BD(coluna=coluna, valor=valor)
        # elif tabela == "Raça":
        #     if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
        #         busca = Crud.read_Raca_BD(coluna=coluna, valor=valor)
        # elif tabela == "Especie":
        #     if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
        #         busca = Crud.read_Especies_BD(coluna=coluna, valor=valor)
        else:
            print("algo deu errado, tabela inexistente")
    mostra(busca)

def acha_id():
    nome = tela_consulta.txt_nome_pet.text()
    busca_id = Crud.read_Animais_BD(coluna="nome", valor=nome)
    if tela_consulta.tableWidget_consulta_pet.rowCount() != 0:
        for i in range(len(busca_id)):
            tela_consulta.tableWidget_consulta_pet.removeRow(i)
    for n, el in enumerate(busca_id):
        tela_consulta.tableWidget_consulta_pet.insertRow(n)
        for ni, v in enumerate(el):
            print(v, type(v))
            if type(v) == type(date.today()):
                v = str('{0:%Y}-{0:%m}-{0:%d}.'.format(v))
            tela_consulta.tableWidget_consulta_pet.setItem(n, ni, QTableWidgetItem(v))
    id = busca_id[0][0]
    return id
    # """Retorna id (int).

    # Argumentos:
    # string -- nome tabela.
    # string -- coluna tabela.
    # string ou int -- valor tabela.
    # """

    # query = []
    # id = 0
    # if tabela == "Raca":
    #     query = Crud.read_Raca_BD(coluna=coluna, valor=valor)
    #     id = query[0]
    # elif tabela == "Especie":
    #     query = Crud.read_Especies_BD(coluna=coluna, valor=valor)
    #     id = query[0]
    # elif tabela == "Animais":
    #     query = Crud.read_Animais_BD(coluna=coluna, valor=valor)
    #     id = query[0]
    # elif tabela == "Cliente":
    #     query = Crud.read_Cliente_BD(coluna=coluna, valor=valor)
    #     id = query[0]
    # elif tabela == "Telefone":
    #     query = Crud.read_Telefone_BD(coluna=coluna, valor=valor)
    #     id = query
    # elif tabela == "Email":
    #     query = Crud.read_Email_BD(coluna=coluna, valor=valor)
    #     id = query
    # else:
    #     print("Algo deu errado")

    # return id[0]

def delete_id():
    retorno = Crud.delete_Animais_BD(id)
    mostra(retorno)

    # """Retorna qunatas linhas foram deletadas.

    # Argumentos:
    # string -- nome da tabela.
    # int -- id na tabela.
    # """

    # query = []
    # if tabela == "Raca":
    #     query = Crud.delete_Raca_BD(id)
    # elif tabela == "Especie":
    #     query = Crud.delete_Especies_BD(id)
    # elif tabela == "Animal":
    #     query = Crud.delete_Animais_BD(id)
    # elif tabela == "Cliente":
    #     query = Crud.delete_Cliente_BD(id)
    # elif tabela == "Telefone":
    #     cliente_id = id[0]
    #     ddd = id[1]
    #     telefone = id[2]
    #     query = Crud.delete_Telefone_BD(cliente_id, ddd, telefone)
    # elif tabela == "Email":
    #     cliente_id = id[0]
    #     email = id[1]
    #     query = Crud.delete_Email_BD(cliente_id, email)
    # else:
    #     print("Algo deu errado")

    # print(query)

def update_id(): # solucao ruim, refazer
    """Retorna qunatas vezes a tabela foi alterada.

    Argumentos:
    string -- nome da tabela.
    int -- id na tabela.
    string -- passa couna que sera a unica a sofrer UPDATE, padrao = None.
    dictionary -- colunas como chaves e seus novos valores como valores.
    """
    data_nova = tela_consulta.txt_atualizar.text()
    retorno = Crud.update_Animais_BD(id, ultima_ida=data_nova, exclusividade='ultima_ida')
    mostra(retorno)
    # contador = 0
    # if tabela == "Raca":
    #     for chave in colunas:
    #         Crud.update_Raca_BD(id, chave=colunas[chave], exclusividade=chave)
    #         contador += 1
    # elif tabela == "Especie":
    #     for chave in colunas:
    #         Crud.update_Especies_BD(id, chave=colunas[chave], exclusividade=chave)
    #         contador += 1
    # if tabela == "Animal":
        # for chave in colunas:
            # contador += 1
    # elif tabela == "Cliente":
    #     for chave in colunas:
    #         Crud.update_Cliente_BD(id, chave=colunas[chave], exclusividade=chave)
    #         contador += 1
    # elif tabela == "Telefone":
    #     cliente_id = id[0]
    #     ddd = id[1]
    #     telefone = id[2]
    #     for chave in colunas:
    #         Crud.update_Telefone_BD(cliente_id, ddd, telefone, chave=colunas[chave], exclusividade=chave)
    #         contador += 1
    # elif tabela == "Email":
    #     cliente_id = id[0]
    #     email = id[1]
    #     for chave in colunas:
    #         Crud.update_Email_BD(cliente_id, email, chave=colunas[chave], exclusividade=chave)
    #         contador += 1
    # else:
    #     print("Algo deu errado")
    # print(f"{retorno} colunas alteradas")

# def eh_ativo(nome):
#     primeira_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[6]
#     ultima_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[7]
#     if primeira_ida == ultima_ida:
#         if ultima_ida <= date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day):
#             return True
#         else:
#             return False
#     else:
#         if (ultima_ida <= (date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day))) and ((ultima_ida - primeira_ida) < datetime.delta(months = 3)):
#             return True
#         else:
#             return False

def abrir_tela_filtrar():
    tela_filtrar.show()
    tela_bem_vindo.close()

def abrir_tela_consultar():
    tela_consulta.show()
    tela_bem_vindo.close()

def abrir_tela_cadastrar_pet():
    tela_cadastro_pet.show()
    tela_bem_vindo.close()

def voltar_tela_bem_vindo():
    tela_bem_vindo.show()
    tela_filtrar.close()

def voltar_tela_bem_vindo_consulta():
    tela_bem_vindo.show()
    tela_consulta.close()

def voltar_tela_bem_vindo_cadastro():
    tela_bem_vindo.show()
    tela_cadastro_pet.close()

def onClicked_a():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do Animal", "Data de nascimento", "Peso", "Pelagem", "Sexo", "Primeira ida", "Última ida", "Castrado", "ID da raça", "Nome da Raça"])
    return tela_filtrar.radioButton_animal.text()

def onClicked_c():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["CPF", "Nome do Cliente", "Logradouro", "Número", "Bairro", "Cidade", "Estado", "Id do Animal"])
    return tela_filtrar.radioButton_cliente.text()

def onClicked_r():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["ID", "Nome da raça", "Nome da espécie", "Id da espécie"])
    return tela_filtrar.radioButton_raca.text()

def onClicked_es():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["ID", "Nome da espécie", "Alimentação"])
    return tela_filtrar.radioButton_especie.text()

def onClicked_em():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do cliente", "Email"])
    return tela_filtrar.radioButton_email.text()
# nome do cliente para achar o id
def onClicked_t():
    tela_filtrar.comboBox_coluna.clear()
    tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do cliente", "DDD", "Telefone"])
    return tela_filtrar.radioButton_telefone.text()

def valor_filtro(s):
    return s

def cadastra():
    nome = tela_cadastro_pet.txt_nome.text()
    data_nasc = tela_cadastro_pet.txt_data.text()
    peso = tela_cadastro_pet.txt_peso.text()
    pelagem = tela_cadastro_pet.txt_pelagem.text()
    sexo = tela_cadastro_pet.txt_sexo.text().upper()
    primeira_ida = tela_cadastro_pet.txt_primeiraIda.text()
    ultima_ida = tela_cadastro_pet.txt_ultimaIda.text()
    castrado = tela_cadastro_pet.checkBox_castrado.isChecked()
    if valida_sexo(sexo):
        retorno = Crud.insert_Animais_BD(nome, data_nasc, peso, pelagem, sexo, primeira_ida, ultima_ida, castrado)
        mostra(retorno)
    else:
        mostra("Erro na escrita do sexo")
#-- FIM ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD ----------------------


#-- INICIO ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -----------------------------

app = QtWidgets.QApplication(sys.argv)
tela_bem_vindo = uic.loadUi('Pet_Inicial_Novo.ui')
# tela_atualizacao_cliente = uic.loadUi('atualizacao_cliente.ui')
# tela_atualizacao_pet = uic.loadUi('atualizacao_pet.ui')
# tela_cadastro_cliente = uic.loadUi('cadastro_cliente.ui')
tela_cadastro_pet = uic.loadUi('cadastro_pet.ui')
# tela_excluir_cliente = uic.loadUi('excluir_cliente.ui')
#tela_excluir_pet = uic.loadUi('excluir_pet.ui')
# tela_menu_excluir = uic.loadUi('excluir_menu.ui')
tela_filtrar = uic.loadUi('filtrar.ui')
#tela_menu_cadastro = uic.loadUi('cadastro_menu.ui')
#tela_menu_atualizacao = uic.loadUi('atualizacao_menu.ui')
tela_consulta = uic.loadUi('tela_consulta.ui')

tela_bem_vindo.show()
tela_bem_vindo.btn_filtrar.clicked.connect(abrir_tela_filtrar)
tela_bem_vindo.btn_cadastrar.clicked.connect(abrir_tela_cadastrar_pet)
tela_bem_vindo.btn_consultar.clicked.connect(abrir_tela_consultar)


tela_consulta.btn_voltar.clicked.connect(voltar_tela_bem_vindo_consulta)
tela_consulta.pushButton_pesquisar.clicked.connect(acha_id)
tela_consulta.btn_Consulta_excluir_Pet.clicked.connect(delete_id)
tela_consulta.pushButton_atualizar.clicked.connect(update_id)

tela_cadastro_pet.btn_voltar.clicked.connect(voltar_tela_bem_vindo_cadastro)
tela_cadastro_pet.txt_data.setInputMask("0000-00-00")
tela_cadastro_pet.txt_primeiraIda.setInputMask("0000-00-00")
tela_cadastro_pet.txt_ultimaIda.setInputMask("0000-00-00")
tela_cadastro_pet.btn_cadastrar.clicked.connect(cadastra)


tela_filtrar.btn_voltar.clicked.connect(voltar_tela_bem_vindo)
tabela = tela_filtrar.radioButton_especie.clicked.connect(onClicked_es)
tabela = tela_filtrar.radioButton_animal.clicked.connect(onClicked_a)
tabela = tela_filtrar.radioButton_email.clicked.connect(onClicked_em)
tabela = tela_filtrar.radioButton_cliente.clicked.connect(onClicked_c)
tabela = tela_filtrar.radioButton_raca.clicked.connect(onClicked_r)
tabela = tela_filtrar.radioButton_telefone.clicked.connect(onClicked_t)
coluna = tela_filtrar.comboBox_coluna.currentText()
valor = tela_filtrar.txt_filtrar.textChanged.connect(valor_filtro)
tela_filtrar.btn_filtrar.clicked.connect(read)

# if tela_filtrar.comboBox_coluna.currentText() == "CPF":
#     tela_filtrar.txt_filtrar.setInputMask('000.000.000-00;_')
if tela_filtrar.comboBox_coluna.currentText() in ("Data de nascimento", "Primeira ida", "Última ida"):
    tela_filtrar.txt_filtrar.setInputMask('0000-00-00;_')
else:
    pass

# if tela_filtrar.comboBox_coluna.currentText() == "Estado":
#     if valida_estado(valor):
#         pass
#     else:
#         tela_filtrar.txt_filtrar.setText("")

#-- FIM ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -------------------------------

app.exec()


