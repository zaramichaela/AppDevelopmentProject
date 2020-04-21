import pickle


def deserialize(dict):
    try:
        return pickle.loads(dict)
    except:
        return None

def serialize(item):
    return pickle.dumps(item)
