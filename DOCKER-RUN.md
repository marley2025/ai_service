# Run with Docker Compose

## Build and start
```bash
docker compose up --build -d
```

The API will be on http://localhost:8080

## Check it’s running
```bash
curl http://localhost:8080/docs
```

## Dev mode (hot reload)
Uncomment the `volumes:` and `command:` in `docker-compose.yml` and run:
```bash
docker compose up --build
```

## Stop
```bash
docker compose down
```
