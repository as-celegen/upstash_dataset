from typing import Callable

from torch.utils.data import Dataset
import upstash_redis


class RedisListDataset(Dataset):
    """
    Dataset class for Upstash Redis List

    This class allows you to use Upstash Redis List as a PyTorch Dataset and allows easy integration for training models. Each element in the list is treated as a sample.
    """
    def __init__(self, redis: upstash_redis.Redis, key: str, transform: Callable = lambda x: x):
        """
        :param redis: Upstash Redis client
        :param key: Redis key to the list
        :param transform: Function to transform the retrieved value before returning
        """
        self._redis = redis
        self._key = key
        self._transform = transform

    def __len__(self):
        return self._redis.llen(self._key)

    def __getitem__(self, idx):
        return self._transform(self._redis.lindex(self._key, idx))

    def __getitems__(self, idx):
        pipeline = self._redis.pipeline()
        for i in idx:
            pipeline.lindex(self._key, i)
        return [self._transform(i) for i in pipeline.exec()]


class RedisSortedSetDataset(Dataset):
    """
    Dataset class for Upstash Redis Sorted Set

    This class allows you to use Upstash Redis Sorted Set as a PyTorch Dataset and allows easy integration for training models. Each element in the sorted set is treated as a sample.
    """
    def __init__(self, redis: upstash_redis.Redis, key: str, transform: Callable = lambda x: x):
        """
        :param redis: Upstash Redis client
        :param key: Redis key to the sorted set
        :param transform: Function to transform the retrieved value before returning
        """
        self._redis = redis
        self._key = key
        self._transform = transform

    def __len__(self):
        return self._redis.zcard(self._key)

    def __getitem__(self, idx):
        return self._transform(self._redis.zrange(self._key, idx, idx, withscores=True)[0])

    def __getitems__(self, idx):
        pipeline = self._redis.pipeline()
        for i in idx:
            pipeline.zrange(self._key, i, i, withscores=True)
        return [self._transform(i[0]) for i in pipeline.exec()]


class RedisStringDataset(Dataset):
    """
    Dataset class for Upstash Redis String

    This class allows you to use Upstash Redis Strings stored in different keys as a PyTorch Dataset and allows easy integration for training models. Each string stored in a different key is treated as a sample.
    """
    def __init__(self, redis: upstash_redis.Redis, key_mapping: Callable, length_function: Callable, transform: Callable = lambda x: x):
        """
        :param redis: Upstash Redis client
        :param key_mapping: Function to map the index to the Redis key
        :param length_function: Function to get the length of the dataset
        :param transform: Function to transform the retrieved value before returning
        """
        self._redis = redis
        self._length_function = length_function
        self._key_mapping = key_mapping
        self._transform = transform

    def __len__(self):
        return self._length_function()

    def __getitem__(self, idx):
        return self._transform(self._redis.get(self._key_mapping(idx)))

    def __getitems__(self, idx):
        pipeline = self._redis.pipeline()
        for i in idx:
            pipeline.get(self._key_mapping(i))
        return [self._transform(i) for i in pipeline.exec()]


class RedisJsonArrayDataset(Dataset):
    """
    Dataset class for Upstash Redis JSON Array

    This class allows you to use Upstash Redis JSON Array as a PyTorch Dataset and allows easy integration for training models. Each element in the JSON array is treated as a sample.
    """
    def __init__(self, redis: upstash_redis.Redis, key: str, array_path: str = '$', transform: Callable = lambda x: x):
        """
        :param redis: Upstash Redis client
        :param key: Redis key to the JSON object
        :param array_path: Path to the array in the JSON object
        :param transform: Function to transform the retrieved value before returning
        """
        self._redis = redis
        self._key = key
        self._array_path = array_path
        self._transform = transform

    def __len__(self):
        l = self._redis.json.arrlen(self._key, self._array_path)
        if type(l) == int:
            return l
        return l[0]

    def __getitem__(self, idx):
        return self._transform(self._redis.json.get(self._key, f'{self._array_path}[{idx}]')[0])

    def __getitems__(self, idx):
        pipeline = self._redis.pipeline()
        for i in idx:
            pipeline.json.get(self._key, f'{self._array_path}[{i}]')
        return [self._transform(i[0]) for i in pipeline.exec()]


class RedisJsonObjectDataset(Dataset):
    """
    Dataset class for Upstash Redis JSON Object

    This class allows you to use Upstash Redis JSON Objects stored in different keys as a PyTorch Dataset and allows easy integration for training models. Each JSON object stored in a different key is treated as a sample.
    """
    def __init__(self, redis: upstash_redis.Redis, key_mapping: Callable, length_function: Callable, object_path: str, transform: Callable = lambda x: x):
        """
        :param redis: Upstash Redis client
        :param key_mapping: Function to map the index to the Redis JSON key
        :param length_function: Function to get the length of the dataset
        :param object_path: Path to the value to be retrieved in the JSON objects
        :param transform: Function to transform the retrieved value before returning
        """
        self._redis = redis
        self._key_mapping = key_mapping
        self._length_function = length_function
        self._object_path = object_path
        self._transform = transform

    def __len__(self):
        return self._length_function()

    def __getitem__(self, idx):
        if self._object_path == '' or self._object_path == '$':
            return self._transform(self._redis.json.get(self._key_mapping(idx)))
        return self._transform(self._redis.json.get(self._key, self._object_path)[0])

    def __getitems__(self, idx):
        result = self._redis.json.mget([self._key_mapping(i) for i in idx], self._object_path)
        if self._object_path == '' or self._object_path == '$':
            return [self._transform(i) for i in result]
        return [self._transform(i[0]) for i in result]