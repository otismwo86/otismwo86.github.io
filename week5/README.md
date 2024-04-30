
# task2
1. task2-1
``` mysql
create database website;
use website;
```
![task2-1](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/addc730c-8a1c-42a6-ae73-db8ceddc4460)

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
```
![task2-2](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/6e5ef54e-f3e0-4a6b-aca1-fd26f2669e5e)

# task3
1.task3-1
``` mysql
Insert into member(name,username,password,follower_count) values ('test','test','test',100);
Insert into member(name,username,password,follower_count) values ('John','John0776','imJohn',135);
Insert into member(name,username,password,follower_count) values ('Mary','Mary8899','Maryhasalittlesheep',56);
Insert into member(name,username,password,follower_count) values ('Jim','Jim55098','imjim',77);
Insert into member(name,username,password,follower_count) values ('luka','luka7899','imluka',98);
```

2.task3-2
``` mysql
select * from member;
```
![task3-1 3-2](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/03a5129e-553e-449c-b57b-51ee560bf0f6)

3.task3-3
``` mysql
select * from member order by time desc;
```
![task3-3](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/0566c989-e0d7-42f6-8877-32968a81706b)

4.task3-4
``` mysql
select * from member order by time desc limit 3 offset 1;
```
![task3-4](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/d1223e36-0309-4438-a759-8a9c22e1d0d0)

5.task3-5
``` mysql
select * from member where username='test';
```
![task3-5](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/08d6c7d2-1f36-476c-982d-e72fb35ae377)


6.task3-6
``` mysql
select * from member where name like '%es%';
```
![task3-6](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/ee40718a-a3ab-4f88-a20f-6e3f472fd533)

7.task3-7
``` mysql
select * from member where username='test' and password='test';
```
![task3-7](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/2a668174-2b47-4596-b0d7-d9491a76a3af)


8.task3-8
``` mysql
update member set name='test2' where username='test';
```
![task3-8](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/a8efd378-b1fa-43f0-a830-7c1110cbf7aa)

# task4
1.task4-1
``` mysql
select count(*) from member;
```
![task4-1](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/0429043a-345e-454f-a9e8-6605128f492c)

2.task4-2
``` mysql
select sum(follower_count) from member;
```
![task4-2](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/72b5ece3-8075-41d0-b70f-b87c254ea8d2)

3.task4-3
``` mysql
select avg(follower_count) from member;
```
![task4-3](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/01a8475f-aceb-46c5-8742-36ee75552ba0)

4.task4-4
``` mysql
select avg(follower_count) from (select * from member order by follower_count desc limit 2) as tworows;
```
![task4-4](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/ca5f7e82-75ec-4559-9f35-b2221b0121ba)

# task5
1.task5-1
``` mysql
create table message(
	id bigint primary key auto_increment,
    member_id bigint,
    content varchar(255) not null,
    like_count int unsigned not null default 0,
    time datetime not null default current_timestamp,
    foreign key (member_id) references member(id)
);
```
![task5-1](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/04f0f962-5808-45cf-b4df-4dd4ebf2ad7b)

-插入資料
``` mysql
insert into message (member_id,content,like_count) values (1,'im test',8);
insert into message (member_id,content,like_count) values (1,'this is a test',12);
insert into message (member_id,content,like_count) values (2,'im John',5);
insert into message (member_id,content,like_count) values (2,'johnny walker',78);
insert into message (member_id,content,like_count) values (3,'im Mary',9);
insert into message (member_id,content,like_count) values (3,'I dont have a sheep',45);
insert into message (member_id,content,like_count) values (4,'im Jim',11);
insert into message (member_id,content,like_count) values (4,'whats up',66);
insert into message (member_id,content,like_count) values (5,'im Luka',34);
insert into message (member_id,content,like_count) values (5,'Luka is here',77);
```
![task5-1-1](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/c3c591fd-2721-48a9-9521-3c6e389649d1)

2.task5-2
``` mysql
select message.*, member.name from message join member on message.member_id = member.id;
```
![task5-2](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/859e46ad-e5b6-4546-a3ca-94d02c4314b3)

3.task5-3
``` mysql
select message.*, member.name from message join member on message.member_id = member.id where member.username='test';
```
![task5-3](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/5e478101-8fac-4d23-b7b1-a2d1754a14ef)

4.task5-4
``` mysql
select avg(message.like_count) from message join member on message.member_id = member.id where member.username='test';
```
![task5-4](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/463afbf4-d100-4a4f-88de-116900ec8f5a)

5.task5-5
``` mysql
select member.username,avg(message.like_count) from message join member on message.member_id = member.id group by member.username;
```
![task5-5](https://github.com/otismwo86/otismwo86.github.io/assets/156811348/7aa3a3a7-8d9c-4a94-8c2f-d5b4fb1e216b)
