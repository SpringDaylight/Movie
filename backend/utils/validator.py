# JSON Schema 검증
def validate_request(schema_name: str, body: dict):
    """
    JSON Schema 검증 (구현은 나중)
    """
    if not isinstance(body, dict):
        raise ValueError("Request body must be JSON object")
