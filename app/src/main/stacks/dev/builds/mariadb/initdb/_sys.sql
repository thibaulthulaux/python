SET time_zone = '+00:00';

-- Create Prometheus Exporter database user
-- The user should have PROCESS, SELECT, REPLICATION CLIENT grants
USE sys;
CREATE USER 'mysqld_exporter'@'localhost' IDENTIFIED BY 'StrongPassword' WITH MAX_USER_CONNECTIONS 2;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'mysqld_exporter'@'localhost';
FLUSH PRIVILEGES;
-- If you have a Master-Slave database architecture, create user on the master servers only
-- WITH MAX_USER_CONNECTIONS 2 is used to set a max connection limit for the user to avoid overloading the server with monitoring scrapes under heavy load.