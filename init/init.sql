drop table if exists city;

drop table if exists job_field;

drop table if exists lagou_componey;

drop table if exists lagou_job;

/*==============================================================*/
/* Table: city                                                  */
/*==============================================================*/
create table city
(
   id                   varchar(50) not null,
   city_name            varchar(30) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: job_field                                             */
/*==============================================================*/
create table job_field
(
   id                   varchar(50) not null,
   ind_tag              varchar(30) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: lagou_componey                                        */
/*==============================================================*/
create table lagou_company
(
   id                   varchar(50) not null,
   com_name             varchar(50) not null,
   com_keyword          varchar(225),
   com_type             varchar(50) not null,
   com_process          varchar(30) not null,
   com_number           varchar(30),
   com_place_id         varchar(30) not null,
   com_num_school       tinyint,
   com_num_social       int,
   com_site             varchar(50) not null,
   primary key (id)
);

alter table lagou_company comment '拉钩网上的公司详情信息';

/*==============================================================*/
/* Table: lagou_job                                             */
/*==============================================================*/
create table lagou_job
(
   id                   int(10) not null,
   job_name             varchar(50) not null,
   job_salary           varchar(50) not null,
   job_place_id         varchar(50) not null,
   job_exper            varchar(50) not null,
   job_record           varchar(10),
   job_type             varchar(10),
   job_attract          varchar(500),
   job_descr            text,
   job_site             varchar(50) not null,
   primary key (id)
);

alter table lagou_job comment '拉钩的工作职位类型';
