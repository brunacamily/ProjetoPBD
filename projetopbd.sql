CREATE DATABASE projetoPBD;

CREATE SCHEMA projetoPBD AUTHORIZATION POSTGRES;
SET search_path TO projetoPBD;

CREATE TYPE tipo_porto AS ENUM ('refrigerado', 'não refrigerado');
CREATE TYPE status_navio AS ENUM ('em viagem', 'livre');
CREATE TYPE tipo_container AS ENUM ('refrigerado', 'não refrigerado');


CREATE TABLE administrador(
	id_adm INT PRIMARY KEY,
	user_adm varchar(255) not null,
	password_adm varchar(255) not null);

CREATE TABLE usuario(
	id_user INT PRIMARY KEY,
	nome varchar(255) not null,
	email varchar(255) not null,
	cpf varchar(255),
	cnpj varchar(255));

CREATE TABLE porto(
	id_porto INT PRIMARY KEY,
	cidade VARCHAR(255) not null,
	tipo tipo_porto not null);

CREATE TABLE navio(
	id_navio INT PRIMARY KEY,
	toneladas INT not null,
	status status_navio not null,
	localizacao varchar(255) not null);

CREATE TABLE viagem(
	id_viagem INT PRIMARY KEY,
	data_partida varchar(255) not null,
	hora_partida varchar(255) not null,
	data_chegada varchar(255) not null,
	hora_chegada varchar(255) not null,
	peso_carga INT not null,
	id_origem INT,
	id_destino INT,
	id_navio INT,
	id_adm INT,
	FOREIGN KEY (id_origem) REFERENCES porto(id_porto),
	FOREIGN KEY (id_destino) REFERENCES porto(id_porto),
	FOREIGN KEY (id_navio) REFERENCES navio(id_navio),
	FOREIGN KEY (id_adm) REFERENCES administrador(id_adm));

CREATE TABLE container(
	id_container INT PRIMARY KEY,
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
(1, '2024-08-01', '08:00', '2024-08-10', '14:00', 8000, 1, 2, 1, 1),
(2, '2024-08-05', '09:00', '2024-08-15', '16:00', 3000, 2, 1, 2, 1);

-- Inserindo dados na tabela container
INSERT INTO container VALUES 
(1, 1000, 'Alimentos perecíveis', 'NF-123456', 'refrigerado', 1),
(2, 2000, 'Eletrônicos', 'NF-654321', 'não refrigerado', 2);

-- Inserindo dados na tabela transporta
INSERT INTO transporta VALUES 
(1, 1, 1),
(2, 2, 1);


 SELECT * FROM administrador;

