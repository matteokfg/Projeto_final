from PyQt5 import uic, QtWidgets
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

def read(): # funcao que pega valores da tela_filtrar e passa como parametros e usa o read_ _BD correto
    pass

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
    primeria_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[6]
    ultima_ida = Crud.read_Animais_BD(coluna="nome", valor=nome)[7]
    if primeria_ida == ultima_ida:
        if ultima_ida <= date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day):
            return True
        else:
            return False
    else:
        if (ultima_ida <= (date.today() - datetime.date(ultima_ida.year, ultima_ida.month-3, ultima_ida.day))) and ((ultima_ida - primeria_ida) < datetime.delta(months = 3)):
            return True
        else:
            return False

def abrir_tela_filtrar():
    tela_filtrar.show()
    tela_bem_vindo.close()

def voltar_tela_bem_vindo():
    tela_bem_vindo.show()
    tela_filtrar.close()
    
def onClicked_a():
    if tela_filtrar.radioButton_animal.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do Animal", "Data de nascimento", "Peso", "Pelagem", "Sexo", "Primeira ida", "Última ida", "Castrado", "ID da raça", "Nome da Raça"])
        return tela_filtrar.radioButton_animal.text()

def onClicked_c():
    if tela_filtrar.radioButton_cliente.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["CPF", "Nome do Cliente", "Logradouro", "Número", "Bairro", "Cidade", "Estado", "Id do Animal"])
        return tela_filtrar.radioButton_cliente.text()

def onClicked_r():
    if tela_filtrar.radioButton_raca.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["ID", "Nome da raça", "Nome da espécie", "Id da espécie"])
        return tela_filtrar.radioButton_raca.text()

def onClicked_es():
    if tela_filtrar.radioButton_especie.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["ID", "Nome da espécie", "Alimentação"])
        return tela_filtrar.radioButton_especie.text()

def onClicked_em():
    if tela_filtrar.radioButton_email.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do cliente", "Email"])
        return tela_filtrar.radioButton_email.text()
# nome do cliente para achar o id
def onClicked_t():
    if tela_filtrar.radioButton_telefone.isChecked():
        tela_filtrar.comboBox_coluna.addItems(["ID", "Nome do cliente", "DDD", "Telefone"])
        return tela_filtrar.radioButton_telefone.text()

def coluna_ComboBox(s):
    return s

def valor_filtro(s):
    return s
#-- FIM ------------ FUNCOES DE VALIDACAO E DE BACKEND, ENTRE TELAS E CRUD ----------------------


#-- INICIO ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -----------------------------

app = QtWidgets.QApplication(sys.argv)
tela_bem_vindo = uic.loadUi('Tela\bem_vindo.ui')
tela_atualizacao_cliente = uic.loadUi('Tela\atualizacao_cliente.ui')
tela_atualizacao_pet = uic.loadUi('Tela\atualizacao_pet.ui')
tela_cadastro_cliente = uic.loadUi('Tela\cadastro_cliente.ui')
tela_cadastro_pet = uic.loadUi('Tela\cadastro_pet.ui')
tela_excluir_cliente = uic.loadUi('Tela\excluir_cliente.ui')
tela_excluir_pet = uic.loadUi('Tela\excluir_pet.ui')
tela_filtrar = uic.loadUi('Tela\filtrar.ui')

tela_bem_vindo.show()
tela_bem_vindo.btn_filtrar2.clicked.connect(abrir_tela_filtrar)

tela_filtrar.btn_voltar.clicked.connect(voltar_tela_bem_vindo)
tela_filtrar.radioButton_especie.toggle.connect(onClicked_es)
tela_filtrar.radioButton_email.toggle.connect(onClicked_em)
tela_filtrar.radioButton_animal.toggle.connect(onClicked_a)
tela_filtrar.radioButton_cliente.toggle.connect(onClicked_c)
tela_filtrar.radioButton_raca.toggle.connect(onClicked_r)
tela_filtrar.radioButton_telefone.toggle.connect(onClicked_t)
tela_filtrar.comboBox_coluna.currentTextChange.connect(coluna_ComboBox)
tela_filtrar.txt_filtrar.textChanged.connect(valor_filtro)

if tela_filtrar.comboBox_coluna.currentTextChange.connect(coluna_ComboBox) == "CPF":
    tela_filtrar.txt_filtrar.setInputMask('000.000.000-00;_')

# if tela_filtrar.txt_filtrar.setValidator(valida_frase):
#     valor = tela_filtrar.txt_filtrar.Text()
#     if tela_filtrar.checkBox_telefone.Value():
#         tela_filtrar.btn_filtrar.clicked.connect(read("Telefone", valor))
#-- FIM ------------ CONFIGURACAO DAS TELAS PARA DEPOIS EXECUTAR, INCLUI VINCULACAO DAS FUNCOES COM OS BOTOES -------------------------------

app.exec()


