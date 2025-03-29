import numpy as np
import random
import matplotlib.pyplot as plt

# Disk parameters
disk_size = 200  # Total cylinders in disk
num_requests = 10  # Number of I/O requests

# Generate random disk requests
requests = np.random.randint(0, disk_size, num_requests)
initial_head = np.random.randint(0, disk_size)

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.2  # Exploration rate

# Q-table initialization
q_table = np.zeros((disk_size, disk_size))

def get_reward(state, action):
    """Reward is negative of seek time (lower seek time is better)."""
    return -abs(state - action)

def choose_action(state):
    """Epsilon-greedy policy."""
    if random.uniform(0, 1) < epsilon:
        return random.choice(requests)  # Explore
    else:
        return np.argmax(q_table[state])  # Exploit best action

# Training the Q-learning model
num_episodes = 1000
for _ in range(num_episodes):
    state = initial_head
    for _ in range(num_requests):
        action = choose_action(state)
        reward = get_reward(state, action)
        next_state = action
        
        # Q-learning update rule
        best_future_q = np.max(q_table[next_state])
        q_table[state, action] += alpha * (reward + gamma * best_future_q - q_table[state, action])
        
        state = next_state

# Testing the trained model
state = initial_head
schedule = [state]
visited = set(schedule)
while len(schedule) < num_requests:
    action = np.argmax(q_table[state])
    
    # If action was already visited, pick a different one
    if action in visited:
        unvisited = list(set(requests) - visited)
        if unvisited:
            action = random.choice(unvisited)
        else:
            break  # Avoid infinite loop if all requests are visited
    
    schedule.append(action)
    visited.add(action)
    state = action

print("Optimized Disk Scheduling Order:", schedule)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(schedule, range(len(schedule)), marker='o', linestyle='-', color='b', label='Optimized Path')
plt.scatter(requests, range(len(requests)), color='r', label='Requests', zorder=3)
plt.axhline(y=0, color='g', linestyle='--', label='Initial Head Position')
plt.xlabel("Cylinder Number")
plt.ylabel("Order of Execution")
plt.title("Disk Scheduling Visualization")
plt.legend()
plt.grid()
plt.show()
