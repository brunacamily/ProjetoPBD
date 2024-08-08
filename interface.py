import psycopg2

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'database': 'projetopbd',
    'user': 'postgres',
    'password': '26022004',
    'port': '5432'
}

# Função para conectar ao banco de dados
def connect():
    try:
        conn = psycopg2.connect(**db_config)
        conn.set_client_encoding('UTF8')  # Defina a codificação do cliente
        print("Conectado ao banco de dados com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Funções para operar em cada tabela

# Administrador
def add_administrador(conn, id_adm, user_adm, password_adm):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO administrador (id_adm, user_adm, password_adm)
            VALUES (%s, %s, %s)
        ''', (id_adm, user_adm, password_adm))
        conn.commit()
        cur.close()
        print("Administrador adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar administrador: {e}")

# Usuário
def add_usuario(conn, id_user, nome, email, cpf, cnpj):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO usuario (id_user, nome, email, cpf, cnpj)
            VALUES (%s, %s, %s, %s, %s)
        ''', (id_user, nome, email, cpf, cnpj))
        conn.commit()
        cur.close()
        print("Usuário adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")

# Porto
def add_porto(conn, id_porto, cidade, tipo):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO porto (id_porto, cidade, tipo)
            VALUES (%s, %s, %s)
        ''', (id_porto, cidade, tipo))
        conn.commit()
        cur.close()
        print("Porto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar porto: {e}")

# Navio
def add_navio(conn, id_navio, toneladas, status, localizacao):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO navio (id_navio, toneladas, status, localizacao)
            VALUES (%s, %s, %s, %s)
        ''', (id_navio, toneladas, status, localizacao))
        conn.commit()
        cur.close()
        print("Navio adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar navio: {e}")

# Viagem
def add_viagem(conn, id_viagem, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO viagem (id_viagem, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (id_viagem, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm))
        conn.commit()
        cur.close()
        print("Viagem adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar viagem: {e}")

# Container
def add_container(conn, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO container (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id_container, peso, conteudo, nota_fiscal, tipo, id_usuario))
        conn.commit()
        cur.close()
        print("Container adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar container: {e}")

# Transporte
def add_transporta(conn, id_viagem, id_container, num_container):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO transporta (id_viagem, id_container, num_container)
            VALUES (%s, %s, %s)
        ''', (id_viagem, id_container, num_container))
        conn.commit()
        cur.close()
        print("Transporte adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar transporte: {e}")

# Consultar Tabelas
def query_table(conn, table_name):
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {table_name}')
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Erro ao consultar tabela {table_name}: {e}")

# Interface de Usuário
def main():
    conn = connect()
    if conn:
        while True:
            print("\nMenu:")
            print("1. Adicionar Administrador")
            print("2. Adicionar Usuário")
            print("3. Adicionar Porto")
            print("4. Adicionar Navio")
            print("5. Adicionar Viagem")
            print("6. Adicionar Container")
            print("7. Adicionar Transporte")
            print("8. Consultar Tabela")
            print("9. Sair")

            choice = input("Escolha uma opção: ")

            if choice == '1':
                id_adm = int(input("ID do Administrador: "))
                user_adm = input("Usuário: ")
                password_adm = input("Senha: ")
                add_administrador(conn, id_adm, user_adm, password_adm)
            elif choice == '2':
                id_user = int(input("ID do Usuário: "))
                nome = input("Nome: ")
                email = input("Email: ")
                cpf = input("CPF (opcional): ")
                cnpj = input("CNPJ (opcional): ")
                add_usuario(conn, id_user, nome, email, cpf, cnpj)
            elif choice == '3':
                id_porto = int(input("ID do Porto: "))
                cidade = input("Cidade: ")
                tipo = input("Tipo (refrigerado / não refrigerado): ")
                add_porto(conn, id_porto, cidade, tipo)
            elif choice == '4':
                id_navio = int(input("ID do Navio: "))
                toneladas = int(input("Toneladas: "))
                status = input("Status (em viagem / livre): ")
                localizacao = input("Localização: ")
                add_navio(conn, id_navio, toneladas, status, localizacao)
            elif choice == '5':
                id_viagem = int(input("ID da Viagem: "))
                data_partida = input("Data de Partida: ")
                hora_partida = input("Hora de Partida: ")
                data_chegada = input("Data de Chegada: ")
                hora_chegada = input("Hora de Chegada: ")
                peso_carga = int(input("Peso da Carga: "))
                id_origem = int(input("ID do Porto de Origem: "))
                id_destino = int(input("ID do Porto de Destino: "))
                id_navio = int(input("ID do Navio: "))
                id_adm = int(input("ID do Administrador: "))
                add_viagem(conn, id_viagem, data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm)
            elif choice == '6':
                id_container = int(input("ID do Container: "))
                peso = int(input("Peso: "))
                conteudo = input("Conteúdo: ")
                nota_fiscal = input("Nota Fiscal: ")
                tipo = input("Tipo (refrigerado / não refrigerado): ")
                id_usuario = int(input("ID do Usuário: "))
                add_container(conn, id_container, peso, conteudo, nota_fiscal, tipo, id_usuario)
            elif choice == '7':
                id_viagem = int(input("ID da Viagem: "))
                id_container = int(input("ID do Container: "))
                num_container = int(input("Número do Container: "))
                add_transporta(conn, id_viagem, id_container, num_container)
            elif choice == '8':
                table_name = input("Nome da Tabela: ")
                query_table(conn, table_name)
            elif choice == '9':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")

        conn.close()

if __name__ == "__main__":
    main()
