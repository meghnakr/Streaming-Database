DROP PROCEDURE IF EXISTS addCompany;

DELIMITER //
CREATE PROCEDURE addCompany(IN company VARCHAR(50))
    BEGIN
        DECLARE insert_company VARCHAR(50);
        SET insert_company = company;

        IF NOT EXISTS (SELECT C.name FROM Company C WHERE C.name = insert_company) THEN
            INSERT INTO Company(name) VALUES (insert_company);
        END IF;
    END //
DELIMITER ;