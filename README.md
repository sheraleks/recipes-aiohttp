# Recipes REST backend with aiohttp, motor and umongo

## Dependency
```
python 3.7.4
mongo 4.0.10
umongo 2.0.3
aiohttp 3.5.4
```

## Make commands

```
env             create python env
install         install requirements
test            run tests with pytest
run             run in local
run_in_docker   run in docker
```

## System interaction examples using HTTPie
OpenAPI specification in openapi.yaml
### Create user
```
http POST http://localhost:8080/users nickname=aleks password=aleks
```
answer
```
{
    "id": "60ee86c71a69b0edb2f969e5",
    "nickname": "aleks",
    "password": "aleks",
    "recipes_count": 0,
    "status": "active"
}
```
### Find user by id
```
http http://localhost:8080/users/60ee86c71a69b0edb2f969e5
```
answer
```
{
    "id": "60ee86c71a69b0edb2f969e5",
    "nickname": "aleks",
    "recipes_count": 1,
    "status": "active"
}
```
### Create recipe
```
http POST http://localhost:8080/recipes author_id='60ee86c71a69b0edb2f969e5' name='Pork' dish_type='second'
```
answer
```
{
    "author_id": "60ee86c71a69b0edb2f969e5",
    "created_date": "2021-07-14T06:43:56.537000+00:00",
    "dish_type": "second",
    "id": "60ee87ac1a69b0edb2f969e6",
    "likes_count": 0,
    "name": "Pork",
    "status": "active"
}
```
### Find recipe by id
```
http http://localhost:8080/recipes/60ee87ac1a69b0edb2f969e6
```
answer
```
{
    "author": {
        "id": "60ee86c71a69b0edb2f969e5",
        "nickname": "aleks",
        "status": "active"
    },
    "author_id": "60ee86c71a69b0edb2f969e5",
    "created_date": "2021-07-14T06:43:56.537000+00:00",
    "dish_type": "second",
    "id": "60ee87ac1a69b0edb2f969e6",
    "likes_count": 0,
    "name": "Pork",
    "status": "active"
}
```

### List top10 users by recipes count
```
http http://localhost:8080/users 
```
answer
```
[
    {
        "id": "60ee86c71a69b0edb2f969e5",
        "nickname": "aleks",
        "recipes_count": 2,
        "status": "active"
    },
    {
        "id": "60ee898a1a69b0edb2f969e9",
        "nickname": "test1",
        "recipes_count": 1,
        "status": "active"
    },
    {
        "id": "60ee897c1a69b0edb2f969e8",
        "nickname": "test",
        "recipes_count": 0,
        "status": "active"
    }
]
```

### List recipes sorted (descending) by name and with 'k' in name
```
http 'http://localhost:8080/recipes?sort_by=name&name_part=k&sort_order=descending'
```
answer
```
[
    {
        "author_id": "60ee86c71a69b0edb2f969e5",
        "created_date": "2021-07-14T06:43:56.537000+00:00",
        "dish_type": "second",
        "id": "60ee87ac1a69b0edb2f969e6",
        "likes_count": 0,
        "name": "Pork",
        "status": "active"
    },
    {
        "author_id": "60ee898a1a69b0edb2f969e9",
        "created_date": "2021-07-14T06:55:52.627000+00:00",
        "dish_type": "second",
        "id": "60ee8a781a69b0edb2f969eb",
        "likes_count": 0,
        "name": "Chicken",
        "status": "active"
    }
]
```