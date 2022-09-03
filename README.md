# Artemis Token Workflow

Provides a login flow for applications that is analogous to Nextcloud [login flow v2](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html#login-flow-v2).

1. The application does an anonymous POST at `/flow/init`. The endpoint returns a JSON object that follows the interface `FlowInitResponse`:
```typescript
interface PollingEndpoint {
    endpoint: string;
    token: string;
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

poetry run python manage.py runserver
```
