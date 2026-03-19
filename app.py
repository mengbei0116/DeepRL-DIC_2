from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

# Initialize 5x5 GridWorld
# Start: (0, 0), End: (4, 4)
import random

def get_initial_data():
    # Initialize 5x5 GridWorld with 0
    value_matrix = np.zeros((5, 5))
    
    # Obstacles at (1,1), (2,2), (3,3)
    obstacles = [[1, 1], [2, 2], [3, 3]]
    
    # Random initial policy
    arrows = ["↑", "↓", "←", "→"]
    policy_matrix = [["" for _ in range(5)] for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if [r, c] in obstacles:
                policy_matrix[r][c] = "X" # Obstacle marker
            elif r == 4 and c == 4:
                policy_matrix[r][c] = "Goal"
            else:
                policy_matrix[r][c] = random.choice(arrows)
                
    return value_matrix.tolist(), policy_matrix, obstacles

@app.route('/')
def index():
    value_matrix, policy_matrix, obstacles = get_initial_data()
    return render_template('index.html', 
                          value_matrix=value_matrix, 
                          policy_matrix=policy_matrix, 
                          obstacles=obstacles)

@app.route('/run_vi', methods=['POST'])
def run_vi():
    gamma = 0.99
    theta = 0.01
    rows, cols = 5, 5
    obstacles = [[1, 1], [2, 2], [3, 3]]
    goal = [4, 4]
    
    V = np.zeros((rows, cols))
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # U, D, L, R
    action_symbols = ["↑", "↓", "←", "→"]
    
    history = []
    
    # Value Iteration Loop
    max_iters = 100
    for _ in range(max_iters):
        delta = 0
        new_V = V.copy()
        current_policy = [["" for _ in range(cols)] for _ in range(rows)]
        
        for r in range(rows):
            for c in range(cols):
                if [r, c] == goal:
                    current_policy[r][c] = "Goal"
                    continue
                if [r, c] in obstacles:
                    current_policy[r][c] = "X"
                    continue
                
                v = V[r, c]
                q_values = []
                for action in actions:
                    next_r, next_c = r + action[0], c + action[1]
                    if 0 <= next_r < rows and 0 <= next_c < cols and [next_r, next_c] not in obstacles:
                        reward = -1 if [next_r, next_c] != goal else 10 # Reward goal highly for visualization
                        q_values.append(reward + gamma * V[next_r, next_c])
                    else:
                        q_values.append(-1 + gamma * V[r, c])
                
                new_V[r, c] = max(q_values)
                best_action = np.argmax(q_values)
                current_policy[r][c] = action_symbols[best_action]
                delta = max(delta, abs(v - new_V[r, c]))
        
        V = new_V
        history.append({
            'values': np.round(V, 2).tolist(),
            'policy': current_policy
        })
        
        if delta < theta:
            break
            
    # Find Final Optimal Path
    path = []
    curr = [0, 0]
    max_path_steps = rows * cols
    while curr != goal and max_path_steps > 0:
        path.append(curr)
        r, c = curr
        q_values = []
        for action in actions:
            next_r, next_c = r + action[0], c + action[1]
            if 0 <= next_r < rows and 0 <= next_c < cols and [next_r, next_c] not in obstacles:
                reward = -1 if [next_r, next_c] != goal else 10
                q_values.append(reward + gamma * V[next_r, next_c])
            else:
                q_values.append(-1.1 + gamma * V[r, c])
        best_action = np.argmax(q_values)
        curr = [curr[0] + actions[best_action][0], curr[1] + actions[best_action][1]]
        max_path_steps -= 1
    path.append(goal)

    return jsonify({
        'history': history,
        'path': path
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
