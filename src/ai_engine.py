"""
Smart Home AI Decision Engine
Processes sensor data and makes intelligent decisions for home automation using neural networks.
"""
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np
from .sensors import SensorData, SensorType
from .ai_model import SmartHomeAI
from .ai_controller import AIController

@dataclass
class Action:
    action_id: str
    action_type: str
    parameters: Dict
    priority: int
    timestamp: datetime

class AIEngine:
    def __init__(self):
        self.ai_controller = AIController()
        self.current_state: Dict[SensorType, SensorData] = {}

    def process_sensor_data(self, sensor_data: SensorData) -> List[Action]:
        """Process new sensor data and determine required actions using neural network."""
        # Update current state
        self.current_state[sensor_data.sensor_type] = sensor_data

        # Prepare sensor data for AI processing
        sensor_dict = {
            'temperature': float(self.current_state.get(SensorType.TEMPERATURE, SensorData(SensorType.TEMPERATURE, "22.0", datetime.now())).value),
            'humidity': float(self.current_state.get(SensorType.HUMIDITY, SensorData(SensorType.HUMIDITY, "45.0", datetime.now())).value),
            'door_status': bool(self.current_state.get(SensorType.DOOR, SensorData(SensorType.DOOR, "False", datetime.now())).value),
            'air_quality': float(self.current_state.get(SensorType.AIR_QUALITY, SensorData(SensorType.AIR_QUALITY, "95.0", datetime.now())).value),
            'presence': bool(self.current_state.get(SensorType.PRESENCE, SensorData(SensorType.PRESENCE, "True", datetime.now())).value)
        }

        # Get AI predictions
        system_actions = self.ai_controller.process_sensor_data(sensor_dict)

        # Convert AI decisions to actions
        actions = []

        if system_actions['ventilation']:
            actions.append(Action(
                action_id=f"ventilation_{datetime.now().timestamp()}",
                action_type="ACTIVATE_VENTILATION",
                parameters={"speed": "auto", "duration_minutes": 15},
                priority=2,
                timestamp=datetime.now()
            ))

        if system_actions['hvac']:
            current_temp = float(self.current_state.get(SensorType.TEMPERATURE, SensorData(SensorType.TEMPERATURE, "22.0", datetime.now())).value)
            if current_temp > 24:
                actions.append(Action(
                    action_id=f"cooling_{datetime.now().timestamp()}",
                    action_type="ACTIVATE_COOLING",
                    parameters={"target_temp": 23},
                    priority=2,
                    timestamp=datetime.now()
                ))
            elif current_temp < 20:
                actions.append(Action(
                    action_id=f"heating_{datetime.now().timestamp()}",
                    action_type="ACTIVATE_HEATING",
                    parameters={"target_temp": 21},
                    priority=2,
                    timestamp=datetime.now()
                ))

        if system_actions['lighting']:
            actions.append(Action(
                action_id=f"lighting_{datetime.now().timestamp()}",
                action_type="ADJUST_ENVIRONMENT",
                parameters={"lights": "on", "optimize_hvac": True},
                priority=3,
                timestamp=datetime.now()
            ))

        if system_actions['security']:
            actions.append(Action(
                action_id=f"security_{datetime.now().timestamp()}",
                action_type="DOOR_NOTIFICATION",
                parameters={"status": "check", "duration_minutes": 5},
                priority=1,
                timestamp=datetime.now()
            ))

        if system_actions['energy_saving']:
            actions.append(Action(
                action_id=f"energy_{datetime.now().timestamp()}",
                action_type="ENERGY_SAVING",
                parameters={"lights": "off", "reduce_hvac": True},
                priority=2,
                timestamp=datetime.now()
            ))

        return sorted(actions, key=lambda x: x.priority)

    def get_learned_rules(self):
        """Get the current set of rules learned by the AI"""
        return self.ai_controller.get_learned_rules()

class ActionExecutor:
    def __init__(self):
        self.action_handlers = {
            "ACTIVATE_COOLING": self._handle_cooling,
            "ACTIVATE_HEATING": self._handle_heating,
            "ACTIVATE_DEHUMIDIFIER": self._handle_dehumidifier,
            "ACTIVATE_HUMIDIFIER": self._handle_humidifier,
            "DOOR_NOTIFICATION": self._handle_door_notification,
            "ACTIVATE_VENTILATION": self._handle_ventilation,
            "ADJUST_ENVIRONMENT": self._handle_environment,
            "ENERGY_SAVING": self._handle_energy_saving
        }

    def execute_action(self, action: Action) -> bool:
        """Execute the given action using the appropriate handler."""
        if action.action_type in self.action_handlers:
            return self.action_handlers[action.action_type](action.parameters)
        return False

    def _handle_cooling(self, params: Dict) -> bool:
        # Implementation would interface with actual HVAC system
        print(f"Activating cooling to {params['target_temp']}°C")
        return True

    def _handle_heating(self, params: Dict) -> bool:
        print(f"Activating heating to {params['target_temp']}°C")
        return True

    def _handle_dehumidifier(self, params: Dict) -> bool:
        print(f"Activating dehumidifier to {params['target_humidity']}%")
        return True

    def _handle_humidifier(self, params: Dict) -> bool:
        print(f"Activating humidifier to {params['target_humidity']}%")
        return True

    def _handle_door_notification(self, params: Dict) -> bool:
        print(f"Door {params['status']} notification sent")
        return True

    def _handle_ventilation(self, params: Dict) -> bool:
        print(f"Activating ventilation: {params['speed']} speed for {params['duration_minutes']} minutes")
        return True

    def _handle_environment(self, params: Dict) -> bool:
        print(f"Adjusting environment: lights={params['lights']}, optimize_hvac={params['optimize_hvac']}")
        return True

    def _handle_energy_saving(self, params: Dict) -> bool:
        print(f"Energy saving mode: lights={params['lights']}, reduce_hvac={params['reduce_hvac']}")
        return True
