create table account
(
    account_id   int         null,
    email        varchar(20) null,
    password     varchar(20) null,
    account_name varchar(20) null,
    constraint account_id
        unique (account_id)
);

create table document
(
    pdf_id            char(36)     not null,
    pdf_name          varchar(60)  null,
    pdf_size          double       null,
    pdf_upload_time   varchar(36)  not null,
    pdf_uploader      varchar(20)  null,
    pdf_update_time   varchar(36)  not null,
    image_status      varchar(10)  null,
    table_status      varchar(10)  null,
    entity_status     varchar(10)  null,
    correction_status varchar(10)  null,
    approval_status   varchar(10)  null,
    pdf_url           varchar(100) null,
    pro_id            int          null,
    constraint pdf_id
        unique (pdf_id)
);

create table member
(
    project_id  int         null,
    member_id   int auto_increment,
    auth        varchar(20) null,
    member_name varchar(20) null,
    constraint member_id
        unique (member_id)
);

create table project
(
    project_id          int auto_increment,
    project_description varchar(100) null,
    project_name        varchar(20)  null,
    constraint project_id
        unique (project_id)
);

