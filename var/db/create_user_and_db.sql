CREATE USER "PINEGAP_DB_USER" WITH PASSWORD 'PINEGAP_DB_PASSWD_TO_CHANGE';
CREATE DATABASE "pinegap_db" WITH OWNER "PINEGAP_DB_USER";
ALTER ROLE "PINEGAP_DB_USER" SET client_encoding TO 'utf8';
ALTER ROLE "PINEGAP_DB_USER" SET default_transaction_isolation TO 'read committed';
-- ALTER ROLE "PINEGAP_DB_USER" SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE "pinegap_db" TO "PINEGAP_DB_USER";

