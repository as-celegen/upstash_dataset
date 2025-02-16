import pytest
import upstash_vector
from upstash_vector.types import FetchResult

import upstash_dataset

@pytest.fixture(autouse=True)
def setup_index(index: upstash_vector.Index):
    index.upsert([
        upstash_vector.types.Vector(id="test_vector_1", vector=[1, 0, 0]),
        upstash_vector.types.Vector(id="test_vector_2", vector=[0, 1, 0]),
        upstash_vector.types.Vector(id="test_vector_3", vector=[0, 0, 1]),
    ], namespace="test_dataset_namespace")
    yield
    index.delete_namespace("test_dataset_namespace")


def test_vector_dataset(index: upstash_vector.Index):
    dataset = upstash_dataset.VectorDataset(index, namespace="test_dataset_namespace", id_mapping=lambda x: f'test_vector_{x+1}')
    assert len(dataset) == 3
    assert dataset[0] == FetchResult(id="test_vector_1", vector=[1, 0, 0])
    assert dataset[1] == FetchResult(id="test_vector_2", vector=[0, 1, 0])
    assert dataset[2] == FetchResult(id="test_vector_3", vector=[0, 0, 1])
    assert dataset.__getitems__((0, 2, 1)) == [FetchResult(id="test_vector_1", vector=[1, 0, 0]), FetchResult(id="test_vector_3", vector=[0, 0, 1]), FetchResult(id="test_vector_2", vector=[0, 1, 0])]

def test_transform(index: upstash_vector.Index):
    dataset = upstash_dataset.VectorDataset(index, namespace="test_dataset_namespace", id_mapping=lambda x: f'test_vector_{x+1}', transform=lambda x: x.vector)
    assert dataset[0] == [1, 0, 0]
    assert dataset[1] == [0, 1, 0]
    assert dataset[2] == [0, 0, 1]
    assert dataset.__getitems__((0, 2, 1)) == [[1, 0, 0], [0, 0, 1], [0, 1, 0]]