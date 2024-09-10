var/bin/update_db_migrations.sh# verlte() {
#     [  "$1" = "`echo -e "$1\n$2" | sort -V | head -n1`" ]
# }
#
# # Check version for compatibility, otherwise exit
# verlte `cat VERSION | cut -f1 -d" "` 1.5.4 && echo "Let's go" || { echo "Use current migration files. Exit now" ; exit; }

echo "-- Migrate django_celery_beat"
python manage.py migrate django_celery_beat

echo "-- Installed tables:"
echo "from django.db import connection ; print(connection.introspection.table_names()) " | python manage.py shell

echo "-- CHANGEEEEEEEEE!:"


python manage.py shell

ALTER TABLE public.assets ALTER COLUMN financeiro TYPE numeric(10) USING financeiro::numeric;
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

-- Permissions

ALTER TABLE public.currencies_currency OWNER TO "PINEGAP_DB_USER";
GRANT ALL ON TABLE public.currencies_currency TO "PINEGAP_DB_USER";

- Update DB

INSERT INTO public.currencies_currency (code,name,symbol,factor,is_active,is_base,is_default,info) VALUES
	 ('BRL','REAL','R$','1',true,true,true,'1');



if echo "from django.db import connection ; print('assets' in connection.introspection.table_names()) " | python manage.py shell | grep -q 'True'; then

    echo "-- Clean the django_migrations table"
    echo "from django.db import connection; cursor = connection.cursor(); cursor.execute('delete from django_migrations')" | python manage.py shell

    echo "-- Remove 'migrations' folders"
    rm -rf events/migrations
    rm -rf users/migrations
    rm -rf scans/migrations
    rm -rf assets/migrations
    rm -rf findings/migrations
    rm -rf rules/migrations
    rm -rf settings/migrations
    rm -rf whitelabels/migrations

    echo "-- Apply fake migrations for built-in apps"
    python manage.py migrate --fake

    echo "-- Run syncdb on every apps"
    python manage.py migrate events --run-syncdb
    python manage.py migrate users --run-syncdb
    python manage.py migrate scans --run-syncdb
    python manage.py migrate assets --run-syncdb
    python manage.py migrate findings --run-syncdb
    python manage.py migrate rules --run-syncdb
    python manage.py migrate settings --run-syncdb
    python manage.py migrate whitelabels --run-syncdb


    echo "-- Make migrations on every apps"
    python manage.py makemigrations events
    python manage.py makemigrations users
    python manage.py makemigrations scans
    python manage.py makemigrations assets
    python manage.py makemigrations findings
    python manage.py makemigrations rules
    python manage.py makemigrations settings
    python manage.py makemigrations whitelabels


    echo "-- Apply migration (fake initial)"
    python manage.py migrate --fake-initial
    python manage.py migrate whitelabels
    python manage.py migrate assets
    python manage.py migrate


#    echo "-- Apply assets migrations (from 1.6.0)"
#    cp var/migrations/assets/0002_asset_exposure.py assets/migrations/0002_asset_exposure.py
#    python manage.py migrate assets 0002
fi
