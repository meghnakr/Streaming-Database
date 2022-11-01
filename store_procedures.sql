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