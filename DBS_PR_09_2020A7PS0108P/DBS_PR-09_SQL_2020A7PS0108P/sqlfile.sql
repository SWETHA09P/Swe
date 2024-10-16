create database if not exists cinema;
use cinema;
drop table if exists books;
drop table if exists customer;
drop table if exists seatinline;
drop table if exists shows;
drop table if exists movie;
drop table if exists hall;
drop table if exists theatre;
drop table if exists payment;

create table if not exists customer(
	ID int not null auto_increment,
    name varchar(50) not null,
    email varchar(50) not null,
    password varchar(50) not null,
    primary key(ID)
);

create table if not exists movie(
	ID int not null auto_increment,
    name varchar(50) not null,
    length time not null,
    genre varchar(50),
    language varchar(50),
    primary key(ID)
);

create table if not exists theatre(
	ID int not null auto_increment,
    name varchar(50) not null,
    road varchar(50) not null,
    city varchar(50) not null,
    pincode int not null,
    primary key(ID)
);

create table if not exists hall(
	ID int not null auto_increment,
    theatre_ID int not null,
    capacity int not null,
    constraint pk primary key(ID,theatre_ID),
    constraint fk_hall foreign key (theatre_ID) references theatre(ID) on update cascade on delete cascade
);

create table if not exists shows(
	ID int not null auto_increment,
    movie_ID int not null,
    hall_ID int not null,
    theatre_ID int not null,
    start_time time not null,
    end_time time not null,
    show_date date not null,
    price float not null,
    primary key(ID),
    constraint fk_movie foreign key(movie_ID) references movie(ID) on update cascade on delete cascade,
    constraint fk_halltheatre foreign key(hall_ID,theatre_ID) references hall(ID,theatre_ID) on update cascade on delete cascade
);

create table if not exists payment(
	ID int not null auto_increment,
    amt float not null,
    pay_time time not null,
    pay_date date not null,
    primary key(ID)
);

create table if not exists books(
	customer_ID int not null,
    seat_ID int not null,
    show_ID int not null,
    payment_ID int not null,
    constraint fk_customer foreign key(customer_ID) references customer(ID) on update cascade on delete cascade,
    constraint fk_show foreign key(show_ID) references shows(ID) on update cascade on delete cascade,
    constraint fk_payment foreign key(payment_ID) references payment(ID) on update cascade on delete cascade
);

create table seatinline(
	ID int not null auto_increment,
	seat_ID int not null,
	show_ID int not null,
	book_time time not null,
	book_date date not null,
	primary key(ID),
    constraint fk_seatShow foreign key(show_ID) references shows(ID) on update cascade on delete cascade 
);

select case when exists(select email from customer where email='example') 
                            then 0 else 1 end as val;                         
insert into customer(name,email,password) values('name','email','password');

select s.ID,t.name,start_time,show_date,hall_ID
               from shows s,theatre t
               where s.movie_ID=1 and s.theatre_ID=t.ID
               order by show_date,start_time;

select hall_ID,theatre_ID from shows where ID=1;

select seat_ID from books where show_ID=1;

SELECT seat_ID from seatinline where show_ID=1 and book_date=curdate() 
                        and (cast(curtime() as time)-cast(book_time as time))<=1000;
                        
insert into seatinline(seat_ID,show_ID,book_time,book_date) values
                            (1,1,curtime(),curdate());
                            
insert into payment(amt,pay_time,pay_date)
                            values(5000,curtime(),curdate());
                            
delete from seatinline where seat_ID=1 and show_ID=1;