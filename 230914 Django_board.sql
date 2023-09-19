USE pyweb;

# 페이지나누기를 위한 저장프로시저
DELIMITER $$
DROP PROCEDURE if EXISTS loopInsert$$

CREATE PROCEDURE loopInsert()
	BEGIN 
	DECLARE i int DEFAULT 1;
	DELETE FROM board_board;
	while i<=991 do
		INSERT INTO board_board(IDX, writer, TITLE, CONTENT, hit, post_date, filesize, down)
		VALUES (i, CONCAT('kim', i), CONCAT('제목',i), CONCAT('내용',i), 0, NOW(), 0,0);
		SET i = i+1;
	END while;
END$$

DELIMITER $$

CALL LoopInsert 

select * from board_board;