-- Init.db process
ALTER ROLE "PINEGAP_DB_USER" SET client_encoding TO 'utf8';
ALTER ROLE "PINEGAP_DB_USER" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "PINEGAP_DB_USER" SET timezone TO 'UTC';
--Permission
GRANT ALL PRIVILEGES ON DATABASE "pinegap_db" TO "PINEGAP_DB_USER";

--Alter Table Asset - Valor em Risco
ALTER TABLE public.assets ALTER COLUMN financeiro TYPE numeric(10) USING financeiro::numeric;

-- Create Table Currency
CREATE TABLE public.currencies_currency (
	code varchar NULL,
	"name" varchar NULL,
	symbol varchar NULL,
	factor varchar NULL,
	is_active bool NULL,
	is_base bool NULL,
	is_default bool NULL,
	info varchar NULL
);

-- Fill Table Currency
INSERT INTO public.currencies_currency (code,name,symbol,factor,is_active,is_base,is_default,info) VALUES
	 ('BRL','REAL','R$','1',true,true,true,'1');


--Permissions over Asset table
ALTER TABLE public.currencies_currency OWNER TO "PINEGAP_DB_USER";
GRANT ALL ON TABLE public.currencies_currency TO "PINEGAP_DB_USER";

BEGIN;

--Alter Table Asset - Valor em Risco
ALTER TABLE public.assets ALTER COLUMN financeiro TYPE numeric(10) USING financeiro::numeric;

-- Create Table Currency
CREATE TABLE public.currencies_currency (
        code varchar NULL,
        "name" varchar NULL,
        symbol varchar NULL,
        factor varchar NULL,
        is_active bool NULL,
        is_base bool NULL,
        is_default bool NULL,
        info varchar NULL
);

-- Fill Table Currency
INSERT INTO public.currencies_currency (code,name,symbol,factor,is_active,is_base,is_default,info) VALUES
         ('BRL','REAL','R$','1',true,true,true,'1');


--Permissions over Asset table
ALTER TABLE public.currencies_currency OWNER TO "PINEGAP_DB_USER";
GRANT ALL ON TABLE public.currencies_currency TO "PINEGAP_DB_USER";

COMMIT;

