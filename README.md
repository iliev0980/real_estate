# Real Estate App
Real Estate listings portal with private panel for realtors and admins.

---
# Install [Python](https://www.python.org/downloads/)

# Install [Docker](https://docs.docker.com/engine/install/)

# Make the entrypoints ececutable
`chmod +x entrypoint.sh`

# Build the image:
`docker-compose build`

# Once the image is built, run the container:
`docker-compose up -d`

# Run the migrations:

`docker-compose exec web python manage.py migrate --noinput`
  
# Ensure that all the migrations are up-to date
`docker-compose exec web python manage.py makemigrations`

# Make the migrations
`docker-compose exec web python manage.py migrate --noinput`

# Ensure that all the migrations are up-to date
`docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations`

# Make the migrations
`docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`

# Collect the static files
`docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`

# populate dump data

`docker-compose exec web python manage.py loaddata realtors.json`
`docker-compose exec web python manage.py loaddata listings.json`

## If you need to create an admin user run the next command and follow the instructions in the console
`docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser`

#### If you want to change the password for the email that is used to send archived invoices to the accoounting edit the EMAIL_PASSWORD variable in .env.prod file
#### If you want to change the email address change EMAIL_HOST_USER variable in gsoft_erp_invoices/settings.py
#### If you want to change the accounting email change the ACCOUNTING_EMAIL variable in gsoft_erp_invoices/settings.py