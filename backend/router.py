from utils.response import success, error
from utils.validator import validate_request

from domain.a1_preference import analyze_preference
from domain.a2_movie_vector import process_movie_vector
from domain.a3_prediction import predict_satisfaction
from domain.a4_explanation import explain_prediction
from domain.a5_emotional_search import emotional_search
from domain.a6_group_simulation import simulate_group
from domain.a7_taste_map import build_taste_map


def route(event: dict) -> dict:
    path = event.get("path")
    body = event.get("body", {})

    try:
        if path == "/analyze/preference":
            validate_request("a1_preference_request.json", body)
            return success(analyze_preference(body))

        if path == "/movie/vector":
            validate_request("a2_movie_vector_request.json", body)
            return success(process_movie_vector(body))

        if path == "/predict/satisfaction":
            validate_request("a3_predict_request.json", body)
            return success(predict_satisfaction(body))

        if path == "/explain/prediction":
            validate_request("a4_explain_request.json", body)
            return success(explain_prediction(body))

        if path == "/search/emotional":
            validate_request("a5_search_request.json", body)
            return success(emotional_search(body))

        if path == "/group/simulate":
            validate_request("a6_group_request.json", body)
            return success(simulate_group(body))

        if path == "/map/taste":
            validate_request("a7_map_request.json", body)
            return success(build_taste_map(body))

        return error("NOT_FOUND", 404)

    except Exception as e:
        return error(str(e), 500)
