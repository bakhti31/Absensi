from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import tensorflow as tf

# Load GPT-2 model and tokenizer
model_name = 'gpt2'
model_gpt2 = TFGPT2LMHeadModel.from_pretrained(model_name)
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(model_name)

# Load your training data
train_data_file = 'train.txt'
train_dataset = tf.data.TextLineDataset(train_data_file)

# Define a function to tokenize text
def tokenize_function(text):
    text = text.numpy().decode('utf-8')
    tokens = tokenizer_gpt2(text, return_tensors="tf", max_length=128, truncation=True)
    return tokens

# Tokenize and process the dataset
def map_function(x):
    return tf.py_function(tokenize_function, [x], tf.Tensor)

tokenized_datasets = train_dataset.map(map_function, num_parallel_calls=tf.data.AUTOTUNE)

# Fine-tune the model
model_gpt2.trainable = True  # Ensure the model is trainable
model_gpt2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5))
model_gpt2.fit(tokenized_datasets)
