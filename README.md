# Shrinkr

Shrinkr is a URL shortener backend built with FastAPI and Apache Cassandra. It supports
user accounts with JWT authentication, deterministic short-code generation with collision
handling, optional custom aliases, link expiration, and click tracking.

This project follows the system design described in
[Design a URL Shortener](https://blog.algomaster.io/p/design-a-url-shortener).

## Features

- **User accounts** — register, log in, look up by email, list, delete your own account
- **JWT authentication** — bearer tokens issued on login; ownership-checked endpoints
- **Short URL creation** — deterministic MD5 + Base62 short codes with automatic collision
  retries, or an optional custom alias
- **Redirects** — 302 redirect to the original URL, with expiration enforcement and
  click-count tracking
- **Per-user URL management** — list and delete your own short URLs
- **Rate limiting** — per-IP limits on login, URL creation, and redirects
- **CORS** — configurable allowed origins

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [Apache Cassandra](https://cassandra.apache.org/) — data store (via `cassandra-driver`)
- [Pydantic](https://docs.pydantic.dev/) / `pydantic-settings` — request/response models and config
- [PyJWT](https://pyjwt.readthedocs.io/) — access token issuance and verification
- [bcrypt](https://pypi.org/project/bcrypt/) — password hashing
- [slowapi](https://pypi.org/project/slowapi/) — rate limiting
- [uv](https://docs.astral.sh/uv/) — dependency management and task running

## Project structure

```
src/shrinkr/
├── config.py              # Settings loaded from environment / .env
├── main.py                # FastAPI app, middleware, router registration
├── db/
│   └── database.py        # Cassandra connection + keyspace/table bootstrap
├── models/                 # Pydantic request/response models
│   ├── url.py
│   └── user.py
├── schema/                  # Internal persistence schemas
│   ├── url.py
│   └── user.py
├── repository/              # Cassandra queries (one responsibility per file)
├── services/                 # Business logic: password hashing, auth, short-code generation
└── routes/                    # API route handlers
    ├── health.py
    ├── users.py
    └── urls.py
tests/                         # Unit tests (pytest)
docs/
├── docs.md
└── cqlsh-commands.md          # cqlsh reference for inspecting Cassandra directly
docker-compose.yaml             # Local Cassandra container
```

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker (to run Cassandra locally) or an existing Cassandra cluster

## Setup

1. **Install dependencies**

   ```bash
   uv sync
   ```

2. **Start Cassandra**

   ```bash
   docker compose up -d
   ```

   This starts a single-node Cassandra cluster on `localhost:9043` (mapped from the
   container's `9042`).

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and set a real `JWT_SECRET_KEY` (used to sign access tokens):

   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

   See [Configuration](#configuration) below for the full list of variables.

4. **Run the app**

   ```bash
   uv run dev
   ```

   On startup the app connects to Cassandra and creates the `shrinkr` keyspace and
   required tables/indexes if they don't already exist (see `db/database.py`). The API
   is then available at `http://127.0.0.1:8000` (or whatever `APP_HOST`/`APP_PORT` are
   set to), with interactive docs at `/docs`.

## Configuration

All settings are read from environment variables (or a `.env` file in the project root).

| Variable              | Default       | Description                                              |
|------------------------|---------------|-----------------------------------------------------------|
| `CASSANDRA_HOST`        | `localhost`   | Cassandra contact point                                    |
| `CASSANDRA_PORT`        | `9043`        | Cassandra native protocol port                              |
| `CASSANDRA_KEYSPACE`    | `shrinkr`     | Keyspace created/used by the app                             |
| `APP_HOST`               | `127.0.0.1`   | Host the FastAPI dev server binds to                          |
| `APP_PORT`               | `8000`        | Port the FastAPI dev server binds to                            |
| `JWT_SECRET_KEY`         | *(required)*  | Secret used to sign/verify access tokens — set a real value |
| `JWT_ALGORITHM`          | `HS256`       | JWT signing algorithm                                          |
| `JWT_EXPIRE_MINUTES`     | `60`          | Access token lifetime, in minutes                                |
| `CORS_ORIGINS`           | `*`           | Comma-separated list of allowed CORS origins                      |

## API reference

All routes are mounted under the `/api` prefix.

### Health

| Method | Path          | Auth | Description      |
|--------|---------------|------|-------------------|
| GET    | `/api/health/` | No   | Liveness check     |

### Users

| Method | Path                  | Auth | Description                                   |
|--------|------------------------|------|-------------------------------------------------|
| POST   | `/api/users/`            | No   | Register a new user                               |
| POST   | `/api/users/login`        | No   | Log in and receive a JWT access token              |
| GET    | `/api/users/{email}`      | No   | Look up a user by email                              |
| GET    | `/api/users/`              | Yes  | List all users                                        |
| DELETE | `/api/users/{email}`       | Yes  | Delete a user account (must be your own)               |

**Register**

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "hunter2pass"}'
```

**Log in**

```bash
curl -X POST http://127.0.0.1:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "hunter2pass"}'
```

Response:

```json
{"access_token": "<jwt>", "token_type": "bearer"}
```

Use the token on authenticated requests:

```bash
curl -H "Authorization: Bearer <jwt>" ...
```

### URLs

| Method | Path                         | Auth | Description                                             |
|--------|-------------------------------|------|-----------------------------------------------------------|
| POST   | `/api/urls/`                    | Yes  | Create a short URL owned by the caller                       |
| GET    | `/api/urls/user/{user_id}`        | Yes  | List the caller's own short URLs (`user_id` must match the token) |
| GET    | `/api/urls/{short_url}`             | No   | Redirect to the original URL and record a click                     |
| DELETE | `/api/urls/{short_url}`              | Yes  | Delete a short URL owned by the caller                                 |

**Create a short URL**

```bash
curl -X POST http://127.0.0.1:8000/api/urls/ \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/some/very/long/path"}'
```

Optionally request a custom alias instead of the auto-generated code:

```bash
curl -X POST http://127.0.0.1:8000/api/urls/ \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/launch", "custom_alias": "launch-2026"}'
```

Short URLs expire 30 days after creation and return `410 Gone` once expired.

## Rate limits

| Endpoint                      | Limit        |
|---------------------------------|--------------|
| `POST /api/users/login`           | 5 / minute per IP  |
| `POST /api/urls/`                   | 20 / minute per IP |
| `GET /api/urls/{short_url}`           | 60 / minute per IP |

## Data model (Cassandra)

```sql
CREATE TABLE users (
    id uuid PRIMARY KEY,
    username text,
    email text,
    password text,
    created_at timestamp
);
CREATE INDEX ON users (email);

CREATE TABLE urls_by_user (
    user_id uuid,
    short_url text,
    long_url text,
    creation_date timestamp,
    expiration_date timestamp,
    click_count int,
    PRIMARY KEY (user_id, short_url)
);
CREATE INDEX ON urls_by_user (short_url);
```

These are created automatically on application startup. For manual inspection via
`cqlsh`, see [docs/cqlsh-commands.md](docs/cqlsh-commands.md).

## Testing

```bash
uv run pytest
```

Current tests cover the pure logic that doesn't require a live Cassandra connection:
Base62 short-code generation, password hashing/verification, and JWT issuance/validation.

## Known limitations

- The Cassandra session is a single module-level connection created at import time, with
  no reconnect/retry handling if the cluster becomes unavailable.
- `GET /api/users/` (list all users) only requires being logged in — there's no
  admin/role concept restricting it to privileged accounts.
- No pagination on `GET /api/users/` or `GET /api/urls/user/{user_id}`.
