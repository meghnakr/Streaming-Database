DROP PROCEDURE IF EXISTS getDirectorId;

DELIMITER //
CREATE PROCEDURE getDirectorId(IN director VARCHAR(50), OUT director_id INTEGER)
    BEGIN
        DECLARE id INTEGER;
        SET id = -1;

        SELECT MAX(T1.Did) INTO id FROM (SELECT D.id AS Did FROM Director D WHERE D.name = director) AS T1;

        SET director_id = id;
        SELECT @director_id;
    END //
DELIMITER ;