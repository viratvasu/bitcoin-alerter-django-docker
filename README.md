## How to setup locally
1. It's running on docker so please do install docker
2. First build image by `docker-compose --build`
2. Then run `sudo docker-compose run web python manage.py migrate` which will do all the mirations
3. Then run server by just typing `docker-compose up`

## API docs
### Signup

Route `/signup/`

Method `POST`

<details><summary>Request</summary>
<p>

```json
{
    "username":"test",
    "password":"test"
}
```
</p>
</details>

<details><summary>Response</summary>
<p>

```json
{
    "message": "Account created succesfully"
}
```
OR

```json
{
    "message": "username or password is missing"
}
```
</p>
</details>


Comments - 
- username, password are mandatory

<hr>

### Login

Route `/api/token/`

Method `POST`

<details><summary>Request</summary>
<p>

```json
{
    "username":"test",
    "password":"test"
}
```
</p>
</details>

<details><summary>Response</summary>
<p>

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Njc0MDUyMywiaWF0IjoxNjU2NjU0MTIzLCJqdGkiOiI3ZmJjNTRjMWViM2I0YzU1Yjc4ZDZiNDJkZDIxM2I3NCIsInVzZXJfaWQiOjF9.1zDxMjEklOGY0XkfaAY9XaaD6l8RIZTeDcGYgfz5V8E",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3OTUwMTIzLCJpYXQiOjE2NTY2NTQxMjMsImp0aSI6ImY0MDA1NjkwZTkwZTQ4ZTBiN2FlYmFiYmRiYzZhMWVlIiwidXNlcl9pZCI6MX0.nnCUf18wC8-7BTwVoOjJ2mDzYv1HcipcYfT_VQu1l3k"
}
```
OR

```json
{
    "detail": "No active account found with the given credentials"
}
```
</p>
</details>


Comments - 
- username, password are mandatory

<hr>

### Create Alert

Route `/create_alert/`

Method `POST`

<details><summary>Request</summary>
<p>

```json
{
    "price":20356
}
```
</p>
</details>

<details><summary>Response</summary>
<p>

```json
{
    "message": "Alert created succesfully"
}
```
OR

```json
{
    "message": "Price required to set alert"
}
```
</p>
</details>


Comments - 
- price is mandatory

<hr>

### Delete Alert

Route `/delete_trigger/`

Method `POST`

<details><summary>Request</summary>
<p>

```json
{
    "id":2
}
```
</p>
</details>

<details><summary>Response</summary>
<p>

```json
{
    "message": "Alert deleted succesfully"
}
```
OR

```json
{
    "message": "Alert not found with given id"
}
```
</p>
</details>


Comments - 
- id is mandatory

<hr>

### Get all Alert

Route `/get_all_alerts/?page=3`

Method `POST`

<details><summary>Request</summary>
<p>

```json
{}
```

OR

```json
{
    "status":"Deleted"
}
```
</p>
</details>

<details><summary>Response</summary>
<p>

```json
{
    "count": 2,
    "data": [
        {
            "id": 1,
            "price": 2000.0,
            "status": "Deleted",
            "created_at": "2022-07-01 01:16:59"
        },
        {
            "id": 2,
            "price": 1000.0,
            "status": "Deleted",
            "created_at": "2022-07-01 01:16:59"
        }
    ]
}
```
OR

```json
{
    "count": 7,
    "message": "page_no is not valid"
}
```
</p>
</details>


Comments - 
- status is optinal
