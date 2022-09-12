ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'REDACTED';
CREATE USER 'web'@'%' IDENTIFIED WITH mysql_native_password BY 'REDACTED';

USE palindrome;

CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO `users` (`email`, `password`) VALUES ("REDACTED@REDACTED", "REDACTED");

CREATE TABLE `tokens` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `token` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

GRANT INSERT, SELECT ON palindrome.tokens TO 'web'@'%';
GRANT SELECT ON palindrome.users TO 'web'@'%';
FLUSH PRIVILEGES;
