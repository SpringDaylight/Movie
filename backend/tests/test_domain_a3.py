from domain.a3_prediction import predict_satisfaction

def test_predict_satisfaction_returns_dict():
    result = predict_satisfaction({})
    assert isinstance(result, dict)
