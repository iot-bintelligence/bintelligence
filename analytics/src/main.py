import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Hyperparameters
learning_rate = 0.001
epochs = 1000
window_size = 5

# Load the data
df = pd.read_csv('../data/actual_data_sorted.csv', sep=',')

df_sorted = df.sort_values("timestamp", ascending=True)

# df_sorted.to_csv("data_sorted.csv", index=False)

df.index = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

measurement = df['measurement']

def df_to_x_y(df, window_size=window_size):
    df_as_numpy = df.to_numpy()
    timestamps = df.index[window_size:]
    X = []
    y = []
    for i in range(len(df_as_numpy) - window_size):
        row = [[x] for x in df_as_numpy[i:i + window_size]]
        X.append(row)
        label = df_as_numpy[i + window_size]
        y.append(label)
    return np.array(X), np.array(y), timestamps

# Prepare the data
X, y, timestamps = df_to_x_y(measurement, window_size)

# Split the data
data_size = len(X)
train_size = int(data_size * 0.73) + 1

# Train and test data
X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size-1:], y[train_size-1:]
test_timestamps = timestamps[train_size-1:]

# Build the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(window_size, 1)))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(8, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='linear'))

# Print the model summary
model.summary()

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss=tf.keras.losses.MeanSquaredError(), 
              metrics=[tf.keras.metrics.RootMeanSquaredError()])

# Train the model
model.fit(X_train, y_train, epochs=epochs)

# Save the model
model.save('../models/model.h5')

# Evaluate the model
model = tf.keras.models.load_model('../models/model.h5')

# Test the model
test_pred = model.predict(X_test).flatten()
test_result = pd.DataFrame(data={'Test pred': test_pred, 'Test actual': y_test, 'Timestamp': test_timestamps})
training_actuals = pd.DataFrame(data={'Training actual': y_train, 'Timestamp': timestamps[:train_size]})

# Plot the results
fig, ax = plt.subplots()
# Set the figure size
fig.set_size_inches(12.5, 6.5)

ax.plot(test_result['Timestamp'], test_result['Test pred'], label='Test pred')
ax.plot(test_result['Timestamp'], test_result['Test actual'], label='Test actual')

# Set the format of the x-axis labels to display the timestamp in the format '%Y-%m-%d %H:%M:%S'
date_fmt = '%Y-%m-%d %H:%M:%S'

date_formatter = mdates.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()
plt.title('Test results')
plt.xlabel('Timestamp')
plt.ylabel('Measurement')
plt.legend(loc='upper left')

# Plot the training and test data in the same plot
fig, ax = plt.subplots()
# Set the figure size
fig.set_size_inches(12.5, 6.5)

ax.plot(training_actuals['Timestamp'], training_actuals['Training actual'], label='Training actual')
ax.plot(test_result['Timestamp'], test_result['Test actual'], label='Test actual')
ax.plot(test_result['Timestamp'], test_result['Test pred'], label='Test pred')

ax.xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()
plt.title('Training and test results')
plt.xlabel('Timestamp')
plt.ylabel('Measurement')
plt.legend(loc='upper left')
plt.show()