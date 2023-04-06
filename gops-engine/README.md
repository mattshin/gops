# Engine (Server)

## quickstart

```
$ poetry install
$ poetry run uvicorn -- main:app --reload

...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7662] using WatchFiles
```

## dev ui

Although this server is meant to service websocket connections created by player clients, a barebones UI for playing games is provided at `/ui`.