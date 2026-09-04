# Todo Items API

A minimal Flask REST API for managing todo items. Used as a sandbox for trying out Devin.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
make install
```

## Run

```bash
make run          # http://localhost:5000
```

## Test

```bash
make test
```

## Endpoints

| Method | Path                | Description                    |
| ------ | ------------------- | ------------------------------ |
| GET    | `/health`           | Liveness check                 |
| GET    | `/items`            | List items (`?done=true/false`) |
| POST   | `/items`            | Create item `{"name": "..."}`  |
| GET    | `/items/<id>`       | Get one item                   |
| POST   | `/items/<id>/done`  | Mark item as done              |

Items are stored in memory and reset on restart.
