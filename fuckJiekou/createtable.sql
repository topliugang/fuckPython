drop table if exists category; 
drop table if exists tag;
drop table if exists post; 
drop table if exists posttag;
drop table if exists img;

create table category(
id integer primary key autoincrement,
name text
);

create table tag(
id integer primary key autoincrement,
name text
);

create table post(
id integer primary key autoincrement,
postid text,
title text,
categoryid integer,
posterimgid integer,
screenshotimgid integer
);

create table posttag(
id integer primary key autoincrement,
postid integer,
tagid integer
);

create table img(
id integer primary key autoincrement,
url text,
filepath text
);