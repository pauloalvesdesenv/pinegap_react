#!/bin/bash

# Set Environment Variables - Devops by Bill
export POSTGRES_HOST=${POSTGRES_HOST:-db}
export RABBITMQ_HOST=${RABBITMQ_HOST:-rabbitmq}
export POSTGRES_PORT=${POSTGRES_PORT:-5432}
export RABBITMQ_PORT=${RABBITMQ_PORT:-5672}


echo "[+] Fase 1"


# Startup Time Rotation Base System - Devops by Bill
#echo "[+] Wait for DB Startup"
while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do sleep 1; done

#echo "[+] Wait for RabbitMQ Startup"
while !</dev/tcp/$RABBITMQ_HOST/$RABBITMQ_PORT; do sleep 1; done

echo "[+] Fase 2"

# Activate Environment
source env/bin/activate

# Collect static files
echo "[+] Collect static files"
python manage.py collectstatic --noinput

echo "[+] Fase 3"

#####################DROP TABLES ####################

#Drop Table Currencies - Devops by Bill
echo "[+] Drop Table Currencies to rebuild on Database"
python manage.py shell < var/bin/drop_table_currencies_db.py

#Drop Table Whitelabels - Devops by Bill
echo "[+] Drop Table Whitelabels to rebuild on Database"
python manage.py shell < var/bin/drop_table_whitelabel_db.py

################### DROP TABLES #####################

echo "[+] Fase 2"

################## INFRA OPERATIONS DJANGO ##########

#Swipe Django Migration Table in dabatase - Devops by Bill
echo "[+] Swipe Django Migration table on Database"
python manage.py shell < var/bin/swipe_column_migrations_db.py

#Correction Django Dabatase - Devops by Bill
echo "[+] Correction Django  table on Database"
python manage.py shell < var/bin/correction_django_content_table_db.py

###############  INFRA OPERATIONS DJANGO  ###########


##############  DEACTIVATED DEFINITELY #############

# Set to NULL  Asset Risk Value (Financeiro) Column - Devops by Bill
echo "[+] Set to Null  Asset Risk Value (Financeiro)"
python manage.py shell < var/bin/alter_colum_null.py

#Create Default_currency Column in Asset  table dabatase - Devops by Bill
echo "[+] Create default Currency Column in Asset table on Database"
python manage.py shell < var/bin/correction_default_currency_table_db.py

#Create Whitelabel  table dabatase - Devops by Bill
echo "[+] Create Whitelabel table on Database"
python manage.py shell < var/bin/create_whitelabel_table_db.py

#Create Currency table dabatase - Devops by Bill
echo "[+] Create Currency table on Database"
python manage.py shell < var/bin/create_table_db.py

# Set to ZERO  Asset Risk Value (Financeiro) Column - Devops by Bill
echo "[+] Set to ZERO  Asset Risk Value (Financeiro)"
python manage.py shell < var/bin/zeroed_db_financeiro_records.py

#Create Default_currency Column in Asset  table dabatase - Devops by Bill
echo "[+] Create default Currency Column in Asset table on Database"
python manage.py shell < var/bin/correction_default_currency_table_db.py

# Update Asset Risk Value (Financeiro) Column - Devops by Bill
echo "[+] Update Asset Risk Value (Financeiro)"
python manage.py shell < var/bin/alter_table_db.py

##############  DEACTIVATED DEFINITELY #############

echo "[+] Fase 3"

##############  PREPARE MIGRATION DB VALUES ########

# Correction Asset Risk Value in  (Financeiro) Column - Devops by Bill
echo "[+] Correction All Values in Asset Risk Value (Financeiro)"
python manage.py shell < var/bin/normalize_db_records.py

# Create Auxiliar (intermediate Column) - Devops by Bill
echo "[+] Create Auxiliar (intermediate Column"
python manage.py shell < var/bin/create_aux_table.py

echo "[Running] Trying to Copy"

# Copy data to (intermediate Column) - Devops by Bill
echo "[+] Copy data from 'financeiro' to (intermediate Column)"
python manage.py shell < var/bin/copy_fin_column.py


##############  PREPARE MIGRATION DB VALUES ########

echo "[+] Fase 4"

# Apply database migrations
echo "[+] Make database migrations"
python manage.py makemigrations
echo " - scans"
python manage.py makemigrations scans
echo " - findings"
python manage.py makemigrations findings
echo " - events"
python manage.py makemigrations events
echo " - whitelabels"
python manage.py makemigrations whitelabels
echo " - Assets"
python manage.py makemigrations assets

echo "[+] Fase 5"

# Apply database migrate
echo "[+] Apply database migrate"
python manage.py migrate whitelabels
python manage.py migrate assets
python manage.py migrate events
python manage.py migrate scans
python manage.py migrate findings
#manage.py migrate --fake contenttypes
manage.py migrate --fake currencies
python manage.py migrate  --fake-initial
python manage.py migrate

echo "[+] Fase 6"

############## ASSET RISK VALUE MIGRATION ##############

# Drop Original (Financeiro) column - Devops by Bill
echo "[+]  Drop Original 'Financeiro' column"
#python manage.py shell < var/bin/drop_fin_table.py

# Rename (Intermediate) Colum to (Financeiro) - Devops by Bill
echo "[+] Rename (Intermediate) Colum to (Financeiro)"
#python manage.py shell < var/bin/rename_aux_columm.py

############## ASSET RISK VALUE MIGRATION ##############

echo "[+] Fase 7"

############## IINSTALLING  MIGRATION ##############

# Fill Column Currency Table - Devops by Bill
echo "[+] Fill Column Currency Table"
python manage.py shell < var/bin/fill_currency_table_db.py

############## IINSTALLING  MIGRATION ##############



# Check for first install
#if [ ! -f status.created ]; then

# Create the default admin user e support user
echo "[+] Create the default admin user"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('bills', 'my@pinegap.io', 'djL9!KDr0QVuc6!1X@XR')" | python manage.py shell
#echo "[+] Create the default support user"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('suporte@pinegap.io', 'suporte@pinegap.io', 'WHm1kDCkc8W9gAH$%lfI')" | python manage.py shell
#  touch status.created
#fi

echo "[+] Fase 8"


# Check for first install
#if [ ! -f status.created ]; then

# Populate the db with default data
#echo "[+] Populate the db with data
python manage.py loaddata var/data/assets.AssetCategory.json
python manage.py loaddata var/data/engines.Engine.json
python manage.py loaddata var/data/engines.EnginePolicyScope.json
python manage.py loaddata var/data/engines.EnginePolicy.json
python manage.py loaddata var/data/whitelabels.path.json
python manage.py loaddata var/data/groups.json
python manage.py loaddata var/data/join_group.json

#touch status.created

echo "[+] settings Users "
python manage.py shell < utils/utils.py
#fi

echo "[+] Fase 9"


# Start Supervisord (Celery workers)
echo "[+] Start Supervisord (Celery workers)"
supervisord -c var/etc/supervisord.conf

# Start server
echo "[+] Starting server"
gunicorn -b 0.0.0.0:8003 app.wsgi:application --timeout 300
