import psycopg2
from psycopg2 import sql
import ast

def cadastra_user(cursor, nome, email, cpf):
    cursor.execute("INSERT INTO companhia.usuario (nome, email, cpf) VALUES (%s, %s, %s)", (nome, email, cpf))

def cadastra_porto(cursor, cidade, tipo):
    cursor.execute(
        "INSERT INTO porto (cidade, tipo) VALUES (%s, %s)", 
        (cidade, tipo)
    )

def cadastra_administrador(cursor, user_adm, password_adm):
    return cursor.execute(
        "INSERT INTO companhia.administrador (id_adm, user_adm, password_adm) VALUES (12,%s, %s)", 
        (user_adm, password_adm)
    )

def cadastra_navio(cursor, toneladas, status, localizacao):
    cursor.execute(
        "INSERT INTO companhia.navio (toneladas, status, localizacao) VALUES (%s, %s, %s)", 
        (toneladas, status, localizacao)
    )

##Verificar se navio esta livre na data da viagem
#def cria_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm):
#    cursor.execute(
#        """
#        INSERT INTO viagem (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm) 
#        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#        """, 
#        (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm)
#    )

def finalizar_viagem(cursor, id_viagem, data_chegada):
    cursor.execute(f"UPDATE companhia.viagem A SET data_chegada = '{data_chegada}' WHERE A.id_viagem = {id_viagem}")

def historico_todas_viagens(cursor):
    cursor.execute("SELECT * FROM companhia.viagem")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
#Verifica se o navio estara ocupado em certo intervalo de datas
#Retorna true se esta livre
def verificar_status_navio(cursor, id_navio, data_partida, data_chegada):
    cursor.execute(f" select * from companhia.viagem B inner join companhia.navio A on B.id_navio = A.id_navio and B.id_navio = '{id_navio}' and B.data_partida >= '{data_partida}' and B.data_chegada <= '{data_chegada}'")
    rows = cursor.fetchall()
    print(rows)
    return rows == []

#Printa o status de toda a frota
def verificar_status_frota_completa(cursor):
    cursor.execute("SELECT * FROM companhia.navio")
    rows = cursor.fetchall()
    for i in rows:
        print(f"Navio {i[0]} está {i[2]}")
    return

#Printa todas os id de viagens que o locatario já fez
def historico_alugueis_de_user(cursor, id_usuario):
    cursor.execute(f"select (E.id_viagem,E.data_chegada, E.data_partida, F.cidade, H.cidade) from companhia.usuario A inner join companhia.container B on B.id_usuario = A.id_user inner join companhia.transporta D on B.id_container = D.id_container inner join companhia.viagem E on D.id_viagem = E.id_viagem inner join companhia.porto F on E.id_origem = F.id_porto inner join companhia.porto H on E.id_destino = H.id_porto and A.id_user = '{id_usuario}'")
    rows = cursor.fetchall()
    for row in rows:
        info = row[0].replace('(','').replace(')','')
        data_list = info.split(',',5)
        print(f"Viagem de {data_list[3]} para {data_list[4]} no dia {data_list[2]} até {data_list[1]}")

def criar_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_adm):
    navios_livres = []
    cursor.execute(f"select id_navio from companhia.navio ")
    rows = cursor.fetchall()
    for row in rows:
        if verificar_status_navio(cursor, row[0], data_partida, data_chegada):
            navios_livres.append(row[0])
    cursor.excecute(f"insert into companhia.viagem (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm) values ({data_partida}, {hora_partida}, {data_chegada}, {hora_chegada}, {peso_carga}, {id_origem}, {id_destino}, {navios_livres[0]}, {id_adm})")

def adicionar_container_viagem(cursor, id_container, id_viagem):
    #1 - pegar peso da viagem
    #2 - pegar peso do container
    #3 - verificar se o peso do container é menor que o peso da viagem

    cursor.execute(f"select peso from companhia.container where id_container = {id_container}")
    peso_container = cursor.fetchall()
    
    cursor.execute(f"select ")

def main_menu(cursor):
    while True:
        print("\nMenu:")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Porto")
        print("3. Cadastrar Administrador")
        print("4. Cadastrar Navio")
        print("5. Finalizar Viagem")
        print("6. Verificar Status de um Navio")
        print("7. Verificar Status da Frota Completa")
        print("8. Histórico de Todas as Viagens")
        print("9. Histórico de Aluguéis de um Usuário")
        print("10. Criar Viagem")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            cpf = input("CPF: ")
            cadastra_user(cursor, nome, email, cpf)

        elif escolha == "2":
            cidade = input("Cidade: ")
            tipo = input("Tipo (refrigerado/não refrigerado): ")
            cadastra_porto(cursor, cidade, tipo)

        elif escolha == "3":
            user_adm = input("Nome do Administrador: ")
            password_adm = input("Senha: ")
            cadastra_administrador(cursor, user_adm, password_adm)

        elif escolha == "4":
            toneladas = input("Toneladas: ")
            status = input("Status (em viagem/livre): ")
            localizacao = input("Localização: ")
            cadastra_navio(cursor, toneladas, status, localizacao)

        elif escolha == "5":
            id_viagem = input("ID da Viagem: ")
            data_chegada = input("Data de Chegada: ")
            finalizar_viagem(cursor, id_viagem, data_chegada)

        elif escolha == "6":
            id_navio = input("ID do Navio: ")
            data_partida = input("Data de Partida: ")
            data_chegada = input("Data de Chegada: ")
            verificar_status_navio(cursor, id_navio, data_partida, data_chegada)

        elif escolha == "7":
            verificar_status_frota_completa(cursor)

        elif escolha == "8":
            historico_todas_viagens(cursor)

        elif escolha == "9":
            id_usuario = input("ID do Usuário: ")
            historico_alugueis_de_user(cursor, id_usuario)

        elif escolha == "10":
            data_partida = input("Data de Partida: ")
            hora_partida = input("Hora de Partida: ")
            data_chegada = input("Data de Chegada: ")
            hora_chegada = input("Hora de Chegada: ")
            peso_carga = input("Peso da Carga: ")
            id_origem = input("ID de Origem: ")
            id_destino = input("ID de Destino: ")
            id_adm = input("ID do Administrador: ")
            criar_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_adm)

        elif escolha == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="leo123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Você está conectado ao - ", record, "\n") 
    #main_menu(cursor)

    #Fazer um try catch para inserir em companhia.transporta 
    cursor.execute("insert into companhia.transporta (id_viagem, id_container) values (1,2)")
    
    conn.commit()
    cursor.close()
    conn.close()

except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL", error)