from .ai_model import SmartHomeAI
import threading
import time

class AIController:
    def __init__(self):
        self.ai = SmartHomeAI()
        self.lock = threading.Lock()
        self._start_training_thread()

    def _start_training_thread(self):
        def training_loop():
            while True:
                with self.lock:
                    self.ai.train_model()
                time.sleep(300)  # Train every 5 minutes

        thread = threading.Thread(target=training_loop, daemon=True)
        thread.start()

    def process_sensor_data(self, sensor_data):
        with self.lock:
            return self.ai.process_sensor_data(sensor_data)

    def get_learned_rules(self):
        with self.lock:
            return self.ai.get_learned_rules()
