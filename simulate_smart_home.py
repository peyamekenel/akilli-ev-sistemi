"""
Smart Home System Simulator
Simulates realistic sensor data and demonstrates AI decision making
"""
import time
from datetime import datetime
import random
import math
from src.sensors import (
    SensorManager, TemperatureSensor, HumiditySensor,
    DoorSensor, AirQualitySensor, PresenceSensor
)
from src.ai_engine import AIEngine, ActionExecutor

class SmartHomeSimulator:
    def __init__(self):
        self.sensor_manager = SensorManager()
        self.ai_engine = AIEngine()
        self.action_executor = ActionExecutor()

        # Register sensors
        self.sensors = {
            "temperature": TemperatureSensor("temp_001"),
            "humidity": HumiditySensor("hum_001"),
            "door": DoorSensor("door_001"),
            "air_quality": AirQualitySensor("air_001"),
            "presence": PresenceSensor("pres_001")
        }

        for sensor in self.sensors.values():
            self.sensor_manager.register_sensor(sensor)

        # Simulation state
        self.time = datetime.now()
        self.temperature = 22.0
        self.humidity = 45.0
        self.door_open = False
        self.air_quality = 95
        self.presence = True

    def simulate_temperature(self):
        """Simulate temperature changes throughout the day."""
        hour = self.time.hour
        # Base temperature curve (cooler at night, warmer during day)
        base_temp = 20 + 5 * math.sin(math.pi * (hour - 6) / 12)
        # Add some random variation
        self.temperature = base_temp + random.uniform(-1, 1)
        return self.temperature

    def simulate_humidity(self):
        """Simulate humidity changes."""
        # Humidity often inversely relates to temperature
        base_humidity = 60 - (self.temperature - 20)
        self.humidity = max(30, min(70, base_humidity + random.uniform(-5, 5)))
        return self.humidity

    def simulate_door(self):
        """Simulate door status changes."""
        # Randomly change door state with higher probability during active hours
        hour = self.time.hour
        if 7 <= hour <= 22:
            if random.random() < 0.1:  # 10% chance during active hours
                self.door_open = not self.door_open
        else:
            if random.random() < 0.01:  # 1% chance during night
                self.door_open = not self.door_open
        return self.door_open

    def simulate_air_quality(self):
        """Simulate air quality changes."""
        # Air quality tends to worsen when door is closed for long periods
        if not self.door_open:
            self.air_quality = max(0, self.air_quality - random.uniform(0, 2))
        else:
            self.air_quality = min(100, self.air_quality + random.uniform(0, 5))
        return self.air_quality

    def simulate_presence(self):
        """Simulate presence detection."""
        hour = self.time.hour
        # Higher probability of presence during typical active hours
        if 7 <= hour <= 22:
            if random.random() < 0.9:  # 90% chance of presence during day
                self.presence = True
            else:
                self.presence = False
        else:
            if random.random() < 0.95:  # 95% chance of presence at night (sleeping)
                self.presence = True
            else:
                self.presence = False
        return self.presence

    def run_simulation(self, duration_minutes=60, time_step_minutes=5):
        """Run the simulation for a specified duration."""
        steps = duration_minutes // time_step_minutes

        print("\n=== Smart Home Simulation Started ===")
        print(f"Duration: {duration_minutes} minutes")
        print(f"Time step: {time_step_minutes} minutes")
        print("=====================================\n")

        for step in range(steps):
            # Update simulation time
            self.time = datetime.now()

            # Simulate sensor readings
            temp = self.simulate_temperature()
            humidity = self.simulate_humidity()
            door_status = self.simulate_door()
            air_qual = self.simulate_air_quality()
            presence = self.simulate_presence()

            print(f"\nTime: {self.time.strftime('%H:%M:%S')}")
            print(f"Temperature: {temp:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
            print(f"Door Status: {'Open' if door_status else 'Closed'}")
            print(f"Air Quality: {air_qual:.1f}")
            print(f"Presence: {'Detected' if presence else 'Not Detected'}")

            # Process sensor data through AI engine
            print("\nAI System Response:")
            for sensor in self.sensors.values():
                sensor_data = sensor.get_reading()
                actions = self.ai_engine.process_sensor_data(sensor_data)

                # Execute actions
                for action in actions:
                    print(f"- {action.action_type}: {action.parameters}")
                    self.action_executor.execute_action(action)

            print("\n-----------------------------------")

            # Wait for next time step
            time.sleep(1)  # Shortened for demonstration

if __name__ == "__main__":
    simulator = SmartHomeSimulator()
    simulator.run_simulation(duration_minutes=30, time_step_minutes=5)
