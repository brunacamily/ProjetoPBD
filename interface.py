import psycopg2
from psycopg2 import sql
import ast

def cadastra_user(cursor, id, nome, email, cpf, cpfCnpj):
    if cpfCnpj == 1:
        cursor.execute("INSERT INTO projetopbd.usuario (id_user, nome, email, cpf) VALUES (%s, %s, %s, %s)", (id, nome, email, cpf))
    else:
        cursor.execute("INSERT INTO projetopbd.usuario (id_user, nome, email, cnpj) VALUES (%s, %s, %s, %s)", (id, nome, email, cpf))

        
def cadastra_porto(cursor, cidade, tipo):
    cursor.execute(
        "INSERT INTO porto (cidade, tipo) VALUES (%s, %s)", 
        (cidade, tipo)
    )

def cadastra_administrador(cursor, user_adm, password_adm):
    return cursor.execute(
        "INSERT INTO projetopbd.administrador (id_adm, user_adm, password_adm) VALUES (12,%s, %s)", 
        (user_adm, password_adm)
    )

def cadastra_navio(cursor, toneladas, status, localizacao):
    cursor.execute(
        "INSERT INTO projetopbd.navio (toneladas, status, localizacao) VALUES (%s, %s, %s)", 
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
    cursor.execute(f"UPDATE projetopbd.viagem A SET data_chegada = '{data_chegada}' WHERE A.id_viagem = {id_viagem}")

def historico_todas_viagens(cursor):
    cursor.execute("SELECT * FROM projetopbd.viagem")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
#Verifica se o navio estara ocupado em certo intervalo de datas
#Retorna true se esta livre
def verificar_status_navio(cursor, id_navio, data_partida, data_chegada):
    cursor.execute(f" select * from projetopbd.viagem B inner join projetopbd.navio A on B.id_navio = A.id_navio and B.id_navio = '{id_navio}' and B.data_partida >= '{data_partida}' and B.data_chegada <= '{data_chegada}'")
    rows = cursor.fetchall()
    print(rows)
    return rows == []

#Printa o status de toda a frota
def verificar_status_frota_completa(cursor):
    cursor.execute("SELECT * FROM projetopbd.navio")
    rows = cursor.fetchall()
    for i in rows:
        print(f"Navio {i[0]} está {i[2]}")
    return

#Printa todas os id de viagens que o locatario já fez
def historico_alugueis_de_user(cursor, id_usuario):
    cursor.execute(f"select (E.id_viagem,E.data_chegada, E.data_partida, F.cidade, H.cidade) from projetopbd.usuario A inner join projetopbd.container B on B.id_usuario = A.id_user inner join projetopbd.transporta D on B.id_container = D.id_container inner join projetopbd.viagem E on D.id_viagem = E.id_viagem inner join projetopbd.porto F on E.id_origem = F.id_porto inner join projetopbd.porto H on E.id_destino = H.id_porto and A.id_user = '{id_usuario}'")
    rows = cursor.fetchall()
    for row in rows:
        info = row[0].replace('(','').replace(')','')
        data_list = info.split(',',5)
        print(f"Viagem de {data_list[3]} para {data_list[4]} no dia {data_list[2]} até {data_list[1]}")

def criar_viagem(cursor, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_adm):
    navios_livres = []
    cursor.execute(f"select id_navio from projetopbd.navio ")
    rows = cursor.fetchall()
    for row in rows:
        if verificar_status_navio(cursor, row[0], data_partida, data_chegada):
            navios_livres.append(row[0])
    cursor.excecute(f"insert into projetopbd.viagem (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm) values ({data_partida}, {hora_partida}, {data_chegada}, {hora_chegada}, {peso_carga}, {id_origem}, {id_destino}, {navios_livres[0]}, {id_adm})")

def cadastra_container(cursor, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario):
    cursor.execute(
        "INSERT INTO projetopbd.container (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario) VALUES (%s, %s, %s, %s, %s, %s)", 
        (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario)
    )

def inserir_container_na_viagem(cursor, id_viagem, id_container, num_container):
    try:
        cursor.execute(
            "INSERT INTO transporta (id_viagem, id_container, num_container) VALUES (%s, %s, %s)",
            (id_viagem, id_container, num_container)
        )
        print(f"Container {id_container} adicionado à viagem {id_viagem} com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar o container à viagem: {e}")
   

def main_menu(cursor):
    while True:
        print("\nMenu:")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Porto")
        print("3. Cadastrar Administrador")
        print("4. Cadastrar Navio")
        print("5. Cadastrar Container e Inserir em uma Viagem")
        print("6s. Finalizar Viagem")
        print("7. Verificar Status de um Navio")
        print("8. Verificar Status da Frota Completa")
        print("9. Histórico de Todas as Viagens")
        print("10. Histórico de Aluguéis de um Usuário")
        print("11. Criar Viagem")
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


                    case '2':
                        print("\tCadrastar Porto:")
                        cidade = input("Cidade: ")
                        tipo = input("Tipo (refrigerado/não refrigerado): ")
                        cadastra_porto(cursor, cidade, tipo)
                        
                    case '3':
                        print("\tCadrastar Administrador:")
                        user_adm = input("Nome do Administrador: ")
                        password_adm = input("Senha: ")
                        cadastra_administrador(cursor, user_adm, password_adm)
                        
                    case '4':
                        print("\tCadrastar Navio:")
                        toneladas = input("Toneladas: ")
                        status = input("Status (em viagem/livre): ")
                        localizacao = input("Localização: ")
                        cadastra_navio(cursor, toneladas, status, localizacao) 
                        


                    case '5':
                        print("\tCadastrar Container e Inserir em uma Viagem")
                        
                        # Cadastrar o container
                        id_container = input("Id do container: ")
                        peso = input("Digite o peso do container: ")
                        conteudo = input("Qual o conteúdo do container? ")
                        nota_fiscal = input("Digite o código da nota fiscal: ")
                        tipo = input("Digite o tipo do container (refrigerado/não refrigerado): ")
                        id_usuario = input("Digite o ID do usuário associado ao container: ")

                        # Inserir container no banco de dados
                        cadastra_container(cursor, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario)

                        # Solicitar informações da viagem
                        id_viagem = input("Digite o ID da viagem: ")
                        num_container = input("Digite o número do container na viagem: ")

                        # Inserir o container na viagem
                        inserir_container_na_viagem(cursor, id_viagem, id_container, num_container)


  
                            
                    case '6':
                        print("\tFinalizar Viagem:")
                        id_viagem = input("ID da Viagem: ")
                        data_chegada = input("Data de Chegada: ")
                        finalizar_viagem(cursor, id_viagem, data_chegada)  
                        
                    case '7': 
                        print("\tVerificar Status de um Navio")
                        id_navio = input("ID do Navio: ")
                        data_partida = input("Data de Partida: ")
                        data_chegada = input("Data de Chegada: ")
                        verificar_status_navio(cursor, id_navio, data_partida, data_chegada)

                    case '8':
                        print("\tVerificar Status da Frota Completa")
                        verificar_status_frota_completa(cursor)

                    case '9':
                        print("\tHistórico de Todas as Viagens")
                        historico_todas_viagens(cursor)

                    case '10':
                        print("\tHistórico de Aluguéis de um Usuário")
                        id_usuario = input("ID do Usuário: ")
                        historico_alugueis_de_user(cursor, id_usuario)

                    case '11':
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

                    case '0':
                        print("\n\tSaindo")
                        exit()

                    case default:
                        print("Opção inválida. Tente novamente.")

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="26022004",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Você está conectado ao - ", record, "\n") 
    main_menu(cursor)

    #Fazer um try catch para inserir em projetopbd.transporta 
    cursor.execute("insert into projetopbd.transporta (id_viagem, id_container) values (1,2)")
    cursor.execute("insert into projetopbd.transporta (id_viagem, id_container) values (1,2)")


    conn.commit()
    cursor.close()
    conn.close()

except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL", error)