import httpx  # third party library
import json  # built-in library

resp = httpx.get("https://catfact.ninja/fact")
data = json.loads(resp.text)
print(data["fact"])
