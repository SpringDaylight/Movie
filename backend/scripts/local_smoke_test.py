import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from router import route


def run(path, body):
    resp = route({"path": path, "body": body})
    print("PATH:", path)
    print("STATUS:", resp["statusCode"])
    print("BODY:", resp["body"])
    try:
        print("BODY(JSON):", json.loads(resp["body"]))
    except Exception:
        pass
    print("-" * 50)

if __name__ == "__main__":
    run("/predict/satisfaction", {"user_vector": {}, "movie_vector": {}})
    run("/analyze/preference", {"text": "잔잔하고 여운 있는 영화 좋아해"})
    run("/search/emotional", {"query": "우울한데 너무 무겁지 않은 영화"})
