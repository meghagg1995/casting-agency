# FSND: CASTING AGENCY

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test.py`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

#
## Local Setup

Make sure you `cd` into the correct folder before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```bash
  $ pip install virtualenv
  $ virtualenv venv
  $ source venv/scripts/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

3. Create databases
```bash
$ createdb casting-agency
$ createdb casting-agency-test
```

4. Run the development server:
  ```bash 
  $ python app.py
  ```

5. To execute tests, run
```bash 
$ python test.py
```
If you choose to run all tests, it should give this response:

```bash
$ python test_app.py
........................
----------------------------------------------------------------------
Ran 24 tests in 44.718s

OK
```
**Note:** If testing the API locally make some **POST** requests for actors and movies before **GET**, **PATCH**, **DELETE** requests because the database is **initially empty**.

## Authentication

All API Endpoints are decorated with Auth0 permissions.


## Roles

They are 3 Roles with the following permissions:

1. Casting Assistant:
  - GET /actors (view:actors): Can get all actors from database
  - GET /movies (view:movies): Can get all movies from database
  - GET /actors/actor_id (view:actors): Can get particular actor from database
  - GET /movies/movie_id (view:movies): Can get particular movie from database
2. Casting Director 
  - All permissions a Casting Assistant has and…
  - POST /actors (add:actors): Can post new actors to database
  - PATCH /actors/actor_id (modify:actors): Can modify existing actors in database
  - DELETE /actors/actor_id (delete:actors): Can delete existing actors from database
  - PATCH /movies/movie_id (modify:movies): Can modify existing movies in database
3. Exectutive Dircector 
  - All permissions a Casting Director has and…
  - POST /movies (add:movies): Can post new movies to database
  - DELETE /movies/movie_id (delete:movies): Can delete existing moties from database

In your API Calls, JWT token for a particular user who is assigned a particular role is passed, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).


## API Documentation

### Base URL

**https://casting-agency-project.herokuapp.com**

#
### 1. GET /actors

GET all actors present in the database, along with their movies.

#### Example request
```
curl -X GET -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/actors
```
- Fetches all actors from the database
- Request Arguments: **None**
- Request Headers: **Authorization**
- Requires permission: `view:actors`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
      - **list** `movies`
  2. **boolean** `success`

#### Example response
```js
{
    "actors": [
        {
            "age": 50,
            "gender": "Male",
            "id": 1,
            "movies": [
                {
                    "id": 1,
                    "title": "Mission Impossible"
                }
            ],
            "name": "Tom Cruise"
        },
        {
            "age": 42,
            "gender": "Male",
            "id": 2,
            "movies": [
                {
                    "id": 4,
                    "title": "The Hunger Games"
                }
            ],
            "name": "Matt Damon"
        }
    ],
    "success": true
}
```
#### Errors
If you try to fetch without giving Authorization header,

```
$ curl -X GET https://casting-agency-project.herokuapp.com/actors
```

will return the following with status code 401

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 2. GET /actors/\<actor_id>

GET actor with corresponding actor_id from the database
#### Example request
```
curl -X GET -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/actors/1
```
- Fetches particular actor from database
- Request Arguments: **integer** `id of actor you want to view`
- Request Headers: **Authorization**
- Requires permission: `view:actors`
- Returns: 
  1. Dict of particular actor with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
      - **list** `movies`
  2. **boolean** `success`

#### Example response
```js
{
    "actor": {
        "age": 50,
        "gender": "Male",
        "id": 1,
        "movies": [
            {
                "id": 1,
                "title": "Mission Impossible"
            }
        ],
        "name": "Tom Cruise"
    },
    "success": true
}
```
#### Errors
If you try to fetch without giving Authorization header,

```
curl -X GET https://casting-agency-project.herokuapp.com/actors/1
```

will return the following with status code `401`

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 3. POST /actors

Insert a new actor in the database.
#### Example request
```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"name": "James Bond","age": 65, "gender": "Male"}' https://casting-agency-project.herokuapp.com/actors
```

- Request Arguments: **None**
- Request Headers: 
   - **Content-Type** (_application/json_)
   - **Authorization**
- Request Body:
  1. **string** `name` (<span style="color:red">*</span>required)
  2. **integer** `age` (<span style="color:red">*</span>required)
  3. **string** `gender` (<span style="color:red">*</span>required)
- Requires permission: `add:actors`
- Returns: 
  1. Dict of particular actor with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`

#### Example response
```js
{
    "actor": {
        "age": 75,
        "gender": "Male",
        "id": 11,
        "name": "James Bond"
    },
    "success": true
}
```
#### Errors
If you try to create a new actor without a required field like `name`, `age` or `gender`
it will throw a `400` error:

```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"age": 65, "gender": "Male"}' https://casting-agency-project.herokuapp.com/actors
```

will return

```js
{
    "error": 400,
    "message": "Bad Request",
    "success": false
}
```

#
### 4. PATCH /actors/\<actor_id>

Modify an existing actor in the database
#### Example request
```
curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"age": 56}' https://casting-agency-project.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id of the actor to update`
- Request Headers: 
  - **Content-Type** (_application/json_)
  - **Authorization**
- Requires permission: `modify:actors`
- Request Body
  1. **string** `name` 
  2. **integer** `age` 
  3. **string** `gender`
- Returns: 
  1. Dict of particular actor with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`
#### Example response
```js
{
    "actor": {
        "age": 56,
        "gender": "Male",
        "id": 1,
        "name": "Tom Cruise"
    },
    "success": true
}
```
#### Errors
If you try to update an actor with a non existent id it will throw a `404` error:

```
curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"age": 56}' https://casting-agency-project.herokuapp.com/actors/100
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```
Additionally, trying to update an actor without giving Authorization header, will return the following with status code `401`,

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 5. DELETE /actors/\<actor_id>

Delete an existing actor from the database
#### Example Request
```
curl -X DELETE -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/actors/11
```

- Request Arguments: **integer** `id of actor to delete`
- Request Headers:
  - **Authorization**
- Requires permission: `delete:actors`
- Returns: 
  1. **integer** `id of deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 11,
    "success": true
}
```
#### Errors
If you try to delete actor with a non existing id, it will throw an `404` error:

```
curl -X DELETE -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/actors/100
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```


#
### 6. GET /movies

GET all movies present in the database, along with their actors.

#### Example request
```
curl -X GET -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/movies
```
- Fetches all movies from the database
- Request Arguments: **None**
- Request Headers: **Authorization**
- Requires permission: `view:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `title`
      - **integer** `release_year`
      - **list** `actors`
  2. **boolean** `success`

#### Example response
```js
{
    "movies": [
        {
            "actors": [
                {
                    "id": 1,
                    "name": "Tom Cruise"
                }
            ],
            "id": 1,
            "release_year": 2021,
            "title": "Mission Impossible"
        },
        {
            "actors": [
                {
                    "id": 3,
                    "name": "Dwayne Johnson"
                },
                {
                    "id": 4,
                    "name": "Anne Hathaway"
                }
            ],
            "id": 2,
            "release_year": 2019,
            "title": "Jumanji"
        }
    ],
    "success": true
}
```
#### Errors
If you try to fetch without giving Authorization header,

```
$ curl -X GET https://casting-agency-project.herokuapp.com/movies
```

will return the following with status code 401

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 7. GET /movies/\<movie_id>

GET movie with corresponding movie_id from the database
#### Example request
```
curl -X GET -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/movies/1
```
- Fetches particular movie from database
- Request Arguments: **integer** `id of movie you want to view`
- Request Headers: **Authorization**
- Requires permission: `view:movies`
- Returns: 
  1. Dict of particular movie with following fields:
      - **integer** `id`
      - **string** `title`
      - **integer** `release_year`
      - **list** `actors`
  2. **boolean** `success`

#### Example response
```js
{
    "movie": {
        "actors": [
            {
                "id": 1,
                "name": "Tom Cruise"
            }
        ],
        "id": 1,
        "release_year": 2021,
        "title": "Mission Impossible"
    },
    "success": true
}
```
#### Errors
If you try to fetch without giving Authorization header,

```
curl -X GET https://casting-agency-project.herokuapp.com/movies/1
```

will return the following with status code `401`

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 8. POST /movies

Insert a new movie in the database.
#### Example request
```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"title": "GodFather", "release_year": 1999}' https://casting-agency-project.herokuapp.com/movies
```

- Request Arguments: **None**
- Request Headers: 
   - **Content-Type** (_application/json_)
   - **Authorization**
- Request Body:
  1. **string** `title` (<span style="color:red">*</span>required)
  2. **integer** `release_year` (<span style="color:red">*</span>required)
- Requires permission: `add:movies`
- Returns: 
  1. Dict of particular movie with following fields:
      - **integer** `id`
      - **string** `title`
      - **integer** `release_year`
  2. **boolean** `success`

#### Example response
```js
{
    "movie": {
        "id": 9,
        "release_year": 1999,
        "title": "Godfather"
    },
    "success": true
}
```
#### Errors
If you try to create a new movie without a required field like `title`, `release_year`
it will throw a `400` error:

```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"title": "Mr. X"}' https://casting-agency-project.herokuapp.com/movies
```

will return

```js
{
    "error": 400,
    "message": "Bad Request",
    "success": false
}
```

#
### 9. PATCH /movies/\<movie_id>

Modify an existing movie in the database
#### Example request
```
curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"release_year": 2007}' https://casting-agency-project.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id of the movie to update`
- Request Headers: 
  - **Content-Type** (_application/json_)
  - **Authorization**
- Requires permission: `modify:movies`
- Request Body
  1. **string** `title` 
  2. **integer** `release_year` 
- Returns: 
  1. Dict of particular movie with following fields:
      - **integer** `id`
      - **string** `title`
      - **integer** `release_year`
  2. **boolean** `success`
#### Example response
```js
{
    "movie": {
        "id": 1,
        "release_year": 2007,
        "title": "Mission Impossible"
    },
    "success": true
}
```
#### Errors
If you try to update an movie with a non existent id it will throw a `404` error:

```
curl -X PATCH -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"release_year": 2007}' https://casting-agency-project.herokuapp.com/movies/100
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```
Additionally, trying to update an movie without giving Authorization header, will return the following with status code `401`,

```js
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

#
### 4. DELETE /movies/\<movie_id>

Delete an existing movie from the database
#### Example Request
```
curl -X DELETE -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/movies/8
```

- Request Arguments: **integer** `id of movie to delete`
- Request Headers:
  - **Authorization**
- Requires permission: `delete:movies`
- Returns: 
  1. **integer** `id of deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 8,
    "success": true
}
```
#### Errors
If you try to delete movie with a non existing id, it will throw an `404` error:

```
curl -X DELETE -H "Authorization: Bearer <JWT>" https://casting-agency-project.herokuapp.com/movies/100
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```
