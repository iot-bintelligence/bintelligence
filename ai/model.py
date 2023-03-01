import tensorflow as tf
import numpy as np
import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('./dataset/waste_data.csv')

# Split the data into training and testing sets
train_data = data.sample(frac=0.8, random_state=0)
test_data = data.drop(train_data.index)

# Extract the input and output features
train_x = train_data[['timestamp', 'amount']].values.astype(np.float32)
train_y = train_data['full_timestamp'].values.reshape(-1, 1).astype(np.float32)
test_x = test_data[['timestamp', 'amount']].values.astype(np.float32)
test_y = test_data['full_timestamp'].values.reshape(-1, 1).astype(np.float32)

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu', input_shape=[2]),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=1)
])

# Compile the model
model.compile(optimizer=tf.optimizers.Adam(), loss='mse')

# Train the model
model.fit(train_x, train_y, epochs=100)

# Evaluate the model
test_loss = model.evaluate(test_x, test_y)
print('Test Loss:', test_loss)

# Save the model
model.save('./models/waste_model.h5')