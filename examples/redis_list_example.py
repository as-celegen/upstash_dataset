import upstash_redis
import upstash_dataset
from torch.utils.data import random_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding

# This example demonstrates how to use RedisListDataset with Hugging Face's Transformers library.
# For this example comments have been labeled as positive and negative and stored in Upstash Redis lists with respective keys, "positive_comments" and "negative_comments".
# We will combine these datasets into one dataset and train a model to classify comments as positive or negative.

# Construct redis client, model and tokenizer

redis = upstash_redis.Redis.from_env()
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Construct our datasets from Redis

positive_comments_dataset = upstash_dataset.RedisListDataset(redis, "positive_comments", transform=lambda x: {"label": 1, "text": x, **tokenizer(x)})
negative_comments_dataset = upstash_dataset.RedisListDataset(redis, "negative_comments", transform=lambda x: {"label": 0, "text": x, **tokenizer(x)})

# Combine datasets with different labels into one dataset

comment_dataset = positive_comments_dataset + negative_comments_dataset

# Split dataset into training and evaluation

train_dataset, eval_dataset = random_split(comment_dataset, [0.9, 0.1])

# Define training arguments and trainer

training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train the model

trainer.train()