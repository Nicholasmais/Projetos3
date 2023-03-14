select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' group by hora order by hora;
select * from logs order by codigo desc;
select * from placas_cadastradas;
select * from pessoas;
describe pessoas;
drop trigger delete_person_trigger;
select * from logs order by data_passagem desc, horario_passagem;
insert into logs(codigo_veiculo, data_passagem, horario_passagem, passagem) values(1,"2023-02-12", '10:23:21', 'entrada');
update logs inner join perfil_cadastrados on perfil_cadastrados.nome = logs.nome set logs.codigo_veiculo = perfil_cadastrados.codigo;
alter table logs 
	add column codigo_veiculo int,
    ADD FOREIGN KEY vehicle_fk(codigo_veiculo) REFERENCES perfil_cadastrados(codigo) ON DELETE CASCADE;
    ;
alter table perfil_cadastrados add column apto int;
alter table logs
	drop column nome, drop column placa;
select * from logs;
describe pessoas;
select min(data_passagem) from logs;
select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' and data_passagem like '%' group by hora order by hora