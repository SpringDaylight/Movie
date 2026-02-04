import os

ENV = os.getenv("ENV", "local")

DEFAULT_WEIGHTS = {
    "emotion": 0.4,
    "narrative": 0.4,
    "ending": 0.2
}
