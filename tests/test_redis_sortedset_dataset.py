import pytest
import upstash_redis

import upstash_dataset

@pytest.fixture(autouse=True)
def setup_index(redis: upstash_redis.Redis):
    redis.zadd('test_redis_sortedset_keys', {'test': 1, 'asd': 2, 'lorem': 3})
    yield
    redis.delete('test_redis_sortedset_keys')


def test_sortedset_dataset(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisSortedSetDataset(redis, 'test_redis_sortedset_keys')
    assert len(dataset) == 3
    assert dataset[0] == ('test', 1.0)
    assert dataset[1] == ('asd', 2.0)
    assert dataset[2] == ('lorem', 3.0)
    assert dataset.__getitems__((0, 2, 1)) == [('test', 1.0), ('lorem', 3.0), ('asd', 2.0)]

def test_transform(redis: upstash_redis.Redis):
    dataset = upstash_dataset.RedisSortedSetDataset(redis, 'test_redis_sortedset_keys', transform=lambda x: {'text': x[0]})
    assert dataset[0] == {'text': 'test'}
    assert dataset[1] == {'text': 'asd'}
    assert dataset[2] == {'text': 'lorem'}
    assert dataset.__getitems__((0, 2, 1)) == [{'text': 'test'}, {'text': 'lorem'}, {'text': 'asd'}]