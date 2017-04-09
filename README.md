# tasq-backend

### Setup
Install packages:
```sh
$ pip install -r requirements.txt
```

### Database
Creating database and user in PostgreSQL:
```sh
CREATE DATABASE tasq;
CREATE USER tasq WITH password ‘tasq‘;
GRANT ALL ON DATABASE tasq TO tasq;
```

### Database migrations
Run migration
```sh
$ python application.py db upgrade
```

### Generate fake data
```sh
$ python manage.py generate_fake
```

### Run dev server
```sh
$ python application.py runserver
```