# Upstash Dataset

Upstash Dataset provides a seamless way to stream data from Upstash directly into PyTorch and Hugging Face workflows.
Built on PyTorch’s `Dataset` abstract class, it ensures native compatibility with `DataLoader` and Hugging Face’s `Trainer`, allowing efficient data loading without the need to pre-download or store datasets in memory.
By fetching data in real-time using pipelines, it enables parallelized model training and evaluation, making it ideal for large-scale and dynamic datasets.

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

The five most common data organization patterns in redis have been implemented as dataset classes:

- RedisListDataset
- RedisSortedSetDataset
- RedisJsonArrayDataset
- RedisJsonObjectDataset
- RedisStringDataset

Additionally, a dataset class for vector databases has been implemented, enabling seamless integration with embedding-based models—a common practice for designing models for downstream tasks such as retrieval, classification, and clustering.

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

This dataset class is used to fetch data from multiple Redis JSON objects. Each JSON object stored as different keys is considered as a sample.
Since each sample is fetched from different key, you need to specify an index-to-key mapping function and a length function in the constructor.

```python
from upstash_dataset import RedisJsonObjectDataset

dataset = RedisJsonObjectDataset(redis, "my_json_object", key_mapping=lambda x: f'json_object_{x+1}', length_function=my_length_function)
```

### RedisStringDataset

This dataset class is used to fetch data from multiple Redis strings. Each string stored as different keys is considered as a sample.
Since each sample is fetched from different key, you need to specify an index-to-key mapping function and a length function in the constructor.

```python
from upstash_dataset import RedisStringDataset

dataset = RedisStringDataset(redis, key_mapping=lambda x: f'string_{x+1}', length_function=my_length_function)
```

### VectorDataset

This dataset class is used to fetch data from a vector database. Each vector in the database is considered as a sample.
Since the IDs of vectors are not sequential, you need to specify an index-to-ID mapping function.

```python
from upstash_dataset import VectorDataset
from upstash_vector import Index

index = Index.from_env()
dataset = VectorDataset(index, id_mapping=my_id_mapping_function)
```