registry = {}

def register(name):
    
    def decorator(fn):
        registry[name] = fn
        return fn
    return decorator

def get_generator(name):
    
    return registry.get(name)

def list_generators():
   
    return list(registry.keys())
