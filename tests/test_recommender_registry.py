from app.Generators import inference_generator
from app.Generators import get_generator
from app import recommender_registry

def test_register_and_list_generators():
    @recommender_registry.register("dummy")
    def dummy_generator(user_id, sport):
        return []

    assert recommender_registry.get_generator("dummy") == dummy_generator
    assert "dummy" in recommender_registry.list_generators()

def test_get_generator_known_key():
    gen = get_generator("inference")
    assert gen == inference_generator

def test_get_generator_unknown_key_returns_default():
    gen = get_generator("non_existing")
    assert gen == inference_generator
