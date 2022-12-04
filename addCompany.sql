DROP PROCEDURE IF EXISTS addCompany;

DELIMITER //
CREATE PROCEDURE addCompany(IN company VARCHAR(50), OUT company_id INTEGER)
    BEGIN
        DECLARE insert_company VARCHAR(50);
        DECLARE new_id INTEGER;
        SET insert_company = company;
        
        SELECT MAX(T1.id) into new_id FROM (SELECT C.id FROM Company C) AS T1;
        SET new_id = new_id + 1;

        IF NOT EXISTS (SELECT C.name FROM Company C WHERE C.name = insert_company) THEN
            INSERT INTO Company(id, name) VALUES (new_id, insert_company);
            SET company_id = new_id;
            SELECT @company_id;
        ELSE 
            SELECT C.id into company_id FROM Company C WHERE C.name = insert_company;
            SELECT @company_id;
        END IF;

    END //
DELIMITER ;