ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'granite-numeric-canopener';
CREATE USER 'web'@'%' IDENTIFIED WITH mysql_native_password BY 'stingray-coleslaw-overbill';

USE palindrome;

CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO `users` (`email`, `password`) VALUES ("pasty-shrank-faction@celestial-stapling-captivate.org", "cloning-rising-amulet");

CREATE TABLE `tokens` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `token` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

GRANT INSERT, SELECT ON palindrome.tokens TO 'web'@'%';
GRANT SELECT ON palindrome.users TO 'web'@'%';
FLUSH PRIVILEGES;
