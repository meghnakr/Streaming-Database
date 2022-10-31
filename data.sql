INSERT INTO Media (name, date_added, date_leaving, age_rating, language, genre, length_in_minutes, 
    company_id, media_type, year_of_release)
    VALUES ("Star Wars: Episode IV - A New Hope", '2022-11-01', NULL, 'PG', 'English', 
    'Science Fiction', 105, 1, "Movie", 1977);
INSERT INTO Media (name, date_added, date_leaving, age_rating, language, genre, length_in_minutes, 
    company_id, media_type, year_of_release)
    VALUES ("Star Wars: Episode V - The Empire Strikes Back", '2022-11-01', NULL, 'PG', 'English',
    'Science Fiction', 124, 1, "Movie", 1980);
INSERT INTO Media (name, date_added, date_leaving, age_rating, language, genre, length_in_minutes, 
    company_id, media_type, year_of_release)
    VALUES ("Star Wars: Episode VI - Return of the Jedi", '2022-11-01', NULL, 'PG', 'English',
    'Science Fiction', 132, 1, "Movie", 1983);
INSERT INTO Media (name, date_added, date_leaving, age_rating, language, genre, length_in_minutes, 
    company_id, media_type, year_of_release)
    VALUES ("Raiders of the Lost Ark", '2022-11-01', NULL, 'PG', 'English',
    'Adventure', 115, 1, "Movie", 1981);

INSERT INTO Subscribers VALUES(1, "John Doe", "johndoe@gmail.com", "Standard", '2022-11-01', NULL);
INSERT INTO Subscribers VALUES(2, "Purdue Pete", "purduepete@purdue.edu", "Premium", '2022-11-01', NULL);

INSERT INTO Plan VALUES("Standard", 1000, 7.99);
INSERT INTO Plan VALUES("Premium", 1000, 14.99);

INSERT INTO Profile VALUES(1, 1, "John", "TV-MA");
INSERT INTO Profile VALUES(2, 1, "Timmy", "PG");

INSERT INTO Actor (name, country) VALUES("Harrison Ford", "USA");
INSERT INTO Actor (name, country) VALUES("Mark Hamill", "USA");

INSERT INTO Director (name, country) VALUES("Steven Spielberg", "USA");
INSERT INTO Director (name, country) VALUES("George Lucas", "USA");

INSERT INTO Company (name, country) VALUES('Disney', "USA");

INSERT INTO Media_Director VALUES(1, 2);
INSERT INTO Media_Director VALUES(4, 1);

INSERT INTO Media_Actor VALUES(1, 1);
INSERT INTO Media_Actor VALUES(2, 1);
INSERT INTO Media_Actor VALUES(3, 1);
INSERT INTO Media_Actor VALUES(4, 1);
INSERT INTO Media_Actor VALUES(1, 2);
INSERT INTO Media_Actor VALUES(2, 2);
INSERT INTO Media_Actor VALUES(3, 2);