import numpy as np
import random
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Disk parameters
disk_size = 200  # Total cylinders in disk
num_requests = 10  # Number of I/O requests

# Generate random disk requests
requests = np.random.randint(0, disk_size, num_requests)
initial_head = np.random.randint(0, disk_size)

# Prepare training data (seek time minimization as supervised learning)
def create_training_data(requests, initial_head):
    X = []  # Features (current head position and pending requests)
    y = []  # Labels (next optimal position)
    
    for _ in range(1000):  # Generate synthetic training samples
        req_sample = random.sample(list(requests), len(requests))
        head = initial_head
        sample_x = []
        sample_y = []
        
        for req in req_sample:
            sample_x.append([head] + req_sample)
            sample_y.append(req)
            head = req
        
        X.extend(sample_x)
        y.extend(sample_y)
    
    return np.array(X), np.array(y)

X_train, y_train = create_training_data(requests, initial_head)

# Define Neural Network Model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(num_requests + 1,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=50, verbose=1, batch_size=32)

# Testing phase
state = initial_head
schedule = [state]
visited = set(schedule)

while len(schedule) < num_requests:
    input_data = np.array([state] + list(requests)).reshape(1, -1)
    prediction = model.predict(input_data, verbose=0)[0][0]
    
    # Select the closest request to the predicted value
    next_request = min(requests, key=lambda x: abs(x - prediction) if x not in visited else float('inf'))
    
    if next_request not in visited:
        schedule.append(next_request)
        visited.add(next_request)
    state = next_request

print("Optimized Disk Scheduling Order:", schedule)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(schedule, range(len(schedule)), marker='o', linestyle='-', color='b', label='Optimized Path')
plt.scatter(requests, range(len(requests)), color='r', label='Requests', zorder=3)
plt.axhline(y=0, color='g', linestyle='--', label='Initial Head Position')
plt.xlabel("Cylinder Number")
plt.ylabel("Order of Execution")
plt.title("Neural Network Disk Scheduling Visualization")
plt.legend()
plt.grid()
plt.show()
