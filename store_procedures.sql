DELIMITER //

CREATE PROCEDURE getNumNewSubs(IN mth_want INT)
BEGIN
    DECLARE cur_mth INT;
    DECLARE mth_no INT;
    DECLARE cur_count INT;

    ITR:LOOP
        IF cur_mth > mth_want THEN
            LEAVE ITR;
        END IF;
        SELECT COUNT(*) INTO cur_count FROM Subscribers s HAVING DATEDIFF(MONTH, s.start_date, GETDATE()) = mth_no;
        SET mth_no = mth_no + 1;
        SELECT cur_mth, cur_count;
    END LOOP;
END //

DELIMITER ;