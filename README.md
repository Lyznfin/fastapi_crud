# Simple CRUD API using fastapi

not much, but this repository covers, something like, beginner-full-project-structure kind of stuff for an app
- authentications covers data validations for several http operations using pydantic
- serializers is used to convert data from the database into a valid json
- routers contain all of the endpoints, returns valid json to client
- tests serve unit test that covers all of the endpoints
- models will store the database table schema, sessions, and dependency (so that we dont have to redeclare session in each router)
- main will just serve as a shortcut to run the server

speaking of running the server, here is how
`git clone https://github.com/Lyznfin/fastapi_crud`
`cd fastapi_crud`
`fastapi dev main.py`
