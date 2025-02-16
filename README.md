# Upstash Dataset

This library provides PyTorch-compatible dataset classes for Upstash products, enabling efficient training and evaluation of deep learning models.
The dataset classes inherit from PyTorch's Dataset class, allowing seamless integration with DataLoader and Hugging Face's Trainer.
Since data is fetched in real-time batches using pipelines, this library is ideal for training on large datasets that cannot fit into memory.

## Installation

```bash
pip install upstash-dataset
```

## Usage

Simply import the desired dataset class from the upstash_dataset module and create an instance of it.

```python
from upstash_redis import Redis
from upstash_dataset import RedisListDataset

redis = Redis.from_env()
dataset = RedisListDataset(redis, "my_comments")
```

You can use the dataset instance with Pytorch's DataLoader class or Huggingface's Trainer class.

```python
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
)
```

## Available dataset classes

5 Most common data organization patterns in redis have been implemented as dataset classes:

- RedisListDataset
- RedisSortedSetDataset
- RedisJsonArrayDataset
- RedisJsonObjectDataset
- RedisStringDataset

Also, one dataset class for vector database has been implemented:

- VectorDataset

### RedisListDataset

This dataset class is used to fetch data from a Redis list. Each element in the list is considered as a sample.

```python
from upstash_dataset import RedisListDataset

dataset = RedisListDataset(redis, "my_list")
```

### RedisSortedSetDataset

This dataset class is used to fetch data from a Redis sorted set. Each element in the sorted set is considered as a sample.

```python
from upstash_dataset import RedisSortedSetDataset

dataset = RedisSortedSetDataset(redis, "my_sorted_set")
```

### RedisJsonArrayDataset

This dataset class is used to fetch data from a JSON array stored in a Redis JSON Object. Each element in the array is considered as a sample.

```python
from upstash_dataset import RedisJsonArrayDataset

dataset = RedisJsonArrayDataset(redis, "my_json_object", "$.my_array")
```

### RedisJsonObjectDataset

This dataset class is used to fetch data from multiple Redis JSON Object. Each JSON object stored as different keys is considered as a sample.
Since each sample is fetched from different key, you need to specify the key mapping function and length function in the constructor.

```python
from upstash_dataset import RedisJsonObjectDataset

dataset = RedisJsonObjectDataset(redis, "my_json_object", key_mapping=lambda x: f'json_object_{x+1}', length_function=my_length_function)
```

### RedisStringDataset

This dataset class is used to fetch data from multiple Redis strings. Each string stored as different keys is considered as a sample.
Since each sample is fetched from different key, you need to specify the key mapping function and length function in the constructor.

```python
from upstash_dataset import RedisStringDataset

dataset = RedisStringDataset(redis, "my_json_object", key_mapping=lambda x: f'json_object_{x+1}', length_function=my_length_function)
```

### VectorDataset

This dataset class is used to fetch data from a vector database. Each vector in the database is considered as a sample.
Since the IDs of vectors are not sequential, you need to specify an ID mapping function.

```python
from upstash_dataset import VectorDataset
from upstash_vector import Index

index = Index.from_env()
dataset = VectorDataset(index, id_mapping=my_id_mapping_function)
```