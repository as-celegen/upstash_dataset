import pytest
import upstash_redis
import upstash_vector

@pytest.fixture
def redis():
    return upstash_redis.Redis.from_env()

@pytest.fixture
def index():
    return upstash_vector.Index.from_env()