create table pessoas( 
	codigo int auto_increment,
    nome varchar(255),
    apartamento smallint,
    data_nascimento date,
    tipo_pessoa enum('responsavel','morador'),
    primary key(codigo)
    );
update pessoas set nome = '', apartamento = 2, data_nascimento = '1992-02-02', tipo_pessoa = 'responsavel' where codigo = 7;
select apartamento.apartamento, pessoas.nome from apartamento inner join pessoas on apartamento.codigo = pessoas.apartamento;
update apartamento set apartamento = 5 where codigo = 5;
select apartamento.apartamento, pessoas.nome from apartamento left join pessoas on apartamento.codigo = pessoas.apartamento;
delete from pessoas where codigo > 3;
delete from placas_cadastradas where codigo > 2;
update apartamento set responsavel = null where codigo > 3;
select apartamento.apartamento, count(pessoas.codigo) from apartamento left join pessoas on apartamento.codigo = pessoas.apartamento group by apartamento;
select placas_cadastradas.placa, count(*) from logs inner join placas_cadastradas on logs.codigo_veiculo = placas_cadastradas.codigo group by logs.codigo_veiculo;
select placas_cadastradas.placa, pessoas.nome from placas_cadastradas inner join pessoas on placas_cadastradas.responsavel = pessoas.codigo;
select * from apartamento;
select * from pessoas;
select * from logs;
select * from placas_cadastradas;

select apartamento.codigo, apartamento.responsavel, placas_cadastradas.placa 
	from apartamento left join placas_cadastradas on apartamento.responsavel = placas_cadastradas.responsavel order by codigo;
select apartamento.*, placas_cadastradas.placa from apartamento inner join placas_cadastradas on apartamento.responsavel = placas_cadastradas.responsavel;
select pessoas.apartamento, pessoas.nome, placas_cadastradas.placa 
	from pessoas left join placas_cadastradas on pessoas.codigo = placas_cadastradas.responsavel 
		where tipo_pessoa="responsavel" ;
create table apartamento(
	codigo int auto_increment,
    apartamento int unique,
    responsavel int,
    primary key(codigo),
    foreign key(responsavel) references pessoas(codigo)
);

insert into apartamento(apartamento, responsavel) values
	(23,1),
    (5,3),
    (3,1)
    ;
    update apartamento set responsavel =3 where codigo =2;
select * from placas_cadastradas;
select * from pessoas;
update placas_cadastradas inner join pessoas on placas_cadastradas.responsavel = pessoas.nome set placas_cadastradas.responsavel = pessoas.codigo;

insert into pessoas(nome, apartamento, data_nascimento, tipo_pessoa) values
	("Nícholas", 2, "1999-09-06", "responsavel")