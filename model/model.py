import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('./dataset/dataset.csv', sep=',')
df.index = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

measurement = df['measurement']

def df_to_x_y(df, window_size=5):
    df_as_numpy = df.to_numpy()
    X = []
    y = []
    for i in range(len(df_as_numpy) - window_size):
        row = [[x] for x in df_as_numpy[i:i + window_size]]
        X.append(row)
        label = df_as_numpy[i + window_size]
        y.append(label)
    return np.array(X), np.array(y)

# Prepare the data
window_size = 5
X, y = df_to_x_y(measurement, window_size)

# Split the data
data_size = len(X)
train_size = int(data_size * 0.7)

# Train and test data
X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size+1:], y[train_size+1:]

# Build the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(window_size, 1)))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(8, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='linear'))

# Print the model summary
model.summary()

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss=tf.keras.losses.MeanSquaredError(), 
              metrics=[tf.keras.metrics.RootMeanSquaredError()])

# Train the model
model.fit(X_train, y_train, epochs=1000)

# Save the model
model.save('./models/model.h5')

# Evaluate the model
model = tf.keras.models.load_model('./models/model.h5')

# Test the model
test_pred = model.predict(X_test).flatten()
test_result = pd.DataFrame(data={'Test pred': test_pred, 'Test actual': y_test})

# Print the results
print(test_result)

# Plot the results
plt.plot(test_result['Test pred'], label='Test pred')
plt.plot(test_result['Test actual'], label='Test actual')
plt.title('Test')
plt.xlabel('Time')
plt.ylabel('Measurement')
plt.legend()
plt.show()