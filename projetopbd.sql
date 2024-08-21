CREATE DATABASE trabalho;

CREATE SCHEMA trabalho AUTHORIZATION POSTGRES;
SET search_path TO trabalho;

CREATE TYPE tipo_porto AS ENUM ('maritimo', 'fluvial');
CREATE TYPE status_navio AS ENUM ('em viagem', 'livre');
CREATE TYPE tipo_container AS ENUM ('refrigerado', 'não refrigerado');


CREATE TABLE administrador(
	id_adm SERIAL PRIMARY KEY,
	user_adm varchar(255) not null,
	password_adm varchar(255) not null);

CREATE TABLE usuario(
	id_user INT PRIMARY KEY,
	nome varchar(255) not null,
	email varchar(255) not null,
	cpf varchar(2515),
	cnpj varchar(255));

CREATE TABLE porto(
	id_porto SERIAL PRIMARY KEY,
	cidade VARCHAR(255) not null,
	tipo tipo_porto not null);

CREATE TABLE navio(
	id_navio SERIAL PRIMARY KEY,
	toneladas INT not null,
	status status_navio not null,
	localizacao varchar(255) not null);

CREATE TABLE viagem(
	id_viagem SERIAL PRIMARY KEY,
	data_partida date not null,
	hora_partida varchar(255) not null,
	data_chegada date not null,
	hora_chegada varchar(255) not null,
	peso_carga INT,
	id_origem INT,
	id_destino INT,
	id_navio INT,
	id_adm INT,
	FOREIGN KEY (id_origem) REFERENCES porto(id_porto),
	FOREIGN KEY (id_destino) REFERENCES porto(id_porto),
	FOREIGN KEY (id_navio) REFERENCES navio(id_navio),
	FOREIGN KEY (id_adm) REFERENCES administrador(id_adm));

CREATE TABLE container(
	id_container int PRIMARY KEY,
	peso INT not null,
	conteudo varchar(255) not null,
	nota_fiscal varchar(255) not null,
	tipo tipo_container not null,
	id_usuario INT,
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_user));

CREATE TABLE transporta( 
	id_viagem INT,
	id_container INT,
	num_container INT,
	FOREIGN KEY (id_viagem) REFERENCES viagem(id_viagem),
	FOREIGN KEY (id_container) REFERENCES container(id_container));

--FUNCTION proc_peso_containers()
CREATE OR REPLACE FUNCTION proc_peso_containers()
RETURNS TRIGGER AS $$
DECLARE
    peso_total_containers INT:= 0;
    peso_navio INT:= 0;
    peso_container_novo INT:= 0;
BEGIN
    -- Calcula o peso total dos containers já associados à viagem
    SELECT COALESCE(SUM(b.peso), 0) INTO peso_total_containers
    FROM trabalho.transporta a
    INNER JOIN trabalho.container b ON a.id_container = b.id_container
    AND a.id_viagem = NEW.id_viagem;
        
    -- Obtém o peso suportado pelo navio associado à viagem
    SELECT d.toneladas INTO peso_navio
    FROM trabalho.viagem c
    INNER JOIN trabalho.navio d ON c.id_navio = d.id_navio
    WHERE c.id_viagem = NEW.id_viagem;
    
    -- Obtém o peso do container que será inserido na viagem
    SELECT e.peso INTO peso_container_novo
    FROM trabalho.container e
    WHERE e.id_container = NEW.id_container;
  
    -- Verifica se o peso total dos containers mais o novo container excede o peso suportado pelo navio
    IF (peso_total_containers + peso_container_novo) > peso_navio THEN
        RAISE EXCEPTION 'Peso total dos containers (%s) excede o peso suportado pelo navio (%s), container não adicionado a viagem', (peso_total_containers + peso_container_novo), peso_navio;
		
	END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--FIM FUNCTION

--TRIGGER para function acima
CREATE TRIGGER trg_peso_viagem
BEFORE INSERT
ON trabalho.transporta
FOR EACH ROW
EXECUTE FUNCTION proc_peso_containers();
--FIM TRIGGER

-- Função para contar os containers e atualizar o número
CREATE OR REPLACE FUNCTION func_trg_num_container()
RETURNS TRIGGER AS $$
DECLARE
    num_containers INT;
BEGIN
    -- Contar o número de containers para a viagem especificada
    SELECT COUNT(*) INTO num_containers
    FROM trabalho.transporta
    WHERE id_viagem = NEW.id_viagem;
    
    -- Atualizar o número de containers para a viagem especificada
    UPDATE trabalho.transporta
    SET num_container = num_containers
    WHERE id_viagem = NEW.id_viagem
    AND id_container = NEW.id_container;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- FIM FUNCTION

-- Trigger para depois que for inserido na tabela transporta
CREATE OR REPLACE TRIGGER trg_num_container
AFTER INSERT 
ON trabalho.transporta
FOR EACH ROW 
EXECUTE FUNCTION func_trg_num_container();


--PROCEDURE 
CREATE OR REPLACE PROCEDURE proc_atualiza_status_navio()
LANGUAGE plpgsql
AS $$
DECLARE
	data_hoje date := CURRENT_DATE;
	data_partida date;
	id_navio int;
	viagem_record RECORD;
BEGIN
	FOR viagem_record IN
		SELECT id_viagem, id_navio
		FROM trabalho.viagem 
		WHERE data_partida = data_hoje
	LOOP
		IF id_navio IS NOT NULL THEN
			UPDATE trabalho.navio
			SET status = 'em viagem'
			WHERE id_navio = id_navio;
		END IF;
	END LOOP;
END;
$$;
--FIM PROCEDURE

INSERT INTO trabalho.administrador (user_adm, password_adm)
VALUES ('admin', 'admin_password');

INSERT INTO trabalho.usuario (id_user,nome, email, cpf, cnpj)
VALUES 
(11,'Usuário 1', 'user1@example.com', '11111111111', NULL),
(12,'Usuário 2', 'user2@example.com', '22222222222', NULL),
(13,'Usuário 3', 'user3@example.com', '33333333333', NULL),
(14,'Usuário 4', 'user4@example.com', '44444444444', NULL),
(15,'Usuário 5', 'user5@example.com', '55555555555', NULL);


INSERT INTO trabalho.container (peso, conteudo, nota_fiscal, tipo, id_usuario)
VALUES 
-- Containers para o Usuário 1
(1000, 'Eletrônicos', 'NF001', 'refrigerado', 11),
(1500, 'Roupas', 'NF002', 'não refrigerado', 11),
(2000, 'Alimentos', 'NF003', 'refrigerado', 11),
(500, 'Móveis', 'NF004', 'não refrigerado', 11),
(1200, 'Livros', 'NF005', 'não refrigerado', 11),
(800, 'Medicamentos', 'NF006', 'refrigerado', 11),
(1600, 'Maquinário', 'NF007', 'não refrigerado', 11),
(1800, 'Computadores', 'NF008', 'refrigerado', 11),
(1100, 'Roupas', 'NF009', 'não refrigerado', 11),
(900, 'Eletrônicos', 'NF010', 'refrigerado', 11),

-- Containers para o Usuário 2
(1100, 'Alimentos', 'NF011', 'refrigerado', 12),
(1300, 'Eletrônicos', 'NF012', 'não refrigerado', 12),
(1400, 'Roupas', 'NF013', 'não refrigerado', 12),
(900, 'Livros', 'NF014', 'não refrigerado', 12),
(1000, 'Medicamentos', 'NF015', 'refrigerado', 12),
(500, 'Eletrônicos', 'NF016', 'refrigerado', 12),
(1200, 'Alimentos', 'NF017', 'refrigerado', 12),
(1500, 'Computadores', 'NF018', 'refrigerado', 12),
(800, 'Roupas', 'NF019', 'não refrigerado', 12),
(900, 'Maquinário', 'NF020', 'não refrigerado', 12),

-- Containers para o Usuário 3
(1000, 'Eletrônicos', 'NF021', 'refrigerado', 13),
(1300, 'Livros', 'NF022', 'não refrigerado', 13),
(900, 'Roupas', 'NF023', 'não refrigerado', 13),
(1100, 'Alimentos', 'NF024', 'refrigerado', 13),
(1400, 'Medicamentos', 'NF025', 'refrigerado', 13),
(1500, 'Móveis', 'NF026', 'não refrigerado', 13),
(800, 'Eletrônicos', 'NF027', 'refrigerado', 13),
(1200, 'Computadores', 'NF028', 'refrigerado', 13),
(1600, 'Maquinário', 'NF029', 'não refrigerado', 13),
(1800, 'Alimentos', 'NF030', 'refrigerado', 13),

-- Containers para o Usuário 4
(1500, 'Roupas', 'NF031', 'não refrigerado', 14),
(1400, 'Eletrônicos', 'NF032', 'refrigerado', 14),
(1600, 'Alimentos', 'NF033', 'refrigerado', 14),
(1000, 'Livros', 'NF034', 'não refrigerado', 14),
(900, 'Medicamentos', 'NF035', 'refrigerado', 14),
(1300, 'Móveis', 'NF036', 'não refrigerado', 14),
(800, 'Eletrônicos', 'NF037', 'refrigerado', 14),
(900, 'Computadores', 'NF038', 'refrigerado', 14),
(1200, 'Maquinário', 'NF039', 'não refrigerado', 14),
(1100, 'Roupas', 'NF040', 'não refrigerado', 14),

-- Containers para o Usuário 5
(1200, 'Eletrônicos', 'NF041', 'refrigerado', 15),
(1000, 'Roupas', 'NF042', 'não refrigerado', 15),
(1500, 'Alimentos', 'NF043', 'refrigerado', 15),
(1800, 'Livros', 'NF044', 'não refrigerado', 15),
(900, 'Medicamentos', 'NF045', 'refrigerado', 15),
(1400, 'Maquinário', 'NF046', 'não refrigerado', 15),
(1600, 'Computadores', 'NF047', 'refrigerado', 15),
(1300, 'Móveis', 'NF048', 'não refrigerado', 15),
(800, 'Eletrônicos', 'NF049', 'refrigerado', 15),
(900, 'Alimentos', 'NF050', 'refrigerado', 15);

INSERT INTO trabalho.porto (cidade, tipo)
VALUES 
('Porto Alegre', 'fluvial'),
('Santos', 'maritimo'),
('Rio de Janeiro', 'maritimo'),
('Salvador', 'maritimo'),
('Manaus', 'fluvial'),
('Fortaleza', 'maritimo'),
('Belém', 'fluvial'),
('São Luís', 'maritimo'),
('Paranaguá', 'maritimo'),
('Vitória', 'maritimo');

INSERT INTO trabalho.navio (toneladas, status, localizacao)
VALUES 
(50000, 'livre', 'Porto Alegre'),
(60000, 'livre', 'Santos'),
(70000, 'livre', 'Rio de Janeiro'),
(80000, 'livre', 'Salvador'),
(55000, 'livre', 'Manaus'),
(50000, 'livre', 'Fortaleza'),
(60000, 'livre', 'Belém'),
(75000, 'livre', 'São Luís'),
(85000, 'livre', 'Paranaguá'),
(65000, 'livre', 'Vitória');

INSERT INTO trabalho.viagem (data_partida, hora_partida, data_chegada, hora_chegada, peso_carga, id_origem, id_destino, id_navio, id_adm)
VALUES 
('2024-08-21', '08:00', '2024-08-22', '18:00', 100000, 11, 12, 11, 3),
('2024-08-22', '09:00', '2024-08-23', '19:00', 150000, 13, 14, 12, 3),
('2024-08-23', '10:00', '2024-08-24', '20:00', 120000, 15, 16, 13, 3),
('2024-08-24', '11:00', '2024-08-25', '21:00', 130000, 17, 18, 14, 3),
('2024-08-25', '12:00', '2024-08-26', '22:00', 140000, 19, 20, 15, 3);

/*


-- Inserindo dados na tabela administrador
INSERT INTO administrador VALUES (3, 'Julia', '4321');
insert into administrador values (01,'Maria', 1234);

-- Inserindo dados na tabela usuario
INSERT INTO usuario VALUES 
(1, 'João Silva', 'joao.silva@email.com', '123.456.789-00', NULL),
(2, 'Empresa XYZ', 'contato@xyz.com.br', NULL, '12.345.678/0001-00');


-- Inserindo dados na tabela porto
INSERT INTO porto VALUES 
(1, 'Rio de Janeiro', 'refrigerado'),
(2, 'Santos', 'não refrigerado');

-- Inserindo dados na tabela navio
INSERT INTO navio VALUES 
(1, 10000, 'em viagem', 'Atlântico'),
(2, 5000, 'livre', 'Porto de Santos');

-- Inserindo dados na tabela viagem
INSERT INTO viagem VALUES 
(1, '2024-08-01', '08:00', '2024-08-10', '14:00', 8000, 1, 2, 1, 11),
(2, '2024-08-05', '09:00', '2024-08-15', '16:00', 3000, 2, 1, 2, 1);

-- Inserindo dados na tabela container
INSERT INTO container VALUES 
(1, 1000, 'Alimentos perecíveis', 'NF-123456', 'refrigerado', 11),
(2, 2000, 'Eletrônicos', 'NF-654321', 'não refrigerado', 2);

-- Inserindo dados na tabela transporta
INSERT INTO transporta VALUES 
(1, 1, 11),
(2, 2, 1);


 SELECT * FROM administrador;

*/