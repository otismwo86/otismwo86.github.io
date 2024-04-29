# task2

1. task2-1
``` mysql
create database website;
use website;

2. task2-2
``` mysql
create table member(
	id bigint primary key auto_increment,
    name varchar(255) not null,
    username varchar(255) not null,
    password varchar(255) not null,
    follower_count int unsigned not null default 0,
    time datetime not null default current_timestamp
);

