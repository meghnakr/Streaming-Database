DROP PROCEDURE IF EXISTS addDirector;

DELIMITER //
CREATE PROCEDURE addDirector(IN director VARCHAR(50))
    BEGIN
        DECLARE insert_director VARCHAR(50);
        SET insert_director = director;

        IF NOT EXISTS (SELECT A.name FROM Director A WHERE A.name = insert_director) THEN
            INSERT INTO Director(name) VALUES (insert_director);
        END IF;
    END //
DELIMITER ;