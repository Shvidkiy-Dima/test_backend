
# Test Backend

Integrated with http://otp.spider.ru/test/. INTEGRATION_SCHEDULE_MIN env var configures
how often fetch data and populate local DB (default 30min).

Get nearest companies -  /company/nearest/?coordinates=21,21. Company coordinates set up in admin panel.

Check it out - https://testbackendproject.herokuapp.com/

### Deploy
- Go to root project directory and run - docker-compose up --build
- Go to http://localhost:8000


### URLs

- / -Admin

- /logs/ -integ logs (dont work on heroku yet)

### API

- /user/registration/ POST {username, password}
- /user/get_token/ POST {username, password}
- /user/{id}/ GET

- /company/?is_active=True|False GET {POST DEL PATCH PUT} - need cred
- /category/ GET {POST DEL PATCH PUT} - need cred
- /product/?is_active=True|False&company=name&category=name&name=name GET {POST DEL PATCH PUT} - need cred

- /company/nearest/?coordinates=21,21 GET
