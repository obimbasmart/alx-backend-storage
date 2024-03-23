-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
-- 
--     Procedure ComputeAverageScoreForUser is taking 1 input:
--     user_id, a users.id value (you can assume user_id is linked to an existing users)


-- calucate normal weighted average

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_avg INT;

    SELECT SUM(score * weight) / SUM(weight) INTO weighted_avg
    FROM corrections
    JOIN projects ON projects.id = project_id
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET average_score = weighted_avg
    WHERE users.id = user_id;
END;
$$
