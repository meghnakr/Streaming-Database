DROP PROCEDURE IF EXISTS getActorId;

DELIMITER //
CREATE PROCEDURE getActorId(IN actor VARCHAR(50), OUT actor_id INTEGER)
    BEGIN
        DECLARE id INTEGER;
        SET id = -1;

        SELECT MAX(T1.Aid) INTO id FROM (SELECT A.id AS Aid FROM Actor A WHERE A.name = actor) AS T1;

        SET actor_id = id;
        SELECT @actor_id;
    END //
DELIMITER ;