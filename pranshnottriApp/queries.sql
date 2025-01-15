create table quiz(
    quiz_id varchar(5), 
    quiz_name varchar (100) NOT NULL, 
    category varchar(100) NOT NULL,
    quiz_creation_date datetime NOT NULL,
    no_of_times_played int,
    primary key (quiz_id)
);

create table quiz_question(
    quiz_id varchar(5),
    question_id varchar(5) NOT NULL,
    op1 varchar(500) NOT NULL, 
    op2 varchar(500) NOT NULL,
    op3 varchar(500) NOT NULL, 
    op4 varchar(500) NOT NULL,
    correct_ans char(1) NOT NULL, 
    question_text varchar (10000) NOT NULL,
    primary key (quiz_id, question_id),
    foreign key (quiz_id) references quiz(quiz_id)
);

insert into quiz values('1001','OOPS','Programming','2010-12-31 01:15:00', 0);
insert into quiz_question values('1001','2001','op11','op12','op13','op14','a','Question_text1');
insert into quiz_question values('1001','2002','op21','op22','op23','op24','a','Question_text2');
insert into quiz_question values('1001','2003','op31','op32','op33','op34','a','Question_text3');
insert into quiz_question values('1001','2004','op41','op42','op43','op44','a','Question_text4');