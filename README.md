# Real Estate App
Real Estate public listings portal with private panel for realtors and admins.

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
