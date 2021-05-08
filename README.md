# crypto-backend

## Getting Started

1. Clone the repository
2. Create `env/backend.env` and `env/database.env` from the `*.env.template` files and update the `ALPHA_VANTAGE_API_KEY` environment variable
3. Build docker images where required
```
docker-compose build
```
4. Run the application/databases locally using
```
docker-compose up
```
5. Creation of Currency objects (USD and BTC) required for the demo is done by docker compose
6. To try the API's locally you will have to create the APIKey objects via admin or shell (steps in link: https://florimondmanca.github.io/djangorestframework-api-key/guide/#creating-and-managing-api-keys)
7. Use the API keys from above step to access the below APIs
```
curl --location --request GET 'http://127.0.0.1:8000/api/v1/quotes/?from_currency=BTC&to_currency=USD' --header 'Authorization: Api-Key <Insert API Key>'
```
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/quotes/?from_currency=BTC&to_currency=USD' --header 'Authorization: Api-Key <Insert API Key>'
```

## Possible Improvements

1. Integrate various code QA tools (https://github.com/PyCQA)
2. Get to at least 95% test coverage from 35%
3. Setup dependency/package management tools
4. Make the django application production ready i.e. `SECRET_KEY` hardcoded, `DEBUG` mode off, gunicorn as web server, etc
5. Proper documentation of APIs as OpenAPI schemas
