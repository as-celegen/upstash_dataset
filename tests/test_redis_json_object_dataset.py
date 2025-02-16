import pytest
import upstash_redis

import upstash_dataset

@pytest.fixture(autouse=True)
def setup_index(redis: upstash_redis.Redis):
    redis.json.set('test_redis_json_object_1', '$', {"str": "test"})
    redis.json.set('test_redis_json_object_2', '$', {"str": "asd"})
    redis.json.set('test_redis_json_object_3', '$', {"str": "lorem"})
    yield
    redis.delete("test_redis_json_object_one", "test_redis_json_object_two", "test_redis_json_object_three")


def test_json_array_dataset(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisJsonObjectDataset(redis, key_mapping=lambda x: f'test_redis_json_object_{x+1}', length_function=lambda: 3, object_path='$.str')
    assert len(dataset) == 3
    assert dataset[0] == 'test'
    assert dataset[1] == 'asd'
    assert dataset[2] == 'lorem'
    assert dataset.__getitems__((0, 2, 1)) == ['test', 'lorem', 'asd']

def test_transform(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisJsonObjectDataset(redis, key_mapping=lambda x: f'test_redis_json_object_{x}', length_function=lambda: 3, object_path='$.str', transform=lambda x: {'text': x})
    assert dataset[0] == {'text': 'test'}
    assert dataset[1] == {'text': 'asd'}
    assert dataset[2] == {'text': 'lorem'}
    assert dataset.__getitems__((0, 2, 1)) == [{'text': 'test'}, {'text': 'lorem'}, {'text': 'asd'}]