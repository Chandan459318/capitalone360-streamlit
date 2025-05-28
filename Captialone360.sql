CREATE DATABASE capitalone360;

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;


SELECT * FROM capitalone360.capitalone_mock_transactions LIMIT 10;

SELECT * FROM capitalone360.capitalone_fraud_detected LIMIT 10;

SELECT * FROM capitalone360.capitalone_user_segments LIMIT 10;

