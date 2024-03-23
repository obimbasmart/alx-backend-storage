-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

--      Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users user
    SET average_score = (
        SELECT SUM(score * weight) / SUM(weight)
        FROM corrections
        JOIN projects ON projects.id = project_id
        WHERE corrections.user_id = user.id
    );
END;
$$
