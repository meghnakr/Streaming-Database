DROP PROCEDURE IF EXISTS addActor;

DELIMITER //
CREATE PROCEDURE addActor(IN actor VARCHAR(50))
    BEGIN
        DECLARE insert_actor VARCHAR(50);
        SET insert_actor = actor;

        IF NOT EXISTS (SELECT A.name FROM Actor A WHERE A.name = insert_actor) THEN
            INSERT INTO Actor(name) VALUES (insert_actor);
        END IF;
    END //
DELIMITER ;