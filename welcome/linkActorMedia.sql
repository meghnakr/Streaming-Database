DROP PROCEDURE IF EXISTS linkActorMedia;

DELIMITER //
CREATE PROCEDURE linkActorMedia(IN media_id INTEGER, actor_id INTEGER)
    BEGIN
        IF NOT EXISTS (SELECT * FROM Media_Actor M WHERE M.media_id = media_id AND M.actor_id = actor_id) THEN
            INSERT INTO Media_Actor VALUES (media_id, actor_id);
        END IF;
    END //
DELIMITER ;