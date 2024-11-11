import unittest
import numpy as np
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_model import SmartHomeAI
from src.ai_controller import AIController

class TestSmartHomeAI(unittest.TestCase):
    def setUp(self):
        self.ai = SmartHomeAI()
        self.controller = AIController()

    def test_sensor_processing(self):
        # Test basic sensor processing
        sensor_data = {
            'temperature': 24.5,
            'humidity': 55.0,
            'door_status': False,
            'air_quality': 95.0,
            'presence': True
        }

        actions = self.controller.process_sensor_data(sensor_data)
        self.assertIsInstance(actions, dict)
        self.assertEqual(len(actions), 5)  # Should have 5 system states

    def test_learning_capability(self):
        # Test if system learns from repeated patterns
        # Pattern 1: High temperature -> Ventilation
        for _ in range(50):
            sensor_data = {
                'temperature': 26.0,
                'humidity': 55.0,
                'door_status': False,
                'air_quality': 95.0,
                'presence': True
            }
            self.controller.process_sensor_data(sensor_data)

        # Test if system learned the pattern
        test_data = {
            'temperature': 26.0,
            'humidity': 55.0,
            'door_status': False,
            'air_quality': 95.0,
            'presence': True
        }
        actions = self.controller.process_sensor_data(test_data)
        self.assertTrue(actions['ventilation'])

    def test_rule_extraction(self):
        # Train with various patterns
        patterns = [
            # Hot + Poor air quality
            {'temperature': 27.0, 'humidity': 60.0, 'door_status': False, 'air_quality': 80.0, 'presence': True},
            # Cold + Good air quality
            {'temperature': 17.0, 'humidity': 45.0, 'door_status': False, 'air_quality': 98.0, 'presence': True},
            # Normal conditions
            {'temperature': 22.0, 'humidity': 50.0, 'door_status': False, 'air_quality': 95.0, 'presence': True},
        ]

        # Train the system
        for pattern in patterns * 20:  # Repeat patterns to simulate learning
            self.controller.process_sensor_data(pattern)

        # Get learned rules
        rules = self.controller.get_learned_rules()
        self.assertGreater(len(rules), 0)

        # Verify rule structure
        for rule in rules:
            self.assertIn('condition', rule)
            self.assertIn('actions', rule)
            self.assertIn('confidence', rule)

    def test_sensor_combinations(self):
        # Test system's ability to handle combined conditions
        combinations = [
            # Hot + Poor air quality should trigger both ventilation and cooling
            {
                'input': {'temperature': 27.0, 'humidity': 60.0, 'door_status': False, 'air_quality': 80.0, 'presence': True},
                'expected': {'ventilation': True, 'hvac': True}
            },
            # Cold + Door open should trigger heating and security
            {
                'input': {'temperature': 17.0, 'humidity': 45.0, 'door_status': True, 'air_quality': 95.0, 'presence': True},
                'expected': {'hvac': True, 'security': True}
            },
            # No presence + Normal conditions should trigger energy saving
            {
                'input': {'temperature': 22.0, 'humidity': 50.0, 'door_status': False, 'air_quality': 95.0, 'presence': False},
                'expected': {'energy_saving': True}
            }
        ]

        # Train the system with these combinations
        for combo in combinations * 20:
            self.controller.process_sensor_data(combo['input'])

        # Test if system learned the combinations
        for combo in combinations:
            actions = self.controller.process_sensor_data(combo['input'])
            for system, expected in combo['expected'].items():
                self.assertEqual(actions[system], expected,
                    f"Failed to learn combination: {combo['input']}, expected {system} to be {expected}")

if __name__ == '__main__':
    unittest.main()
