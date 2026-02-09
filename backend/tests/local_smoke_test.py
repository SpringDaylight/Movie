import json
import os
import sys

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
    run("/analyze/preference", {"text": "감동적이고 잔잔한 영화 좋아해요"})
    run("/search/emotional", {"query": "설레는데 너무 무겁지 않은 영화"})
