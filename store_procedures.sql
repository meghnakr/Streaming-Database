DELIMITER //

CREATE PROCEDURE getNumNewSubs(IN mth_want INT)
BEGIN
    DECLARE mth_no INT;
    DECLARE cur_count INT;
    SET mth_no = 1;

    CREATE TABLE res(
        num INT,
        mth INT,
        df INT
    );

    ITR:LOOP
        IF mth_no > mth_want THEN
            LEAVE ITR;
        END IF;
        INSERT INTO res (SELECT COUNT(*), mth_no, df FROM (SELECT id, DATE_FORMAT(start_date, '%Y%m') AS df FROM Subscribers) AS s GROUP BY df
            HAVING PERIOD_DIFF(DATE_FORMAT(CURDATE(), '%Y%m'), df) = mth_no);
        SET mth_no = mth_no + 1;
    END LOOP;

    SELECT mth, num FROM res;
    DROP TABLE res;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE getNumLostSubs(IN mth_want INT)
BEGIN
    DECLARE mth_no INT;
    DECLARE cur_count INT;
    SET mth_no = 1;

    CREATE TABLE res(
        num INT,
        mth INT,
        df INT
    );

    ITR:LOOP
        IF mth_no > mth_want THEN
            LEAVE ITR;
        END IF;
        INSERT INTO res (SELECT COUNT(*), mth_no, df FROM (SELECT id, DATE_FORMAT(end_date, '%Y%m') AS df FROM Subscribers) AS s GROUP BY df
            HAVING PERIOD_DIFF(DATE_FORMAT(CURDATE(), '%Y%m'), df) = mth_no);
        SET mth_no = mth_no + 1;
    END LOOP;

    SELECT mth, num FROM res;
    DROP TABLE res;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE getNumLostMedia(IN mth_want INT)
BEGIN
    DECLARE mth_no INT;
    DECLARE cur_count INT;
    DECLARE temp_count INT;
    SET mth_no = 1;

    CREATE TABLE res(
        num INT,
        mth INT,
        df INT
    );

    ITR:LOOP
        IF mth_no > mth_want THEN
            LEAVE ITR;
        END IF;
        SET temp_count = 0;
        INSERT INTO res (SELECT COUNT(*), mth_no, df FROM (SELECT id, DATE_FORMAT(date_leaving, '%Y%m') AS df FROM Media WHERE date_added IS NOT NULL) AS s GROUP BY df
            HAVING PERIOD_DIFF(DATE_FORMAT(CURDATE(), '%Y%m'), df) = mth_no);
        SELECT num INTO temp_count FROM res WHERE mth = mth_no;
        IF temp_count IS NULL OR temp_count = 0 THEN
            INSERT INTO res VALUES(0, mth_no, 0);
        END IF;
        SET mth_no = mth_no + 1;
    END LOOP;

    SELECT mth, num FROM res;
    DROP TABLE res;
END //

DELIMITER ;


