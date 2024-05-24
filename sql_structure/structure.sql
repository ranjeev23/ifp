use nptel_management;

DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS register_course;
DROP TABLE IF EXISTS certificate;
DROP TABLE IF EXISTS NPTEL_MARKS;
DROP TABLE IF EXISTS Ad_min;
DROP TABLE IF EXISTS set_course;
DROP TABLE IF EXISTS rejected;

create table STUDENT(
dig_id TEXT,
regno BIGINT primary key,
st_name TEXT,
dob DATE,
gender TEXT,
dept TEXT,
section TEXT,
email_id VARCHAR(100),
sem VARCHAR(10),
acc_year VARCHAR(15),
pass_word TEXT
);

create table TEACHER(
staffname TEXT,
email_id VARCHAR(100) Primary key,
pass_word Text
);

create table Course(
c_code VARCHAR(15) PRIMARY KEY,
c_name TEXT,
weeks INTEGER,
nptel_link varchar(255),
if_yes VARCHAR(5)
);

create table REGISTER_COURSE(
regno BIGINT,
c_code varchar(25),
PRIMARY KEY (regno,C_CODE)
);

create table certificate(
regno BIGINT,
c_code Varchar(25),
marks INTEGER,
certificate_link varchar(255),
verified varchar(10),
qr_code_url varchar(255),
upload_date datetime,
PRIMARY KEY (regno,C_CODE)
);

create table NPTEL_MARKS(
regno BIGINT,
c_code varchar(20),
verified_marks integer,
ssn_marks integer,
verified_date datetime,
sem VARCHAR(10),
acc_year varchar(15),
sem_type varchar(15),
PRIMARY KEY (regno,C_CODE)
);

create table Ad_min(
email_id varchar(255) PRIMARY KEY
);

create Table set_course(
c_no INTEGER PRIMARY KEY AUTO_INCREMENT,
SEM VARCHAR(10),
DEPT VARCHAR(10),
C_CODE VARCHAR(10),
ACC_YEAR varchar(15)
);

create table rejected(
regno varchar(255),
C_CODE VARCHAR(10),
teacher_email_id varchar(255),
issue varchar(255),
rejected_date datetime
);

