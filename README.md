# API for Bloggers Social Network

### Demo
- Web site https://yatube.w2c.net.eu.org/
- API https://yatube.w2c.net.eu.org/api/v1/
- Documentation https://yatube.w2c.net.eu.org/redoc/

![example workflow](https://github.com/web2cap/api_final_yatube/actions/workflows/master_yatube_workflow.yml/badge.svg)


### Project details:

Built on Django and Django Rest Framework
 
The project allows you to view and publish author's articles, by category.

There is registration and authorization of users.

An authorized user can leave reviews on articles and comments on reviews, subscribe to authors and manage their subscriptions.

This is the final version of two projects in Docker with CI / CD deploy
- Bloggers Social Network https://github.com/web2cap/hw05_final/
- API for Bloggers Social Network https://github.com/web2cap/api_yatube
Final version of this project is in Docker compose with CI/CD deploy


## Technology:

- Python and Django
- Rest Framework
- JWTAuthentication and djoser
- Postgres
- Bootstrap
- Pytest
- Docker and Docker compose
- Github actions


## Local installation
- Install docker and docker compose
```
git clone https://github.com/web2cap/api_final_yatube.git
cd api_final_yatube/infra
```

 - Create .env file by example:

 ```
ST_SECRET_KEY="" # Django Secret Key
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME= # YOUR_DB_NAME
DB_HOST=yatube_db
DB_PORT=5432
DB_USER= # YOUR_DB_USER
DB_PASSWORD= # YOUR_DB_PASSWORD
 ```

```
docker compose up -d
docker compose exec yatube_db psql -Upostgres
create role YOUR_DB_USER with login;
alter role YOUR_DB_USER with encrypted password 'YOUR_DB_PASSWORD';
alter user YOUR_DB_USER createdb;
create database YOUR_DB_NAME owner YOUR_DB_USER;

docker compose exec yatube_web python manage.py migrate
docker compose exec yatube_web python manage.py collectstatic --no-input
```

- You can create superuser
```
docker compose exec yatube_web python manage.py createsuperuser
```
- Go to website http://localhost:800/


## Documentation
When you launch the project, documentation for the Yatube API will be available at /redoc/.
The documentation describes how your API should work.
The documentation is in Redoc format.
* Documentation in Russian from the customer


## Examples of API requests and responses:
| Resource | Type | Path | Transferred data (JSON) |
| ------ | ------ | ------ | ------ |
| Get an API token | POST | /api/v1/jwt/create/ | {"username":"","password":""}

#### Answer:
```
{
    "refresh": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "access": "eyeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
}
```

| Resource | Type | Path |
| ------ | ------ | ------ |
| Get List of Posts | GET | /api/v1/posts/ |

#### Answer:
```
[
    {
        "id": 1,
        "text": "In the evening we gathered at the editorial office to talk about the theatre. Everyone likes the project.",
        "pub_date": "2022-04-21T11:22:03.167305Z",
        "author": "test",
        "image": null
        group: 1
    }
]
```

| Resource | Type | Path | Transferred data (JSON) |
| ------ | ------ | ------ | ------ |
| Add post | POST | /api/v1/posts/ | {"text": "","group": ""}

#### Answer:
```
{
    "id": 14,
    "text": ""In the evening we gathered at the editorial office to talk about the theatre. Everyone loves the project.
    "author": "anton",
    "image": null
    group: 1
    "pub_date": "2021-06-01T08:47:11.084589Z"
}
```
http://localhost:8000/api/v1/follow/


## Endpoints
| Path | Type | Description |
| ------ | ------ | ------ |
| api/v1/jwt/create/ | (POST) | pass login and password, get refresh, access token |
| api/v1/jwt/refresh/ | (POST) | pass refresh token, get access token |
| api/v1/jwt/verify/ | (POST) | pass access token for validation |
| api/v1/posts/ | (GET, POST) | get a list of all posts or create a new post |
| api/v1/posts/{post_id}/ | (GET, PUT, PATCH, DELETE) | getting, editing or deleting a post by id |
| api/v1/groups/ | (GET) | get a list of all groups |
| api/v1/groups/{group_id}/ | (GET) | get information about the group by id |
| api/v1/posts/{post_id}/comments/ | (GET, POST) | get a list of all post comments with id=post_id or create a new one by specifying the id of the post we want to comment on |
| api/v1/posts/{post_id}/comments/{comment_id}/ | (GET, PUT, PATCH, DELETE) | getting, editing or deleting a comment by id for a post with id=post_id |
| api/v1/follow/ | (GET) | returns all subscriptions of the user who made the request |
| api/v1/follow/ | (POST) | subscription of the user on behalf of which the request was made to the user passed in the body of the request |


### Author:

Pavel Koshelev