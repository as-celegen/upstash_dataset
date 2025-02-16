import upstash_vector
import upstash_dataset
import torch
from torch.utils.data import random_split, DataLoader
import torch.optim as optim
import torch.nn.functional as F

# This example demonstrates how to use VectorDataset with Pytorch models.
# For this example we have a dataset of movie embeddings and their genres stored in Upstash Vector Database.
# Those embeddings are used to train a model to classify movies into genres.

class GenreClassificationModel(torch.nn.Module):
    def __init__(self, num_labels: int):
        super().__init__()
        self.dropout = torch.nn.Dropout(0.1)
        self.classifier = torch.nn.Linear(1024, num_labels)

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        x = self.dropout(embedding)
        x = self.classifier(x)
        return x


# Initialize Redis client and model
index = upstash_vector.Index.from_env()
num_labels = 10  # Adjust based on the dataset
model = GenreClassificationModel(num_labels)

# Construct dataset from Upstash Vector Database
dataset = upstash_dataset.VectorDataset(
    index,
    "movies",
    id_mapping=lambda x: f'movie_{x}',
    transform=lambda x: {"genre": torch.tensor(x.metadata["genre"]), "embedding": torch.tensor(x.vector)}
)

# Split dataset into training and evaluation sets
train_size = int(0.9 * len(dataset))
eval_size = len(dataset) - train_size
train_dataset, eval_dataset = random_split(dataset, [train_size, eval_size])

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=1)
eval_loader = DataLoader(eval_dataset, batch_size=16, shuffle=False, num_workers=1)

# Define optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=2e-5, weight_decay=0.01)
criterion = torch.nn.CrossEntropyLoss()


# Training loop
def train_model(model, train_loader, optimizer, criterion, epochs=5):
    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()
            outputs = model(batch["embedding"])
            loss = criterion(outputs, batch["genre"])
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader)}")


# Train the model
train_model(model, train_loader, optimizer, criterion)
