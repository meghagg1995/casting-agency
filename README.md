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

JWT's for user for all the 3 roles are included in the .env file for testing the API Endpoints. They are also added below:

<details>
  <summary>JWT of casting assistant, Click to expand!</summary>
  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImszaFIzVDdvQ3lwLWlYRVZnbF9QeSJ9.eyJpc3MiOiJodHRwczovL21lZ2hhZ2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmQ0Y2FmNjJkMDNjMGM2ZmUxYmNjMCIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg5NjE3NjIxLCJleHAiOjE1ODk3MDQwMjEsImF6cCI6IlNHNGpvUWEzREhJZjVLRTZKZm1wUVlUdGNDdklxeW9wIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.msfC8iLVcMMp3f30nb9vJJFuzSmtjcHzDA8xzZyvIDxuw7Wibk9U9BezYQIy8L8lcpnV4KnVG6iYF3DH55P57hYJzxepOZIyublUKrQUSTZMC5K0OYVY5MPl2c85V0m8TrvKhdbKQANYwQLTPecYp1yPC2bcQkD4JoB-Qku9eYxUaSn6RaXeIsSChvylia_smYPqF6WRcX5v3kfOJTA985jSHDUtabqKqd5P1w6AAYSSKae0264lM390bVuQK3c-1CdFAOqcunaNH2dGP5ejP-3GaRpF8wO7CWaOgLvTeTdfkyf6UKKwoSjm4cmDw5xMPWXvzuzUGayqkZ35xWJT_A
</details>

<details>
  <summary>JWT of casting director, Click to expand!</summary>
  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImszaFIzVDdvQ3lwLWlYRVZnbF9QeSJ9.eyJpc3MiOiJodHRwczovL21lZ2hhZ2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmQ0ZTAyMDU1YTRiMGM2ZmNmNjhkYSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg5NjE3NzA2LCJleHAiOjE1ODk3MDQxMDYsImF6cCI6IlNHNGpvUWEzREhJZjVLRTZKZm1wUVlUdGNDdklxeW9wIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsIm1vZGlmeTphY3RvcnMiLCJtb2RpZnk6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.0RUn9sx7R-OyptpsmtNXOBCS1bb8-GLg22yF_Dubo8JCgc_v13bV2_FkJs87ZTOBb8RKzh7_I_R-d4kL3nDWlBF1JyR-uA1PAVtVctb2gbqZ4_5QeWjAS2el7M9Aw5WoF6SDlDkjB755C_GF9TcPGsHqzBDQLthUjKaVnS6ZVR3s11gsYBIv9FYCTsYV_y_9I0xuwBRwl2ie_98UI7M_PlAKyJLWmB6t_g4oPhwHU4Aldmwj38xQ_9wSkmiPJoR_GS7644D4CwxXiSb3a9g315FZv739eF_sbp71OeqL9trQM8kA_VmFqnDr2Bnhw2JbV7rkrPh3R1wO8TCinofnag
</details>

<details>
  <summary>JWT of executive producer, Click to expand!</summary>
  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImszaFIzVDdvQ3lwLWlYRVZnbF9QeSJ9.eyJpc3MiOiJodHRwczovL21lZ2hhZ2cuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmQ0ZTFmNjJkMDNjMGM2ZmUxYzI1ZCIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg5NjE3NzU3LCJleHAiOjE1ODk3MDQxNTcsImF6cCI6IlNHNGpvUWEzREhJZjVLRTZKZm1wUVlUdGNDdklxeW9wIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiYWRkOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwibW9kaWZ5OmFjdG9ycyIsIm1vZGlmeTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.vJx7V1ETUpRV2WrCKUMHhRSYXfn5S1xZn9H1lF2izTONZ9cbF5eLhS3HaJhXyVDSRzRDaxyS0qOMBtuoCnH-UhE4nsiIqRbkMB9XWmuNgtol3HiT-bvTH-TAn2y__oFaWDg5-B8cJIfm-N_7U2oWrnybz-xzsXagKKTm4nBK7R-dUbnxmDgOYm-Gaji8gTc6ItkhiJpKTVgCzl3sYPGMp4-1ydLIE45iQJ6aAQuL9C63jUYId0WBLrd8_Qus9gKRnCxa4ifopKV8obUDo3DqY9plXX99qM6-tw-lkM8556YI7ziMQzpRNppTsHSbD2Go-EqpZw55ZG8S0x8qm0oZCw
</details>


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
### 10. DELETE /movies/\<movie_id>

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
#
### 11. POST /cast

Insert a many to many relationship between actors and movies, ie. insert actor and movie id's in association table.
#### Example request
```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"actor_id": 1, "movie_id": 1}' https://casting-agency-project.herokuapp.com/cast
```

- Request Arguments: **None**
- Request Headers: 
   - **Content-Type** (_application/json_)
   - **Authorization**
- Request Body:
  1. **integer** `actor_id` (<span style="color:red">*</span>required)
  2. **integer** `movie_id` (<span style="color:red">*</span>required)
- Requires permission: `add:movies`
- Returns: 
  1. Dict with following fields:
      - **string** `actor.name`
      - **string** `movie.title`
  2. **boolean** `success`

#### Example response
```js
{
    "actor": "Tom Cruise",
    "movie": "Mission Impossible",
    "success": true
}
```
#### Errors
If you try to create a new entry without a required field like `actor_id`, `movie_id`
it will throw a `400` error:

```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"actor_id": 1}' https://casting-agency-project.herokuapp.com/cast
```

will return

```js
{
    "error": 400,
    "message": "Bad Request",
    "success": false
}
```

If you try to create a new entry with a id of movie or actor that doesn't exsist in the database it will throw a `404` error:

```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"actor_id": 100, "movie_id": 5}' https://casting-agency-project.herokuapp.com/cast
```

will return

```js
{
    "error": 404,
    "message": "Resource Not Found",
    "success": false
}
```
