# Psywerx.net

[![CircleCI](https://circleci.com/gh/Psywerx/psywerx.svg?style=svg)](https://circleci.com/gh/Psywerx/psywerx)
[![codecov](https://codecov.io/gh/psywerx/psywerx/branch/master/graph/badge.svg)](https://codecov.io/gh/psywerx/psywerx)


## Dev environment

```
$ docker-compose up -d
$ docker-compose exec psywerx bash # You are now in the psywerx container
# mysql -uroot -proot -hdb -e 'create database psywerx' # create the database
# python manage.py syncdb # set up the database tables
# python manage.py runserver 0.0.0.0:8000 # start the server
```

Testing codereivew.chat # test 2
