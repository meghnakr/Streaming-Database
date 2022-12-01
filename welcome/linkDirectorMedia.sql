DROP PROCEDURE IF EXISTS linkDirectorMedia;

DELIMITER //
CREATE PROCEDURE linkDirectorMedia(IN media_id INTEGER, director_id INTEGER)
    BEGIN
        IF NOT EXISTS (SELECT * FROM Media_Director M WHERE M.media_id = media_id AND M.director_id = director_id) THEN
            INSERT INTO Media_Director VALUES (media_id, director_id);
        END IF;
    END //
DELIMITER ;