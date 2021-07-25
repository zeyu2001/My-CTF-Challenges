USE starcereal;

CREATE TABLE admins (email VARCHAR(255), password VARCHAR(255));
CREATE USER 'web'@'%' IDENTIFIED BY 'e3d5004f6d8fbd9ace33add1fcdb61a67e0ada23b7559396d2fd2af88d53a84b';

GRANT SELECT ON starcereal.admins to 'web'@'%';
FLUSH PRIVILEGES;
