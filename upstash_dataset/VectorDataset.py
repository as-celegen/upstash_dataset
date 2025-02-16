from typing import Callable

from torch.utils.data import Dataset
import upstash_vector


class VectorDataset(Dataset):
    """
    Dataset class for Upstash Vector Index

    This class allows you to use Upstash Vector Index as a PyTorch Dataset and allows easy integration for training models.
    """
    def __init__(self, index : upstash_vector.Index, namespace: str = "",
                 id_mapping: Callable = lambda x: str(x), transform: Callable[[upstash_vector.Vector], any] = lambda x: x,
                 include_vectors: bool = True, include_metadata: bool = True, include_data: bool = False):
        """
        :param index: Upstash Vector Index
        :param namespace: Namespace of the vectors in the index
        :param id_mapping: Function to map the index to the vector id
        :param transform: Function to transform the retrieved vector before returning
        :param include_vectors: Whether to include vectors in the fetch
        :param include_metadata: Whether to include metadata in the fetch
        :param include_data: Whether to include data in the fetch
        """
        self._index = index
        self._namespace = namespace
        self._id_mapping = id_mapping
        self._transform = transform
        self._options = {"include_vectors": include_vectors, "include_metadata": include_metadata, "include_data": include_data}

    def __len__(self):
        info = self._index.info()
        return info.namespaces[self._namespace].vector_count

    def __getitem__(self, idx):
        vectors = self._index.fetch(ids=self._id_mapping(idx), namespace=self._namespace, **self._options)
        if len(vectors) == 0 or vectors[0] is None:
            raise IndexError("Index out of range")
        return self._transform(vectors[0])

    def __getitems__(self, idx):
        vectors = self._index.fetch(ids=[self._id_mapping(i) for i in idx], namespace=self._namespace, **self._options)
        if None in vectors:
            raise IndexError("Index out of range")
        return [self._transform(v) for v in vectors]
