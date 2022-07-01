import redis

try:
    r = redis.Redis(host='redis', port=6379)
    print("redis connection initialized succesfully")
except Exception as e:
    print(e)
    print("redis initialisation failed")
    # Send email to notify so that we can get this easily


def set_data(key, data):
    return r.set(key, data,ex=1800)  # Expiry time of 30 min


def get_data(key):
    return r.get(key)
