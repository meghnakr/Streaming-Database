DROP PROCEDURE IF EXISTS addDirector;

DELIMITER //
CREATE PROCEDURE addDirector(IN director VARCHAR(50), OUT director_id INTEGER)
    BEGIN
        DECLARE insert_director VARCHAR(50);
        DECLARE new_id INTEGER;
        SET insert_director = director;

        SELECT MAX(D.id) INTO new_id FROM Director D;
        SET new_id = new_id + 1;

        IF NOT EXISTS (SELECT D.name FROM Director D WHERE D.name = insert_director) THEN
            INSERT INTO Director(id, name) VALUES (new_id, insert_director);
            SET director_id = new_id;
            SELECT @director_id;
        ELSE
            SELECT D.id INTO director_id FROM Director D WHERE D.name = insert_director;
            SELECT @director_id;
        
        END IF;
    END //
DELIMITER ;