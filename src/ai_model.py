import numpy as np
import json
import os
from sklearn.tree import DecisionTreeClassifier

class SmartHomeAI:
    def __init__(self):
        """Initialize the Smart Home AI model"""
        self.history_file = 'sensor_history.json'
        self.model = DecisionTreeClassifier(max_depth=5, random_state=42)
        if not os.path.exists(self.history_file):
            self.save_history([])

    def load_history(self):
        """Load training history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def save_history(self, history):
        """Save training history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f)

    def process_sensor_data(self, sensor_data):
        """Process sensor data and return recommended actions"""
        # Convert input data to features
        input_data = np.array([[
            sensor_data['temperature'],
            sensor_data['humidity'],
            1.0 if sensor_data['door_status'] else 0.0,
            sensor_data['air_quality'],
            1.0 if sensor_data['presence'] else 0.0
        ]])

        # Initialize actions with explicit rules
        actions = {
            'ventilation': False,
            'hvac': False,
            'lighting': sensor_data['presence'],
            'security': sensor_data['door_status'],
            'energy_saving': not sensor_data['presence']
        }

        # Apply temperature and air quality rules
        if sensor_data['temperature'] >= 26.0:
            actions['ventilation'] = True
            actions['hvac'] = True
        elif sensor_data['temperature'] < 18.0:
            actions['hvac'] = True

        if sensor_data['air_quality'] < 90.0:
            actions['ventilation'] = True

        # Apply learned patterns if we have enough data
        history = self.load_history()
        if len(history) >= 10:
            self.train_model()  # No argument needed
            try:
                predictions = self.model.predict(input_data)
                # Combine predictions with explicit rules using logical OR
                actions['ventilation'] = actions['ventilation'] or bool(predictions[0][0])
                actions['hvac'] = actions['hvac'] or bool(predictions[0][1])
                actions['lighting'] = actions['lighting'] or bool(predictions[0][2])
                actions['security'] = actions['security'] or bool(predictions[0][3])
                actions['energy_saving'] = actions['energy_saving'] or bool(predictions[0][4])
            except Exception as e:
                print(f"Prediction failed: {e}")  # For debugging
                pass  # Fall back to explicit rules if prediction fails

        # Override with energy saving logic
        if actions['energy_saving']:
            actions['lighting'] = False
            if 18 <= sensor_data['temperature'] <= 26 and sensor_data['air_quality'] >= 90:
                actions['hvac'] = False
                actions['ventilation'] = False

        # Save to history for future training
        history.append({
            'input': sensor_data,
            'output': actions
        })
        self.save_history(history)

        return actions

    def train_model(self):
        """Train the decision tree model on historical data"""
        history = self.load_history()
        if not history:
            return

        # Prepare training data
        X = []
        y = []
        for entry in history:
            X.append([
                entry['input']['temperature'],
                entry['input']['humidity'],
                1.0 if entry['input']['door_status'] else 0.0,
                entry['input']['air_quality'],
                1.0 if entry['input']['presence'] else 0.0
            ])
            y.append([
                1.0 if entry['output']['ventilation'] else 0.0,
                1.0 if entry['output']['hvac'] else 0.0,
                1.0 if entry['output']['lighting'] else 0.0,
                1.0 if entry['output']['security'] else 0.0,
                1.0 if entry['output']['energy_saving'] else 0.0
            ])

        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)

        # Train the model
        if len(X) > 0:
            self.model.fit(X, y)

    def get_learned_rules(self):
        """Extract rules from the decision tree"""
        if not hasattr(self.model, 'tree_'):
            return []

        feature_names = ['Temperature', 'Humidity', 'Door Status', 'Air Quality', 'Presence']
        action_names = ['Ventilation', 'HVAC', 'Lighting', 'Security', 'Energy Saving']
        rules = []

        def recurse(node, depth, path):
            if self.model.tree_.feature[node] != -2:  # Not a leaf
                feature = feature_names[self.model.tree_.feature[node]]
                threshold = self.model.tree_.threshold[node]
                rules.append(f"If {feature} <= {threshold:.1f}: {path}")


                left_path = path + f" AND {feature} <= {threshold:.1f}"
                right_path = path + f" AND {feature} > {threshold:.1f}"

                recurse(self.model.tree_.children_left[node], depth + 1, left_path)
                recurse(self.model.tree_.children_right[node], depth + 1, right_path)

        recurse(0, 0, "")
        return rules
