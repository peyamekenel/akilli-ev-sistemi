"""
Test suite for Smart Home AI System
Tests all sensor types and AI decision making capabilities
"""
import sys
import os
from datetime import datetime
import unittest

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sensors import (
    SensorManager, TemperatureSensor, HumiditySensor,
    DoorSensor, AirQualitySensor, PresenceSensor
)
from src.ai_engine import AIEngine, ActionExecutor

class TestSmartHomeSystem(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.sensor_manager = SensorManager()
        self.ai_engine = AIEngine()
        self.action_executor = ActionExecutor()

        # Register all sensor types
        self.sensor_manager.register_sensor(TemperatureSensor("temp_001"))
        self.sensor_manager.register_sensor(HumiditySensor("hum_001"))
        self.sensor_manager.register_sensor(DoorSensor("door_001"))
        self.sensor_manager.register_sensor(AirQualitySensor("air_001"))
        self.sensor_manager.register_sensor(PresenceSensor("pres_001"))

    def test_temperature_processing(self):
        """Test temperature sensor data processing and actions."""
        sensor_data = self.sensor_manager.get_sensor_data("temp_001")
        actions = self.ai_engine.process_sensor_data(sensor_data)

        self.assertIsNotNone(sensor_data)
        self.assertIsNotNone(actions)
        print(f"\nTemperature test: {sensor_data.value}°C")
        print("Generated actions:", [a.action_type for a in actions])

    def test_humidity_processing(self):
        """Test humidity sensor data processing and actions."""
        sensor_data = self.sensor_manager.get_sensor_data("hum_001")
        actions = self.ai_engine.process_sensor_data(sensor_data)

        self.assertIsNotNone(sensor_data)
        self.assertIsNotNone(actions)
        print(f"\nHumidity test: {sensor_data.value}%")
        print("Generated actions:", [a.action_type for a in actions])

    def test_door_processing(self):
        """Test door sensor data processing and actions."""
        sensor_data = self.sensor_manager.get_sensor_data("door_001")
        actions = self.ai_engine.process_sensor_data(sensor_data)

        self.assertIsNotNone(sensor_data)
        self.assertIsNotNone(actions)
        print(f"\nDoor test: {'Open' if sensor_data.value else 'Closed'}")
        print("Generated actions:", [a.action_type for a in actions])

    def test_air_quality_processing(self):
        """Test air quality sensor data processing and actions."""
        sensor_data = self.sensor_manager.get_sensor_data("air_001")
        actions = self.ai_engine.process_sensor_data(sensor_data)

        self.assertIsNotNone(sensor_data)
        self.assertIsNotNone(actions)
        print(f"\nAir Quality test: {sensor_data.value} AQI")
        print("Generated actions:", [a.action_type for a in actions])

    def test_presence_processing(self):
        """Test presence sensor data processing and actions."""
        sensor_data = self.sensor_manager.get_sensor_data("pres_001")
        actions = self.ai_engine.process_sensor_data(sensor_data)

        self.assertIsNotNone(sensor_data)
        self.assertIsNotNone(actions)
        print(f"\nPresence test: {'Present' if sensor_data.value else 'Absent'}")
        print("Generated actions:", [a.action_type for a in actions])

    def test_multiple_sensor_integration(self):
        """Test processing of multiple sensor inputs simultaneously."""
        all_sensor_data = self.sensor_manager.get_all_sensor_data()

        self.assertEqual(len(all_sensor_data), 5)  # Should have all 5 sensor types

        all_actions = []
        for sensor_data in all_sensor_data.values():
            actions = self.ai_engine.process_sensor_data(sensor_data)
            all_actions.extend(actions)

        print("\nMultiple sensor test:")
        for sensor_id, sensor_data in all_sensor_data.items():
            print(f"{sensor_id}: {sensor_data.value}")
        print("Total actions generated:", len(all_actions))
        print("Action types:", [a.action_type for a in all_actions])

    def test_action_execution(self):
        """Test that actions can be executed successfully."""
        all_sensor_data = self.sensor_manager.get_all_sensor_data()

        for sensor_data in all_sensor_data.values():
            actions = self.ai_engine.process_sensor_data(sensor_data)
            for action in actions:
                success = self.action_executor.execute_action(action)
                self.assertTrue(success)

if __name__ == '__main__':
    unittest.main(verbosity=2)
