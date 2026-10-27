
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
import json

BASE_URL = "https://api.frankfurter.dev"
TIMEOUT = 3
MAX_RETRIES = 1

def get(path, params=None):
"""
Envoie une requête GET avec timeout, mesure de latence
et une seule nouvelle tentative si nécessaire.
"""
url = BASE_URL + path

```
if params:
    url += "?" + urlencode(params)

last_error = None

for attempt in range(MAX_RETRIES + 1):
    start = time.perf_counter()

    try:
        req = Request(
            url,
            headers={"Accept": "application/json"}
        )

        with urlopen(req, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8")
            latency_ms = (time.perf_counter() - start) * 1000

            return {
                "status_code": response.status,
                "content_type": response.headers.get(
                    "Content-Type", ""
                ),
                "latency_ms": round(latency_ms, 2),
                "data": json.loads(body),
                "error": None,
            }

    except HTTPError as exc:
        latency_ms = (time.perf_counter() - start) * 1000

        last_error = {
            "status_code": exc.code,
            "content_type": exc.headers.get(
                "Content-Type", ""
            ),
            "latency_ms": round(latency_ms, 2),
            "data": None,
            "error": str(exc),
        }

        # Une nouvelle tentative uniquement pour 429 et 5xx.
        if exc.code == 429 or exc.code >= 500:
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue

        return last_error

    except (URLError, TimeoutError, OSError, ValueError) as exc:
        latency_ms = (time.perf_counter() - start) * 1000

        last_error = {
            "status_code": None,
            "content_type": "",
            "latency_ms": round(latency_ms, 2),
            "data": None,
            "error": str(exc),
        }

        if attempt < MAX_RETRIES:
            time.sleep(0.5)
            continue

        return last_error

return last_error
```
