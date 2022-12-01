DROP PROCEDURE IF EXISTS getMediaId;

DELIMITER //
CREATE PROCEDURE getMediaId(IN media VARCHAR(50), OUT media_id INTEGER)
    BEGIN
        DECLARE id INTEGER;
        SET id = -1;

        SELECT MAX(T1.Mid) INTO id FROM (SELECT M.id AS Mid FROM Media M WHERE M.name = media) AS T1;

        SET media_id = id;
        SELECT @media_id;
    END //
DELIMITER ;