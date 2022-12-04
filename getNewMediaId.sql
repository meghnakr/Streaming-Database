DROP PROCEDURE IF EXISTS getNewMediaId;

DELIMITER //
CREATE PROCEDURE getNewMediaId(OUT media_id INTEGER)
    BEGIN
        DECLARE id INTEGER;
        SET id = -1;

        SELECT MAX(M.id) into id FROM Media M;
        SET id = id + 1;
        SET media_id = id;
        SELECT @media_id;
    END //
DELIMITER ;