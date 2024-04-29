#task 2
##task2-1
create database website;
use website;
##task2-2
create table member(
	id bigint primary key auto_increment,
    name varchar(255) not null,
    username varchar(255) not null,
    password varchar(255) not null,
    follower_count int unsigned not null default 0,
    time datetime not null default current_timestamp
);

