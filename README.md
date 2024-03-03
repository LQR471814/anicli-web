## anipy-web

> a simple, minimal web interface for [anipy-cli](https://github.com/sdaqo/anipy-cli/tree/master).

### running it via docker

```bash
docker pull lqr471814/anipy-web
# the file that stores watch history
touch history.json
docker run -v ./history.json:/app/history.json -dp 8080:8080 -t lqr471814/anipy-web
```

### running it manually

1. `pip install anipy-cli bottle`
2. `git clone <this repo>`
3. `python3 server.py`

