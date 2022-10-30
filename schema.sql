CREATE TABLE Media(
   id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
   name varchar(255),
   date_added date, /* date is always YYYY-MM-DD */
   date_leaving date,
   age_rating varchar(50),
   language varchar(50),
   genre varchar(50),
   length_in_minutes integer,
   company_id integer, /*foreign key to company.id*/
   media_type varchar(50),
   year_of_release year
);

CREATE TABLE Subscribers(
   id integer PRIMARY KEY,
   name varchar(50),
   email varchar(50),
   plan_type varchar(50),
   start_date date,
   end_date date
);

CREATE TABLE Plan(
   plan_type varchar(50) PRIMARY KEY,
   max_number_of_profiles integer,
   cost float
);

CREATE TABLE Profile (
   profile_id integer,
   subscriber_id integer,
   name varchar(50),
   age_rating_limit varchar(50),
   PRIMARY KEY (profile_id, subscriber_id)
);

CREATE TABLE Actor(
   id integer PRIMARY KEY,
   name varchar(50),
   country varchar(50)
);

CREATE TABLE Director(
   id integer PRIMARY KEY,
   name varchar(50),
   country varchar(50)
);

CREATE TABLE Company(
   id integer PRIMARY KEY,
   name varchar(50),
   country varchar(50)
);


CREATE TABLE Media_Director(
   media_id integer,
   director_id integer,
   PRIMARY KEY (media_id, director_id)
);

CREATE TABLE Media_Actor(
   media_id integer,
   actor_id integer,
   PRIMARY KEY (media_id, actor_id)
);
