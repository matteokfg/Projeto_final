from PyQt5 import uic, QtWidgets
import sys
import os
from datetime import datetime, date
import mysql.connector
import crud as Crud # importa as funcoes do documento crud.py
# os.system("pip install mysql-connector-python")

tabela = ""
coluna = ""
valor = ""

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

def valida_estado(estado):
    """Retorna booleano.

    Argumentos:
    string -- sigla que representa estado brasileiro.
    """

    if (valida_frase(estado)) and (len(estado) == 2):
        estado = estado.upper()
        if estado in ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'):
            return True
        else:
            return False
    else:
        return False

def createTable(query):
    tableWidget = QTableWidget()

    if tabela == "Animal":
        tableWidget.setColumnCount(10)
    elif tabela == "Cliente":
        tableWidget.setColumnCount(8)
    elif tabela == "Email":
        tableWidget.setColumnCount(2)
    elif tabela == "Telefone":
        tableWidget.setColumnCount(3)
    elif tabela == "Raça":
        tableWidget.setColumnCount(3)
    elif tabela == "Especie":
        tableWidget.setColumnCount(3)
    else:
        pass

    for i in range(len(query)):
        tableWidget.setItem(0, i, QTableWidgetItem(query[i]))

    tableWidget.horizontalHeader().setStrechLastSection(True)
    tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Scretch)

def mostra(query):
    sub_window = QWidget()
    layout = QVBoxLayout()
    sub_window.setLayout(layout)

    createTable(query)

    sub_window.addWidget(tableWidget)

    sub_window.show()

def read(): # funcao que pega valores da tela_filtrar e passa como parametros e usa o read_ _BD correto
    if valida_frase(tabela):
        if tabela == "Animal":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Animais_BD(coluna=coluna, valor=valor)
        elif tabela == "Cliente":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Cliente_BD(coluna=coluna, valor=valor)
        elif tabela == "Email":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Email_BD(coluna=coluna, valor=valor)
        elif tabela == "Telefone":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Telefone_BD(coluna=coluna, valor=valor)
        elif tabela == "Raça":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Raca_BD(coluna=coluna, valor=valor)
        elif tabela == "Especie":
            if valida_frase(coluna) and (valida_frase(valor) or valida_data(valor) or valida_numero(valor) or valida_sexo(valor)):
                query = Crud.read_Especies_BD(coluna=coluna, valor=valor)
        else:
            print("algo deu errado, tabela inexistente")
    mostra(query)

def acha_id(tabela, coluna, valor):
    """Retorna id (int).

    Argumentos:
    string -- nome tabela.
    string -- coluna tabela.
    string ou int -- valor tabela.
    """

    query = []
    id = 0
    if tabela == "Raca":
        query = Crud.read_Raca_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Especie":
        query = Crud.read_Especies_BD(coluna=coluna, valor=valor)
        id = query[0]
    elif tabela == "Animais":
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

    return id[0]

def delete_id(tabela, id):
    """Retorna qunatas linhas foram deletadas.

    Argumentos:
    string -- nome da tabela.
    int -- id na tabela.
    """

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

def update_id(tabela, id, exclusividade=None, **colunas): # solucao ruim, refazer
    """Retorna qunatas vezes a tabela foi alterada.

    Argumentos:
    string -- nome da tabela.
    int -- id na tabela.
    string -- passa couna que sera a unica a sofrer UPDATE, padrao = None.
    dictionary -- colunas como chaves e seus novos valores como valores.
    """

    contador = 0
    if tabela == "Raca":
        for chave in colunas:
            Crud.update_Raca_BD(id, chave=colunas[chave], exclusividade=chave)
            contador += 1
    elif tabela == "Especie":
        for chave in colunas:
            Crud.update_Especies_BD(id, chave=colunas[chave], exclusividade=chave)
            contador += 1
    elif tabela == "Animal":
        for chave in colunas:
            Crud.update_Animais_BD(id, chave=colunas[chave], exclusividade=chave)
            contador += 1
    elif tabela == "Cliente":
        for chave in colunas:
            Crud.update_Cliente_BD(id, chave=colunas[chave], exclusividade=chave)
            contador += 1
    elif tabela == "Telefone":
        cliente_id = id[0]
        ddd = id[1]
        telefone = id[2]
        for chave in colunas:
            Crud.update_Telefone_BD(cliente_id, ddd, telefone, chave=colunas[chave], exclusividade=chave)
            contador += 1
    elif tabela == "Email":
        cliente_id = id[0]
        email = id[1]
        for chave in colunas:
            Crud.update_Email_BD(cliente_id, email, chave=colunas[chave], exclusividade=chave)
            contador += 1
    else:
        print("Algo deu errado")

    print(f"{contador} colunas alteradas")
#delete_id("Cliente", achar_id("Cliente", "nome", "Matteo"))

def eh_ativo(nome):
    primeira_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[6]
    ultima_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[7]
    if primeira_ida == ultima_ida:
        if ultima_ida <= date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day):
            return True
        else:
            return False
    else:
        if (ultima_ida <= (date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day))) and ((ultima_ida - primeira_ida) < datetime.delta(months = 3)):
            return True
        else:
            return False

def abrir_tela_filtrar():
    tela_filtrar.show()
    tela_bem_vindo.close()

def abrir_tela_menu_excluir():
    tela_menu_excluir.show()
    tela_bem_vindo.close()

def abrir_tela_menu_cadastrar():
    tela_menu_cadastro.show()
    tela_bem_vindo.close()

def abrir_tela_menu_atualizar():
    tela_menu_atualizacao.show()
    tela_bem_vindo.close()

def voltar_tela_bem_vindo():
    tela_bem_vindo.show()
    tela_filtrar.close()
    
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
#-- FIM ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD ----------------------


#-- INICIO ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -----------------------------

#-- nao mexer --
app = QtWidgets.QApplication(sys.argv)
tela_bem_vindo = uic.loadUi('bem_vindo.ui')
tela_atualizacao_cliente = uic.loadUi('atualizacao_cliente.ui')
tela_atualizacao_pet = uic.loadUi('atualizacao_pet.ui')
tela_cadastro_cliente = uic.loadUi('cadastro_cliente.ui')
tela_cadastro_pet = uic.loadUi('cadastro_pet.ui')
tela_excluir_cliente = uic.loadUi('excluir_cliente.ui')
tela_excluir_pet = uic.loadUi('excluir_pet.ui')
tela_menu_excluir = uic.loadUi('excluir_menu.ui')
tela_filtrar = uic.loadUi('filtrar.ui')
tela_menu_cadastro = uic.loadUi('cadastro_menu.ui')
tela_menu_atualizacao = uic.loadUi('atualizacao_menu.ui')
#-- nao mexer --

#-- nao mexer -- matteo
tela_bem_vindo.show()
tela_bem_vindo.btn_filtrar2.clicked.connect(abrir_tela_filtrar)
tela_bem_vindo.btn_cadastrar.clicked.connect(abrir_tela_menu_cadastrar)
tela_bem_vindo.btn_atualizar2.clicked.connect(abrir_tela_menu_atualizar)
tela_bem_vindo.btn_excluir2.clicked.connect(abrir_tela_menu_excluir)
#-- nao mexer --
#-- matteo --


tela_filtrar.btn_voltar.clicked.connect(voltar_tela_bem_vindo)
tela_filtrar.radioButton_especie.clicked.connect(onClicked_es)
tela_filtrar.radioButton_animal.clicked.connect(onClicked_a)
tela_filtrar.radioButton_email.clicked.connect(onClicked_em)
tela_filtrar.radioButton_cliente.clicked.connect(onClicked_c)
tela_filtrar.radioButton_raca.clicked.connect(onClicked_r)
tela_filtrar.radioButton_telefone.clicked.connect(onClicked_t)
coluna = tela_filtrar.comboBox_coluna.currentText()
valor = tela_filtrar.txt_filtrar.textChanged.connect(valor_filtro)
tela_filtrar.btn_filtrar.clicked.connect(read)

if tela_filtrar.comboBox_coluna.currentText() == "CPF":
    tela_filtrar.txt_filtrar.setInputMask('000.000.000-00;_')
elif tela_filtrar.comboBox_coluna.currentText() in ("Data de nascimento", "Primeira ida", "Última ida"):
    tela_filtrar.txt_filtrar.setInputMask('0000-00-00;_')
else:
    pass

if tela_filtrar.comboBox_coluna.currentText() == "Estado":
    if valida_estado(valor):
        pass
    else:
        tela_filtrar.txt_filtrar.setText("")

#-- matteo --

# if tela_filtrar.txt_filtrar.setValidator(valida_frase):
#     valor = tela_filtrar.txt_filtrar.Text()
#     if tela_filtrar.checkBox_telefone.Value():
#         tela_filtrar.btn_filtrar.clicked.connect(read("Telefone", valor))
#-- FIM ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -------------------------------

app.exec()


