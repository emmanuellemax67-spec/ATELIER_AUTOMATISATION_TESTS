
from tester.client import get

def test_latest_eur_status():
"""Test 1 : l'API répond correctement pour EUR."""
result = get("/latest", {"from": "EUR"})
assert result["status_code"] == 200, (
f"Statut inattendu : {result['status_code']}"
)

def test_latest_eur_json():
"""Test 2 : la réponse contient un objet JSON."""
result = get("/latest", {"from": "EUR"})
assert result["status_code"] == 200, result["error"]
assert isinstance(result["data"], dict), (
"La réponse n'est pas un objet JSON"
)

def test_latest_eur_schema():
"""Test 3 : les champs obligatoires sont présents."""
result = get("/latest", {"from": "EUR"})
assert result["status_code"] == 200, result["error"]

```
data = result["data"]
for field in ("amount", "base", "date", "rates"):
    assert field in data, f"Champ absent : {field}"
```

def test_latest_eur_types():
"""Test 4 : les types des champs sont corrects."""
result = get("/latest", {"from": "EUR"})
assert result["status_code"] == 200, result["error"]

```
data = result["data"]
assert isinstance(data["amount"], (int, float))
assert isinstance(data["base"], str)
assert isinstance(data["date"], str)
assert isinstance(data["rates"], dict)
```

def test_eur_usd_rate():
"""Test 5 : le taux USD est présent dans la réponse."""
result = get("/latest", {"from": "EUR", "to": "USD"})
assert result["status_code"] == 200, result["error"]

```
rates = result["data"]["rates"]
assert "USD" in rates, "Le taux USD est absent"
assert isinstance(rates["USD"], (int, float))
assert rates["USD"] > 0
```

def test_currencies():
"""Test 6 : l'endpoint des devises renvoie un objet valide."""
result = get("/currencies")
assert result["status_code"] == 200, result["error"]

```
data = result["data"]
assert isinstance(data, dict), "La réponse doit être un objet"
assert "EUR" in data, "La devise EUR est absente"
assert isinstance(data["EUR"], str)
```

def test_historical_rate():
"""Test 7 : les taux historiques sont disponibles."""
result = get(
"/2020-01-01",
{"from": "EUR", "to": "USD"}
)
assert result["status_code"] == 200, result["error"]

```
data = result["data"]
assert isinstance(data, dict)
assert isinstance(data.get("rates"), dict)
assert "USD" in data["rates"]
```
