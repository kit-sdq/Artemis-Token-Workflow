# Artemis Token Workflow

Provides a login flow for applications that is analogous to Nextcloud [login flow v2](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2).

1. The application does an anonymous POST at `v1/login/flow/init/`. The endpoint returns a JSON object that follows the interface `FlowInitResponse`:
```typescript
interface PollingEndpoint {
    token: string;
    endpoint: string;
}

interface FlowInitResponse {
    poll: PollingEndpoint;
    login: string;
}
```
2. The application opens a browser at the URL that is defined by `login`. The user gets redirected to the specified SAML2 login provider.
3. The application polls the endpoint defined by `poll.endpoint` and uses `poll.token` as `token` query parameter. The endpoint returns 404 until the user is logged in. Once the user is logged in a 200 is returned together with a JSON object that follows the interface:
```typescript
interface FlowSuccessResponse {
    server: string;
    loginName: string;
    appPassword: string;
}
```

## Installation

Prerequisites:
- xmlsec (Path to `xmlsec1` can be adjusted in the config)

## Configuration
Rename the `.json.template` files in the `config` folder to `.json` and enter your settings according to the preconfigured schema.
The application first searches configuration in the dev/prod files depending on the `DJANGO_CONFIG` environment variable (default is `PROD`), then the base file at `base.json` is checked.

Never change `base.json`.

## Development

Set up your python environment using Poetry.

```bash
poetry install
```

### Run the development server

```bash
# Run the first few commands only once
# Generate the necessary tables
poetry run python manage.py migrate
# Create admin account
poetry run python manage.py createsuperuser

# Select development configuration (production is default or PROD)
export DJANGO_CONFIG=DEV
poetry run python manage.py runserver
```
