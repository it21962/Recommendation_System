from .inference_generator import inference_generator

registry = {
    "inference": inference_generator,
}

def get_generator(name):
    return registry.get(name, inference_generator)
