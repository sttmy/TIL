-- ---해보기
-- bookstore 스키마 만들고
-- table 3개 만들기 (book, customer, order)
-- foreign key (custid) references Customer(custid)

CREATE DATABASE bookstore;

USE bookstore;

CREATE TABLE Book
( bookid INTEGER PRIMARY KEY,
	bookname VARCHAR(40),
    publisher VARCHAR(40),
    price INTEGER
    );

CREATE TABLE Customer
( custid INTEGER PRIMARY KEY,
	username VARCHAR(20),
    address VARCHAR(50),
    phone VARCHAR(20)
    );
    
CREATE TABLE Orders
( orderid INTEGER PRIMARY KEY,
	custid INTEGER,
    bookid INTEGER,
    saleprice INTEGER,
    orderdate date,
    FOREIGN KEY (custid) REFERENCES Customer(custid),
    FOREIGN KEY (bookid) REFERENCES Book(bookid)
    );  

INSERT INTO Book VALUES(1, '철학의 역사', '정론사', 7500);
INSERT INTO Book VALUES(2, '3D 모델링 시작하기', '한비사', 15000);
INSERT INTO Book VALUES(3, 'SQL의 이해', '새미디어', 2200);
INSERT INTO Book VALUES(4, '텐서플로우 시작', '새미디어', 3500);
INSERT INTO Book VALUES(5, '인공지능 개론', '정론사', 8000);
INSERT INTO Book VALUES(6, '파이썬 고급', '정론사', 8000);
INSERT INTO Book VALUES(7, '객체지향 Java', '튜링사', 20000);
INSERT INTO Book VALUES(8, 'C++ 중급', '튜링사', 18000);
INSERT INTO Book VALUES(9, 'Secure 코딩', '정보사', 7500);
INSERT INTO Book VALUES(10, 'Machine learning 이해', '새미디어', 32000);

SELECT * FROM book;


INSERT INTO Customer VALUES(1, '박지성','영국 맨체스타','010-1234-1010');
INSERT INTO Customer VALUES(2, '김연아','대한민국 서울','010-1223-3456');
INSERT INTO Customer VALUES(3, '장미란','대한민국 강원도','010-4878-1901');
INSERT INTO Customer VALUES(4, '추신수','대한민국 부산','010-8000-8765');
INSERT INTO Customer VALUES(5, '박세리','대한민국 대전', NULL);  -- null값은 그대로 삽입

SELECT * FROM Customer;


INSERT INTO Orders VALUES(1, 1, 1, 7500, str_to_date('2021-02-01', '%Y-%m-%d'));
INSERT INTO Orders VALUES(2, 1, 3, 44000, str_to_date('2021-02-03', '%Y-%m-%d'));
INSERT INTO Orders VALUES(3, 2, 5, 8000, str_to_date('2021-02-03', '%Y-%m-%d'));
INSERT INTO Orders VALUES(4, 3, 6, 8000, str_to_date('2021-02-04', '%Y-%m-%d'));
INSERT INTO Orders VALUES(5, 4, 7, 20000, str_to_date('2021-02-05', '%Y-%m-%d'));
INSERT INTO Orders VALUES(6, 1, 2, 15000, str_to_date('2021-02-07', '%Y-%m-%d'));
INSERT INTO Orders VALUES(7, 4, 8, 18000, str_to_date('2021-02-07', '%Y-%m-%d'));
INSERT INTO Orders VALUES(8, 3, 10, 32000, str_to_date('2021-02-08', '%Y-%m-%d'));
INSERT INTO Orders VALUES(9, 2, 10, 32000, str_to_date('2021-02-09', '%Y-%m-%d'));
INSERT INTO Orders VALUES(10, 3, 8, 18000, str_to_date('2021-02-10', '%Y-%m-%d'));
    
SELECT * FROM Orders;    