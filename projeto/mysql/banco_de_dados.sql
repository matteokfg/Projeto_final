create database PetShop;          -- Cria o banco de dados
use PetShop;                      -- Seleciona o banco para os próximos comandos
/* As linhas acima não devem ser executas em serviços online como o sqlite oline*/
create table Especies (
	id				integer 			primary key auto_increment,
	nome			varchar(50)			unique  not null,
	alimentacao		varchar(20)
);

create table Raca (
	id		    integer		primary key auto_increment,
    nome	    varchar(60)	unique not null,
    especie_id  integer references Especies(id)
);

create table Animais (
	id				integer 			primary key auto_increment,
	nome			varchar(50) 		not null,
	data_nasc		date 				not null,
	peso			decimal(10,2)		check (peso > 0),
	pelagem			varchar(50)			not null,
    sexo			char(1)				not null,
    primeira_ida	date				not null,
    ultima_ida		date				not null,
    castrado		boolean				not null,
	cliente_id		integer				references Cliente(cpf)
	raca_id			integer				references Raca(id)
);

create table Cliente (
	cpf			char(11)		primary key,
    nome		varchar(60) 	not null,
    logradouro	varchar(100)	not null,
    numero		varchar(8)		not null,
    bairro		varchar(30),
    cidade		varchar(50)		not null,
    estado		char(2)			not null, 
);

create table Telefone (
	cliente_id	char(11),
    ddd			char(2),
    telefone	char(9),
    
    primary key(cliente_id, ddd, telefone),
    foreign key(cliente_id) references Cliente(cpf)
);

create table Email (
	cliente_id	char(11),
    email		varchar(100),
    
    primary key(cliente_id, email),
    foreign key(cliente_id) references Cliente(cpf)
);
