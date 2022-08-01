# API for Bloggers Social Network
Built on Django Rest Framework
 
The project allows you to view and publish author's articles, by category.

There is registration and authorization of users.

An authorized user can leave reviews on articles and comments on reviews, subscribe to authors and manage their subscriptions.

Bloggers Social Network https://github.com/web2cap/hw05_final/


## Technology:

-Python and Django
- Rest Framework
- JWTAuthentication and djoser

## Installation
- Clone the repository
- Create and activate virtual environment
- Install all required packages from requirements.txt.
- Apply migrations

## Documentation
When you launch the project, documentation for the Yatube API will be available at /redoc/.
The documentation describes how your API should work.
The documentation is in Redoc format.


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