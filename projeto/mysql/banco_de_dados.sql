create database PetShop;          -- Cria o banco de dados
use PetShop;                      -- Seleciona o banco para os próximos comandos
/* As linhas acima não devem ser executas em serviços online como o sqlite oline*/
create table Raca (
	id		integer		primary key auto_increment,
    nome	varchar(60)
);

create table Especies (
	id				integer 			primary key auto_increment,
	nome			varchar(50)			unique  not null,
	alimentacao		varchar(20),
    raca_id			integer				references Raca(id)
);
create table Animais (
	id				integer 			primary key auto_increment,
	nome			varchar(50) 		not null,
	data_nasc		date 				not null,
	peso			decimal(10,2)		check (peso > 0),
	pelagem			varchar(50),
    sexo			char(1),
    primeira_ida	date,
    ultima_ida		date,
    castrado		boolean,
	especie_id		int					references Especies(id)
);
create table Telefone (
	dono_id		int,
    ddd			char(2),
    telefone	char(9),
    
    primary key(dono_id, ddd, telefone),
    foreign key(dono_id) references Cliente(cpf)
);
create table Email (
	cliente_id	int,
    email		varchar(100),
    
    primary key(cliente_id, email),
    foreign key(cliente_id) references Cliente(cpf)
);
create table Cliente (
	cpf			char(11)		primary key,
    nome		varchar(60) 	not null,
    logradouro	varchar(100),
    numero		varchar(8),
    bairro		varchar(30),
	animal_id	int				references Animais(id)
);
