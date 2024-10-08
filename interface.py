import psycopg2
from psycopg2 import sql
import ast

def cadastra_user(cursor, id, nome, email, cpf, cpfCnpj):
    if cpfCnpj == 1:
        cursor.execute("INSERT INTO trabalho.usuario (id_user, nome, email, cpf) VALUES (%s, %s, %s, %s)", (id, nome, email, cpf))
    else:
        cursor.execute("INSERT INTO trabalho.usuario (id_user, nome, email, cnpj) VALUES (%s, %s, %s, %s)", (id, nome, email, cpf))
        
def cadastra_porto(cursor, cidade, tipo):
    if tipo == 0:
        cursor.execute(f"INSERT INTO trabalho.porto (cidade, tipo) VALUES ('{cidade}', 'maritimo')")
    else:
        cursor.execute(f"INSERT INTO trabalho.porto (cidade, tipo) VALUES ('{cidade}', 'fluvial')")

def cadastra_administrador(cursor, user_adm, password_adm):
    return cursor.execute(
        "INSERT INTO trabalho.administrador (id_adm, user_adm, password_adm) VALUES (12,%s, %s)", 
        (user_adm, password_adm)
    )

def cadastra_navio(cursor, toneladas, status, localizacao):
    if status == 0:
        cursor.execute(f"INSERT INTO trabalho.navio (toneladas, status, localizacao) VALUES ('{toneladas}', 'em viagem', {localizacao})")
    else:
        cursor.execute(f"INSERT INTO trabalho.navio (toneladas, status, localizacao) VALUES ('{toneladas}', 'livre', {localizacao})")

def finalizar_viagem(cursor, id_viagem, data_chegada):
    cursor.execute(f"UPDATE trabalho.viagem A SET data_chegada = '{data_chegada}' WHERE A.id_viagem = {id_viagem}")

def historico_todas_viagens(cursor):
    cursor.execute("SELECT * FROM trabalho.viagem")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        #info = row.replace('(','').replace(')','')
        #data_list = info.split(',',10)
        #print(f"Viagem ID {data_list[0]}, data partido {data_list[1]} as {data_list[2]}, data previsão chegada {data_list[3]} as {data_list[4]}, peso da carga {data_list[5]}, id origem {data_list[6]}, id destino {data_list[7]}, id navio {data_list[8]}, id administrador {data_list[9]}")

def listar_viagens_nao_comecadas(cursor):
    cursor.execute("select (E.id_viagem,E.data_chegada, E.data_partida, F.cidade, H.cidade) from trabalho.viagem E inner join trabalho.porto F on E.id_origem = F.id_porto inner join trabalho.porto H on E.id_destino = H.id_porto where CURRENT_DATE < E.data_partida")    
    rows = cursor.fetchall()
    print("Viagens que ainda não começaram:")
    for row in rows:
        info = row[0].replace('(','').replace(')','')
        data_list = info.split(',',5)
        print(f"Viagem ID {data_list[0]} de {data_list[3]} para {data_list[4]} no dia {data_list[2]} até {data_list[1]}")

def listar_containers_user(cursor, id_usuario):
    cursor.execute(f"select * from trabalho.container where id_usuario = '{id_usuario}'")
    rows = cursor.fetchall()
    print("Containers do usuário:")
    for row in rows:
        print(row)
#Verifica se o navio estara ocupado em certo intervalo de datas
#Retorna true se esta livre
def verificar_status_navio(cursor, id_navio, data_partida, data_chegada):
    cursor.execute(f" select * from trabalho.viagem B inner join trabalho.navio A on B.id_navio = A.id_navio and B.id_navio = '{id_navio}' and B.data_partida >= '{data_partida}' and B.data_chegada <= '{data_chegada}'")
    rows = cursor.fetchall()
    if rows == []:
        print(f"Navio {id_navio} está livre entre essas datas")
    else:
        print(f"Navio {id_navio} está ocupado entre essas datas")

#Printa o status de toda a frota
def verificar_status_frota_completa(cursor):
    cursor.execute("SELECT * FROM trabalho.navio")
    rows = cursor.fetchall()
    for i in rows:
        print(f"Navio {i[0]} está {i[2]}")
    return

#Printa todas os id de viagens que o locatario já fez
def historico_alugueis_de_user(cursor, id_usuario):
    cursor.execute(f"select (E.id_viagem,E.data_chegada, E.data_partida, F.cidade, H.cidade) from trabalho.usuario A inner join trabalho.container B on B.id_usuario = A.id_user inner join trabalho.transporta D on B.id_container = D.id_container inner join trabalho.viagem E on D.id_viagem = E.id_viagem inner join trabalho.porto F on E.id_origem = F.id_porto inner join trabalho.porto H on E.id_destino = H.id_porto and A.id_user = '{id_usuario}'")
    rows = cursor.fetchall()
    for row in rows:
        info = row[0].replace('(','').replace(')','')
        data_list = info.split(',',5)
        print(f"Viagem de {data_list[3]} para {data_list[4]} no dia {data_list[2]} até {data_list[1]}")

def criar_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_adm):
    navios_livres = []
    cursor.execute(f"select id_navio from trabalho.navio ")
    rows = cursor.fetchall()
    for row in rows:
        if verificar_status_navio(cursor, row[0], data_partida, data_chegada):
            navios_livres.append(row[0])
    cursor.execute(f"insert into trabalho.viagem (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm) values ({data_partida}, {hora_partida}, {data_chegada}, {hora_chegada}, {peso_carga}, {id_origem}, {id_destino}, {navios_livres[0]}, {id_adm})")

def cadastra_container(cursor, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario):
    if tipo == 0:
        cursor.execute(f"INSERT INTO trabalho.container (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario) VALUES ({id_container}, {peso}, '{conteudo}', '{nota_fiscal}', 'refrigerado', {id_usuario})")
    else:
        cursor.execute(f"INSERT INTO trabalho.container (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario) VALUES ({id_container}, {peso}, '{conteudo}', '{nota_fiscal}', 'não refrigerado', {id_usuario})")    

def inserir_container_na_viagem(cursor, id_viagem, id_container, num_container):
    try:
        cursor.execute(f"insert into trabalho.transporta (id_container, id_viagem) values ({id_container}, {id_viagem})")
        print(f"Container {id_container} adicionado à viagem {id_viagem} com sucesso.")
    except Exception as e:
       print(f"Erro ao adicionar o container à viagem: {e}")
   

def main_menu(cursor, conn):
    while True:
        print("\nMenu:")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Porto")
        print("3. Cadastrar Administrador")
        print("4. Cadastrar Navio")
        print("5. Cadastrar Container")
        print("6. Inserir container em uma Viagem")
        print("7. Finalizar Viagem")
        print("8. Verificar Status de um Navio")
        print("9. Verificar Status da Frota Completa")
        print("10. Histórico de Todas as Viagens")
        print("11. Histórico de Aluguéis de um Usuário")
        print("12. Criar Viagem")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")
        
        match escolha:
                    case '1':
                        print("\tCadrastar Usuário:")
                        id = input("Id: ")
                        nome = input("Nome: ")
                        email = input("Email: ")
                        cpfCnpj = int(input("Digite 1 para CPF ou 0 para CNPJ: "))
                        cpf = None
                        
                        while True:                            
                            if cpfCnpj == 1: 
                                cpf = input("CPF: ")
                                break
                            elif cpfCnpj == 0: 
                                cpf = input("CNPJ: ")
                                break
                            else: 
                                print("Opção não existe. Tente novamente.")

                        cadastra_user(cursor, id, nome, email, cpf, cpfCnpj)
                        conn.commit()

                    case '2':
                        print("\tCadrastar Porto:")
                        cidade = input("Cidade: ")
                        tipo = input("Tipo ( 0-maritimo / 1-fluvial): ")
                        cadastra_porto(cursor, cidade, tipo)
                        conn.commit()
                        
                    case '3':
                        print("\tCadrastar Administrador:")
                        user_adm = input("Nome do Administrador: ")
                        password_adm = input("Senha: ")
                        cadastra_administrador(cursor, user_adm, password_adm)
                        conn.commit()
                        
                    case '4':
                        print("\tCadrastar Navio:")
                        toneladas = input("Toneladas: ")
                        status = input("Status (0-em viagem/ 1-livre): ")
                        localizacao = input("Localização: ")
                        cadastra_navio(cursor, toneladas, status, localizacao) 
                        conn.commit()

                    case '5':
                        print("\tCadastrar Container")
                        
                        # Cadastrar o container
                        id_container = input("Id do container: ")
                        peso = input("Digite o peso do container: ")
                        conteudo = input("Qual o conteúdo do container? ")
                        nota_fiscal = input("Digite o código da nota fiscal: ")
                        tipo = input("Digite o tipo do container (0-refrigerado/1-não refrigerado): ")
                        id_usuario = input("Digite o ID do usuário associado ao container: ")

                        # Inserir container no banco de dados
                        cadastra_container(cursor, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario)
                        conn.commit()

                    case '6':
                        print("\tColocar container em uma viagem")
                        id_user = input("ID do usuário: ")
                        listar_viagens_nao_comecadas(cursor)
                        listar_containers_user(cursor, id_user)
                        id_container = input("ID do container: ")
                        id_viagem = input("ID da viagem para colocar o container: ")
                        inserir_container_na_viagem(cursor, id_viagem, id_container, 1)
                        conn.commit()

                    case '7':
                        print("\tFinalizar Viagem:")
                        id_viagem = input("ID da Viagem: ")
                        data_chegada = input("Data de Chegada: ")
                        finalizar_viagem(cursor, id_viagem, data_chegada)  
                        conn.commit()
                        
                    case '8': 
                        print("\tVerificar Status de um Navio")
                        id_navio = input("ID do Navio: ")
                        data_partida = input("Data de Partida: ")
                        data_chegada = input("Data de Chegada: ")
                        verificar_status_navio(cursor, id_navio, data_partida, data_chegada)
                        conn.commit()

                    case '9':
                        print("\tVerificar Status da Frota Completa")
                        verificar_status_frota_completa(cursor)
                        conn.commit()

                    case '10':
                        print("\tHistórico de Todas as Viagens")
                        historico_todas_viagens(cursor)
                        conn.commit()

                    case '11':
                        print("\tHistórico de Aluguéis de um Usuário")
                        id_usuario = input("ID do Usuário: ")
                        historico_alugueis_de_user(cursor, id_usuario)
                        conn.commit()

                    case '12':
                        print("\tCriando Viagem")
                        data_partida = input("Data de Partida: ")
                        hora_partida = input("Hora de Partida: ")
                        data_chegada = input("Data de Chegada: ")
                        hora_chegada = input("Hora de Chegada: ")
                        peso_carga = input("Peso da Carga: ")
                        id_origem = input("ID de Origem: ")
                        id_destino = input("ID de Destino: ")
                        id_adm = input("ID do Administrador: ")
                        criar_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_adm)
                        conn.commit()
                    
                    case '0':
                        print("\n\tSaindo")
                        exit()

                    case default:
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
    main_menu(cursor, conn)

    cursor.close()
    conn.close()

except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL", error)