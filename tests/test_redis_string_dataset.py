import pytest
import upstash_redis

import upstash_dataset

@pytest.fixture(autouse=True)
def setup_index(redis: upstash_redis.Redis):
    redis.set('test_redis_string_1', 'test')
    redis.set('test_redis_string_2', 'asd')
    redis.set('test_redis_string_3', 'lorem')
    yield
    redis.delete("test_redis_string_one", "test_redis_string_two", "test_redis_string_three")


def test_redis_string_dataset(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisStringDataset(redis, key_mapping=lambda x: f'test_redis_string_{x+1}', length_function=lambda: 3)
    assert len(dataset) == 3
    assert dataset[0] == 'test'
    assert dataset[1] == 'asd'
    assert dataset[2] == 'lorem'
    assert dataset.__getitems__((0, 2, 1)) == ['test', 'lorem', 'asd']

def test_transform(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisStringDataset(redis, key_mapping=lambda x: f'test_redis_string_{x+1}', length_function=lambda: 3, transform=lambda x: {'text': x})
    assert dataset[0] == {'text': 'test'}
    assert dataset[1] == {'text': 'asd'}
    assert dataset[2] == {'text': 'lorem'}
    assert dataset.__getitems__((0, 2, 1)) == [{'text': 'test'}, {'text': 'lorem'}, {'text': 'asd'}]