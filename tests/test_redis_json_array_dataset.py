import pytest
import upstash_redis

import upstash_dataset

@pytest.fixture(autouse=True)
def setup_index(redis: upstash_redis.Redis):
    redis.json.set('test_redis_json_array', '$', {"array": ['test', 'asd', 'lorem']})
    yield
    redis.delete("test_redis_json_array")


def test_json_array_dataset(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisJsonArrayDataset(redis, 'test_redis_list_dataset', '$.array')
    assert len(dataset) == 3
    assert dataset[0] == 'test'
    assert dataset[1] == 'asd'
    assert dataset[2] == 'lorem'
    assert dataset.__getitems__((0, 2, 1)) == ['test', 'lorem', 'asd']

def test_transform(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisJsonArrayDataset(redis, 'test_redis_list_dataset', '$.array', transform=lambda x: {'text': x})
    assert dataset[0] == {'text': 'test'}
    assert dataset[1] == {'text': 'asd'}
    assert dataset[2] == {'text': 'lorem'}
    assert dataset.__getitems__((0, 2, 1)) == [{'text': 'test'}, {'text': 'lorem'}, {'text': 'asd'}]