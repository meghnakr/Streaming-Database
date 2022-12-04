DROP PROCEDURE IF EXISTS addActor;

DELIMITER //
CREATE PROCEDURE addActor(IN actor VARCHAR(50), OUT actor_id INTEGER)
    BEGIN
        DECLARE insert_actor VARCHAR(50);
        DECLARE new_id INTEGER;
        SET insert_actor = actor;

        SELECT MAX(A.id) INTO new_id FROM Actor A;
        SET new_id = new_id + 1;

        IF NOT EXISTS (SELECT A.name FROM Actor A WHERE A.name = insert_actor) THEN
            INSERT INTO Actor(id, name) VALUES (new_id, insert_actor);
            SET actor_id = new_id;
            SELECT @actor_id;
        ELSE
            SELECT A.id INTO actor_id FROM Actor A WHERE A.name = insert_actor;
            SELECT @actor_id;
        
        END IF;
    END //
DELIMITER ;