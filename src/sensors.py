"""
Smart Home Sensor Management System
Handles sensor data collection and processing for the smart home AI system.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union
from dataclasses import dataclass

class SensorType(Enum):
    TEMPERATURE = "temperature"  # sıcaklık
    HUMIDITY = "humidity"        # nem
    DOOR = "door"               # kapı durumu
    AIR_QUALITY = "air_quality" # hava kalitesi
    PRESENCE = "presence"       # varlık yokluk

@dataclass
class SensorData:
    timestamp: datetime
    sensor_id: str
    sensor_type: SensorType
    value: Union[float, bool, int]
    unit: Optional[str] = None

class BaseSensor:
    def __init__(self, sensor_id: str, sensor_type: SensorType):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.last_reading: Optional[SensorData] = None

    def get_reading(self) -> SensorData:
        """Get the latest reading from the sensor."""
        raise NotImplementedError("Subclasses must implement get_reading()")

class TemperatureSensor(BaseSensor):
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, SensorType.TEMPERATURE)

    def get_reading(self) -> SensorData:
        # In a real implementation, this would read from actual hardware
        return SensorData(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=22.0,  # Example value
            unit="°C"
        )

class HumiditySensor(BaseSensor):
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, SensorType.HUMIDITY)

    def get_reading(self) -> SensorData:
        return SensorData(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=45.0,  # Example value
            unit="%"
        )

class DoorSensor(BaseSensor):
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, SensorType.DOOR)

    def get_reading(self) -> SensorData:
        return SensorData(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=False,  # False = closed, True = open
            unit=None
        )

class AirQualitySensor(BaseSensor):
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, SensorType.AIR_QUALITY)

    def get_reading(self) -> SensorData:
        return SensorData(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=95,  # Example AQI value
            unit="AQI"
        )

class PresenceSensor(BaseSensor):
    def __init__(self, sensor_id: str):
        super().__init__(sensor_id, SensorType.PRESENCE)

    def get_reading(self) -> SensorData:
        return SensorData(
            timestamp=datetime.now(),
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=True,  # True = presence detected
            unit=None
        )

class SensorManager:
    def __init__(self):
        self.sensors: Dict[str, BaseSensor] = {}

    def register_sensor(self, sensor: BaseSensor) -> None:
        """Register a new sensor with the manager."""
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor_data(self, sensor_id: str) -> Optional[SensorData]:
        """Get the latest reading from a specific sensor."""
        if sensor_id in self.sensors:
            return self.sensors[sensor_id].get_reading()
        return None

    def get_all_sensor_data(self) -> Dict[str, SensorData]:
        """Get the latest readings from all sensors."""
        return {
            sensor_id: sensor.get_reading()
            for sensor_id, sensor in self.sensors.items()
        }
