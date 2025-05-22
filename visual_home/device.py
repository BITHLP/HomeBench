
from typing import Any, Dict, List, Callable, Optional, Tuple
import random

AllCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","kitchen","bathroom","foyer","corridor","balcony","garage","store room"]

class LightDevice:
    def __init__(self, state: str):
        self.name = "light"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "brightness": {"value": 100, "lowest": "0", "highest": "100"},
            "color": {"value": (255,255,255)},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_brightness": self.set_brightness,
            "set_color": self.set_color
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_brightness(self, brightness: int):
        if self.state == "off":
            print("Cannot set brightness while device is off.")
        else:
            self.attributes["brightness"]["value"] = brightness
            print(f"Brightness set to {brightness}.")
    
    def set_color(self, color: Tuple[int, int, int]):
        if self.state == "off":
            print("Cannot set color while device is off.")
        else:
            self.attributes["color"]["value"] = color
            print(f"Color set to {color}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["brightness"]["value"] = random.randint(0, 100)
        self.attributes["color"]["value"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return self.get_status()

    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "brightness" in self.attributes.keys():
            for brightness in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_brightness({brightness})", "device": self.name})

                if self.attributes["brightness"]["value"] < brightness:
                    instructions_list.append({"instruction": f"set_brightness({brightness})", "device": self.name, "explain": "increase " + str(brightness-self.attributes["brightness"]["value"]) + " precent"})
                elif self.attributes["brightness"]["value"] > brightness:
                    instructions_list.append({"instruction": f"set_brightness({brightness})", "device": self.name, "explain": "decrease " + str(self.attributes["brightness"]["value"]-brightness) + " precent"})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        for brightness in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_brightness({brightness})", "device": self.name})
        return instructions_list

class AirConditionerDevice:
    def __init__(self, state: str):
        self.name = "air_conditioner"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "temperature": {"value": 25, "lowest": "16", "highest": "30"},
            "mode": {"value": "cool", "options": ["cool", "heat", "fan_only", "dry"]},
            "fan_speed": {"value": "auto", "options": ["auto", "low", "medium", "high"]},
            "swing": {"value": "auto", "options": ["auto", "up", "middle", "down"]},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_temperature": self.set_temperature,
            "set_mode": self.set_mode,
            "set_fan_speed": self.set_fan_speed,
            "set_swing": self.set_swing
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_temperature(self, temperature: int):
        if self.state == "off":
            print("Cannot set temperature while device is off.")
        else:
            self.attributes["temperature"]["value"] = temperature
            print(f"Temperature set to {temperature}.")
    
    def set_mode(self, mode: str):
        if self.state == "off":
            print("Cannot set mode while device is off.")
        elif mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            self.attributes["mode"]["value"] = mode
            print(f"Mode set to {mode}.")

    def set_fan_speed(self, fan_speed: str):
        if self.state == "off":
            print("Cannot set fan speed while device is off.")
        elif fan_speed not in self.attributes["fan_speed"]["options"]:
            print(f"Invalid fan speed: {fan_speed}.")
        else:
            self.attributes["fan_speed"]["value"] = fan_speed
            print(f"Fan speed set to {fan_speed}.")

    def set_swing(self, swing: str):
        if self.state == "off":
            print("Cannot set swing while device is off.")
        elif swing not in self.attributes["swing"]["options"]:
            print(f"Invalid swing: {swing}.")
        else:
            self.attributes["swing"]["value"] = swing
            print(f"Swing set to {swing}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["temperature"]["value"] = random.randint(16, 30)
        self.attributes["mode"]["value"] = random.choice(["cool", "heat", "fan_only", "dry"])
        self.attributes["fan_speed"]["value"] = random.choice(["auto", "low", "medium", "high"])
        self.attributes["swing"]["value"] = random.choice(["auto", "up", "middle", "down"])

        return self.get_status()

    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        
        for temperature in range(16, 31):
            instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name})
            if self.attributes["temperature"]["value"] < temperature:
                instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name, "explain": "increase " + str(temperature-self.attributes["temperature"]["value"])})
            elif self.attributes["temperature"]["value"] > temperature:
                instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name, "explain": "decrease " + str(self.attributes["temperature"]["value"]-temperature)})

        for mode in ["cool", "heat", "fan_only", "dry"]:
            instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})

        fan_speed_list = ["auto", "low", "medium", "high"]
        for fan_speed in ["auto", "low", "medium", "high"]:
            instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name})
            if fan_speed_list.index(self.attributes["fan_speed"]["value"]) < fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "increase " + str(fan_speed_list.index(fan_speed)-fan_speed_list.index(self.attributes["fan_speed"]["value"])) + " level"})
            elif fan_speed_list.index(self.attributes["fan_speed"]["value"]) > fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "decrease " + str(fan_speed_list.index(self.attributes["fan_speed"]["value"])-fan_speed_list.index(fan_speed)) + " level"})

        swing_list = ["auto", "up", "middle", "down"]
        for swing in ["auto", "up", "middle", "down"]:
            instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name})
            if swing_list.index(self.attributes["swing"]["value"]) < swing_list.index(swing) and swing != "auto" and self.attributes["swing"]["value"] != "auto":
                instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name, "explain": "increase " + str(swing_list.index(swing)-swing_list.index(self.attributes["swing"]["value"])) + " level"})
            elif swing_list.index(self.attributes["swing"]["value"]) > swing_list.index(swing) and swing != "auto" and self.attributes["swing"]["value"] != "auto":
                instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name, "explain": "decrease " + str(swing_list.index(self.attributes["swing"]["value"])-swing_list.index(swing)) + " level"})

        return instructions_list

class HeatingDevice:
    def __init__(self, state: str):
        self.name = "heating"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "temperature": {"value": 25, "lowest": "16", "highest": "30"},
            "mode": {"value": "heat", "options": ["heat", "fan_only"]},
            "fan_speed": {"value": "auto", "options": ["auto", "low", "medium", "high"]},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_temperature": self.set_temperature,
            "set_mode": self.set_mode,
            "set_fan_speed": self.set_fan_speed
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_temperature(self, temperature: int):
        if self.state == "off":
            print("Cannot set temperature while device is off.")
        else:
            self.attributes["temperature"]["value"] = temperature
            print(f"Temperature set to {temperature}.")
    
    def set_mode(self, mode: str):
        if self.state == "off":
            print("Cannot set mode while device is off.")
        elif mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            self.attributes["mode"]["value"] = mode
            print(f"Mode set to {mode}.")

    def set_fan_speed(self, fan_speed: str):
        if self.state == "off":
            print("Cannot set fan speed while device is off.")
        elif fan_speed not in self.attributes["fan_speed"]["options"]:
            print(f"Invalid fan speed: {fan_speed}.")
        else:
            self.attributes["fan_speed"]["value"] = fan_speed
            print(f"Fan speed set to {fan_speed}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["temperature"]["value"] = random.randint(16, 30)
        self.attributes["mode"]["value"] = random.choice(["heat", "fan_only"])
        self.attributes["fan_speed"]["value"] = random.choice(["auto", "low", "medium", "high"])
        return self.get_status()

    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "temperature" in self.attributes.keys():
            for temperature in range(16, 31):
                instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name})
                if self.attributes["temperature"]["value"] < temperature:
                    instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name, "explain": "increase " + str(temperature-self.attributes["temperature"]["value"])+ " degree"})
                elif self.attributes["temperature"]["value"] > temperature:
                    instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name, "explain": "decrease " + str(self.attributes["temperature"]["value"]-temperature)+ " degree"})

        if "mode" in self.attributes.keys():
            for mode in ["heat", "fan_only"]:
                instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        
        fan_speed_list = ["auto", "low", "medium", "high"]
        if  "fan_speed" in self.attributes.keys():
            for fan_speed in ["auto", "low", "medium", "high"]:
                instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name})
                if fan_speed_list.index(self.attributes["fan_speed"]["value"]) < fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "increase " + str(fan_speed_list.index(fan_speed)-fan_speed_list.index(self.attributes["fan_speed"]["value"])) + " level"})

                elif fan_speed_list.index(self.attributes["fan_speed"]["value"]) > fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "decrease " + str(fan_speed_list.index(self.attributes["fan_speed"]["value"])-fan_speed_list.index(fan_speed)) + " level"})


        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "temperature" not in self.attributes.keys():
            for temperature in range(16, 31):
                    instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name})
        if "mode" not in self.attributes.keys():
            for mode in ["heat", "fan_only"]:
                    instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if  "fan_speed" not in self.attributes.keys():
            for fan_speed in ["auto", "low", "medium", "high"]:
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name})
        return instructions_list

class FanDevice:
    def __init__(self, state: str):
        self.name = "fan"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "speed": {"value": "auto", "options": ["auto", "low", "medium", "high"]},
            "swing": {"value": "auto", "options": ["auto", "up", "middle", "down"]},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_speed": self.set_speed,
            "set_swing": self.set_swing
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_speed(self, speed: str):
        if self.state == "off":
            print("Cannot set speed while device is off.")
        elif speed not in self.attributes["speed"]["options"]:
            print(f"Invalid speed: {speed}.")
        else:
            self.attributes["speed"]["value"] = speed
            print(f"Speed set to {speed}.")

    def set_swing(self, swing: str):
        if self.state == "off":
            print("Cannot set swing while device is off.")
        elif swing not in self.attributes["swing"]["options"]:
            print(f"Invalid swing: {swing}.")
        else:
            self.attributes["swing"]["value"] = swing
            print(f"Swing set to {swing}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["speed"]["value"] = random.choice(["auto", "low", "medium", "high"])
        self.attributes["swing"]["value"] = random.choice(["auto", "up", "middle", "down"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "speed" in self.attributes.keys():
            fan_speed_list = ["auto", "low", "medium", "high"]
            for speed in ["auto", "low", "medium", "high"]:
                instructions_list.append({"instruction": f"set_speed({speed})", "device": self.name})
                if fan_speed_list.index(self.attributes["speed"]["value"]) < fan_speed_list.index(speed) and speed != "auto" and self.attributes["speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_speed({speed})", "device": self.name, "explain": "increase " + str(fan_speed_list.index(speed)-fan_speed_list.index(self.attributes["speed"]["value"])) + " level"})
                elif fan_speed_list.index(self.attributes["speed"]["value"]) > fan_speed_list.index(speed) and speed != "auto" and self.attributes["speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_speed({speed})", "device": self.name, "explain": "decrease " + str(fan_speed_list.index(self.attributes["speed"]["value"])-fan_speed_list.index(speed)) + " level"})
        
        if "swing" in self.attributes.keys():
            swing_list = ["auto", "up", "middle", "down"]
            for swing in ["auto", "up", "middle", "down"]:
                instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name})
                if swing_list.index(self.attributes["swing"]["value"]) < swing_list.index(swing) and swing != "auto" and self.attributes["swing"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name, "explain": "increase " + str(swing_list.index(swing)-swing_list.index(self.attributes["swing"]["value"])) + " level"})
                elif swing_list.index(self.attributes["swing"]["value"]) > swing_list.index(swing) and swing != "auto" and self.attributes["swing"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name, "explain": "decrease " + str(swing_list.index(self.attributes["swing"]["value"])-swing_list.index(swing)) + " level"})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "speed" not in self.attributes.keys():
            for speed in ["auto", "low", "medium", "high"]:
                    instructions_list.append({"instruction": f"set_speed({speed})", "device": self.name})
        if "swing" not in self.attributes.keys():
            for swing in ["auto", "up", "middle", "down"]:
                    instructions_list.append({"instruction": f"set_swing({swing})", "device": self.name})
        return instructions_list

class GarageDoorDevice:
    def __init__(self, state: str):
        self.name = "garage_door"
        self.state = state  # e.g., "open", "closed",
        self.attributes = {}
        self.operations = {
            "open": self.open,
            "close": self.close
        }

    def open(self):
        self.state = "open"
        print("Door is now OPEN.")

    def close(self):
        self.state = "closed"
        print("Door is now CLOSED.")
    
    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["open", "closed"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "open()", "device": self.name})
        instructions_list.append({"instruction": "close()", "device": self.name})
        return instructions_list

class BlindsDevice:
    def __init__(self, state: str):
        self.name = "blinds"
        self.state = state  # e.g., "open", "closed",
        self.attributes = {}
        self.operations = {
            "open": self.open,
            "close": self.close
        }

    def open(self):
        self.state = "open"
        print("Blinds is now OPEN.")

    def close(self):
        self.state = "closed"
        print("Blinds is now CLOSED.")
    
    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["open", "closed"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "open()", "device": self.name})
        instructions_list.append({"instruction": "close()", "device": self.name})
        return instructions_list
    
class CurtainDevice:
    def __init__(self, state: str):
        self.name = "curtain"
        self.state = state  # e.g., "open", "closed",
        self.attributes = {
            " degree": {"value":0, "lowest":0, "highest":"100"}
        }
        self.operations = {
            "open": self.open,
            "close": self.close,
            "set_ degree": self.set_degree
        }
    
    def open(self):
        self.state = "open"
        print("Curtain is now OPEN.")

    def close(self):
        self.state = "closed"
        print("Curtain is now CLOSED.")

    def set_degree(self,  degree: int):
        self.attributes[" degree"]["value"] =  degree
        print(f"Temperature set to { degree}.")

    
    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["open", "closed"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "open()", "device": self.name})
        instructions_list.append({"instruction": "close()", "device": self.name})
        if " degree" in self.attributes.keys():
            for  degree in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_ degree({ degree})", "device": self.name})
                if self.attributes[" degree"]["value"] <  degree:
                    instructions_list.append({"instruction": f"set_ degree({ degree})", "device": self.name, "explain": "increase " + str( degree-self.attributes[" degree"]["value"]) + " precent"})
                elif self.attributes[" degree"]["value"] >  degree:
                    instructions_list.append({"instruction": f"set_ degree({ degree})", "device": self.name, "explain": "decrease " + str(self.attributes[" degree"]["value"]- degree) + " precent"})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if " degree" not in self.attributes.keys():
            for  degree in range(0, 101, 10):
                    instructions_list.append({"instruction": f"set_ degree({ degree})", "device": self.name})
        return instructions_list

class AirPurifiersDevice:
    def __init__(self, state: str):
        self.name = "air_purifiers"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "mode": {"value": "auto", "options": ["auto", "sleep"]},
            "fan_speed": {"value": "auto", "options": ["auto", "low", "medium", "high"]},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_mode": self.set_mode,
            "set_fan_speed": self.set_fan_speed,
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_mode(self, mode: str):
        if self.state == "off":
            print("Cannot set mode while device is off.")
        elif mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            self.attributes["mode"]["value"] = mode
            print(f"Mode set to {mode}.")

    def set_fan_speed(self, fan_speed: str):
        if self.state == "off":
            print("Cannot set fan speed while device is off.")
        elif fan_speed not in self.attributes["fan_speed"]["options"]:
            print(f"Invalid fan speed: {fan_speed}.")
        else:
            self.attributes["fan_speed"]["value"] = fan_speed
            print(f"Fan speed set to {fan_speed}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
        
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["mode"]["value"] = random.choice(["auto", "sleep"])
        self.attributes["fan_speed"]["value"] = random.choice(["auto", "low", "medium", "high"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "mode" in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "fan_speed" in self.attributes.keys():
            fan_speed_list = ["auto", "low", "medium", "high"]
            for fan_speed in ["auto", "low", "medium", "high"]:
                instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name})
                if fan_speed_list.index(self.attributes["fan_speed"]["value"]) < fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "increase " + str(fan_speed_list.index(fan_speed)-fan_speed_list.index(self.attributes["fan_speed"]["value"])) + " level"})
                elif fan_speed_list.index(self.attributes["fan_speed"]["value"]) > fan_speed_list.index(fan_speed) and fan_speed != "auto" and self.attributes["fan_speed"]["value"] != "auto":
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name, "explain": "decrease " + str(fan_speed_list.index(self.attributes["fan_speed"]["value"])-fan_speed_list.index(fan_speed)) + " level"})
        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "mode" not in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                    instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "fan_speed" not in self.attributes.keys():
            for fan_speed in ["auto", "low", "medium", "high"]:
                    instructions_list.append({"instruction": f"set_fan_speed({fan_speed})", "device": self.name})
        return instructions_list

class WaterHeaterDevice:
    def __init__(self, state: str):
        self.name = "water_heater"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "temperature": {"value": 60, "lowest": "30", "highest": "100"},
            "mode": {"value": "heating", "options": ["heating", "eco"]},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_temperature": self.set_temperature,
            "set_mode": self.set_mode
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")

    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_temperature(self, temperature: int):
        if self.state == "off":
            print("Cannot set temperature while device is off.")
        else:
            self.attributes["temperature"]["value"] = temperature
            print(f"Temperature set to {temperature}.")
    
    def set_mode(self, mode: str):
        if self.state == "off":
            print("Cannot set mode while device is off.")
        elif mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            self.attributes["mode"]["value"] = mode
            print(f"Mode set to {mode}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["temperature"]["value"] = random.randint(30, 100)
        self.attributes["mode"]["value"] = random.choice(["heating", "eco"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "temperature" in self.attributes.keys():
            for temperature in range(30, 101,5):
                instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name})
        if "mode" in self.attributes.keys():
            for mode in ["heating", "eco"]:
                instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "temperature" not in self.attributes.keys():
            for temperature in range(30, 101,5):
                    instructions_list.append({"instruction": f"set_temperature({temperature})", "device": self.name})
        if "mode" not in self.attributes.keys():
            for mode in ["heating", "eco"]:
                    instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        return instructions_list

class MediaPlayerDevice:
    def __init__(self, state: str):
        self.name = "media_player"
        self.state = state  # e.g., "playing", "paused", "stopped"
        self.attributes = {
            "volume": {"value": 50, "lowest": "0", "highest": "100"},
        }
        self.operations = {
            "play": self.play,
            "pause": self.pause,
            "stop": self.stop,
            "set_volume": self.set_volume,
            "set_song": self.set_song,
            "set_artist": self.set_artist,
            "set_style": self.set_style
        }

    def play(self):
        self.state = "playing"
        print("Media is now PLAYING.")
    
    def pause(self):
        self.state = "paused"
        print("Media is now PAUSED.")
    
    def stop(self):
        self.state = "stopped"
        print("Media is now STOPPED.")

    def set_volume(self, volume: int):
        self.attributes["volume"]["value"] = volume
        print(f"Volume set to {volume}.")

    def set_song(self, song: str):
        print(f"Song set to {song}.")

    def set_artist(self, artist: str):
        print(f"Artist set to {artist}.")

    def set_style(self, style: str):
        print(f"Style set to {style}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["playing", "paused", "stopped"])
        self.attributes["volume"]["value"] = random.randint(0, 100) 
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "play()", "device": self.name})
        instructions_list.append({"instruction": "pause()", "device": self.name})
        instructions_list.append({"instruction": "stop()", "device": self.name})
        for volume in range(0, 101, 10):
            instructions_list.append({"instruction": f"set_volume({volume})", "device": self.name})
            if self.attributes["volume"]["value"] < volume:
                instructions_list.append({"instruction": f"set_volume({volume})", "device": self.name, "explain": "increase " + str(volume-self.attributes["volume"]["value"]) + ' precent'})
            elif self.attributes["volume"]["value"] > volume:
                instructions_list.append({"instruction": f"set_volume({volume})", "device": self.name, "explain": "decrease " + str(self.attributes["volume"]["value"]-volume) + ' precent'})

        return instructions_list      

class VacuumRobotrDevice:
    def __init__(self, state: str):
        self.name = "vacuum_robot"
        self.state = state  # e.g., "cleaning", "charging", "stopped", "paused"
        self.attributes = {
            "battery": {"value": 100, "lowest": 0, "highest": 100},
            "mode": {"value": "auto", "options": ["auto", "strong", "sleep"]},
        }
        self.operations = {
            "start": self.start,
            "pause": self.pause,
            "stop": self.stop,
            "charge": self.charge,
            "set_mode": self.set_mode,
            "set_cleaning_area": self.set_cleaning_area
        }

    def start(self):
        self.state = "cleaning"
        print("Vacuum is now CLEANING.")
    
    def pause(self):
        self.state = "paused"
        print("Vacuum is now PAUSED.")
    
    def stop(self):
        self.state = "stopped"
        print("Vacuum is now STOPPED.")

    def charge(self):
        self.state = "charging"
        print("Vacuum is now CHARGING.")

    def set_mode(self, mode: str):
        if mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            self.attributes["mode"]["value"] = mode
            print(f"Mode set to {mode}.")

    def set_cleaning_area(self, area: str):
        print(f"Cleaning area set to {area}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["cleaning", "charging", "stopped", "paused"])
        self.attributes["battery"]["value"] = random.randint(0, 100)
        self.attributes["mode"]["value"] = random.choice(["auto", "strong", "sleep"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "start()", "device": self.name})
        instructions_list.append({"instruction": "pause()", "device": self.name})
        instructions_list.append({"instruction": "stop()", "device": self.name})
        instructions_list.append({"instruction": "charge()", "device": self.name})
        for mode in ["auto", "strong", "sleep"]:
            instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})

        for area in AllCandiateRoom:
            instructions_list.append({"instruction": f"set_cleaning_area({area})", "device": self.name})

        return instructions_list

class AromatherapyDevice:
    def __init__(self, state: str):
        self.name = "aromatherapy"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "intensity": {"value": 50, "lowest": "0", "highest": "100"},
            "interval": {"value": 30, "lowest": "10", "highest": "60"},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_intensity": self.set_intensity,
            "set_interval": self.set_interval
        }

    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")
    
    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")

    def set_intensity(self, intensity: int):
        self.attributes["intensity"]["value"] = intensity
        print(f"Intensity set to {intensity}.")

    def set_interval(self, interval: int):
        self.attributes["interval"]["value"] = interval
        print(f"Interval set to {interval}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["intensity"]["value"] = random.randint(0, 100)
        self.attributes["interval"]["value"] = random.randint(10, 60)
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "intensity" in self.attributes.keys():
            for intensity in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
                if self.attributes["intensity"]["value"] < intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "increase  " + str(intensity-self.attributes["intensity"]["value"]) + '  precent'})
                elif self.attributes["intensity"]["value"] > intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "decrease  " + str(self.attributes["intensity"]["value"]-intensity) + '  precent'})
                
        if "interval" in self.attributes.keys():
            for interval in range(10, 61, 10):
                instructions_list.append({"instruction": f"set_interval({interval})", "device": self.name})
                if self.attributes["interval"]["value"] < interval:
                    instructions_list.append({"instruction": f"set_interval({interval})", "device": self.name, "explain": "increase  " + str(interval-self.attributes["interval"]["value"]) + ' second'})
                elif self.attributes["interval"]["value"] > interval:
                    instructions_list.append({"instruction": f"set_interval({interval})", "device": self.name, "explain": "decrease  " + str(self.attributes["interval"]["value"]-interval) + ' second'})

        return instructions_list

    def generate_unexist_instructions(self):
        instructions_list = []
        if "intensity" not in self.attributes.keys():
            for intensity in range(0, 101, 10):
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
        if "interval" not in self.attributes.keys():
            for interval in range(10, 61, 10):
                    instructions_list.append({"instruction": f"set_interval({interval})", "device": self.name})
        return instructions_list

class TrashDevice:
    def __init__(self, state: str):
        self.name = "trash"
        self.state = state  # e.g., "full", "empty", "not_full"
        self.attributes = {}
        self.operations = {
            "pack": self.pack
        }

    def pack(self):
        self.state = "empty"
        print("Trash is now empty.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["full", "empty", "not_full"])
        return self.get_status()

    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "pack()", "device": self.name})
        return instructions_list

class HumidifierDevice:
    def __init__(self, state: str):
        self.name = "humidifier"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "mode": {"value": "auto", "options": ["auto", "sleep"]},
            "intensity": {"value": 50, "lowest": 0, "highest": 100},
            "tank": {"value": 100, "lowest": 0, "highest": 100}
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_mode": self.set_mode,
            "set_intensity": self.set_intensity
        }

    def turn_on(self):
        self.state = "on"
        if self.attributes["tank"]["value"] == 0:
            print("Cannot turn on while tank is empty.")
        else:
            print("Device is now ON.")
    
    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")

    def set_mode(self, mode: str):
        if mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            if self.attributes["tank"]["value"] == 0:
                print("Cannot turn on while tank is empty.")
            else:
                self.attributes["mode"]["value"] = mode
                print(f"Mode set to {mode}.")

    def set_intensity(self, intensity: int):
        if self.attributes["tank"]["value"] == 0:
            print("Cannot turn on while tank is empty.")
        else:
            self.attributes["intensity"]["value"] = intensity
            print(f"Intensity set to {intensity}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["mode"]["value"] = random.choice(["auto", "sleep"])
        self.attributes["intensity"]["value"] = random.randint(0, 100)
        return self.get_status()

    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "mode" in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "intensity" in self.attributes.keys():
            for intensity in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
                if self.attributes["intensity"]["value"] < intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "increase  " + str(intensity-self.attributes["intensity"]["value"]) + '  precent'})
                elif self.attributes["intensity"]["value"] > intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "decrease  " + str(self.attributes["intensity"]["value"]-intensity) + '  precent'})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "mode" not in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                    instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "intensity" not in self.attributes.keys():
            for intensity in range(0, 101, 10):
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
        return instructions_list

class DehumidifiersDevice:
    def __init__(self, state: str):
        self.name = "dehumidifiers"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "mode": {"value": "auto", "options": ["auto", "sleep"]},
            "intensity": {"value": 50, "lowest": "0", "highest": "100"},
            "tank": {"value": 0, "lowest": "0", "highest": "100"}
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_mode": self.set_mode,
            "set_intensity": self.set_intensity
        }

    def turn_on(self):
        self.state = "on"
        if self.attributes["tank"]["value"] == 100:
            print("Cannot turn on while tank is full.")
        else:
            print("Device is now ON.")
    
    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")

    def set_mode(self, mode: str):
        if mode not in self.attributes["mode"]["options"]:
            print(f"Invalid mode: {mode}.")
        else:
            if self.attributes["tank"]["value"] == 100:
                print("Cannot turn on while tank is full.")
            else:
                self.attributes["mode"]["value"] = mode
                print(f"Mode set to {mode}.")

    def set_intensity(self, intensity: int):
        if self.attributes["tank"]["value"] == 100:
            print("Cannot turn on while tank is full.")
        else:
            self.attributes["intensity"]["value"] = intensity
            print(f"Intensity set to {intensity}.")

    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }

    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["mode"]["value"] = random.choice(["auto", "sleep"])
        self.attributes["intensity"]["value"] = random.randint(0, 100)
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        if "mode" in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "intensity" in self.attributes.keys():
            for intensity in range(0, 101, 10):
                instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
                if self.attributes["intensity"]["value"] < intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "increase  " + str(intensity-self.attributes["intensity"]["value"]) + '  precent'})
                elif self.attributes["intensity"]["value"] > intensity:
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name, "explain": "decrease  " + str(self.attributes["intensity"]["value"]-intensity) + '  precent'})

        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "mode" not in self.attributes.keys():
            for mode in ["auto", "sleep"]:
                    instructions_list.append({"instruction": f"set_mode({mode})", "device": self.name})
        if "intensity" not in self.attributes.keys():
            for intensity in range(0, 101, 10):
                    instructions_list.append({"instruction": f"set_intensity({intensity})", "device": self.name})
        return instructions_list
    
class PetFeederDevice:
    def __init__(self, state: str):
        self.name = "pet_feeder"
        self.state = state  # e.g., "on", "off"
        self.attributes = {
            "feeding_interval": {"value": 24, "lowest": 1, "highest": 24},
            "feeding_weight": {"value": 50, "lowest": 0, "highest": 100},
        }
        self.operations = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_feeding_interval": self.set_feeding_interval,
            "set_feeding_weight": self.set_feeding_weight,
            "feed": self.feed
        }
    
    def turn_on(self):
        self.state = "on"
        print("Device is now ON.")
    
    def turn_off(self):
        self.state = "off"
        print("Device is now OFF.")
    
    def set_feeding_interval(self, feeding_interval: int):
        self.attributes["feeding_interval"]["value"] = feeding_interval
        print(f"Feeding interval set to {feeding_interval}.")
    
    def set_feeding_weight(self, feeding_weight: int):
        self.attributes["feeding_weight"]["value"] = feeding_weight
        print(f"Feeding weight set to {feeding_weight}.")

    def feed(self):
        if self.state == "off":
            print("Cannot feed while device is off.")
        else:
            print("Feeding.")
        
    def initialize(self, state: str, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes = attributes

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.state = random.choice(["on", "off"])
        self.attributes["feeding_interval"]["value"] = random.randint(1, 24)
        self.attributes["feeding_weight"]["value"] = random.randint(0, 100)
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        instructions_list.append({"instruction": "turn_on()", "device": self.name})
        instructions_list.append({"instruction": "turn_off()", "device": self.name})
        for feeding_interval in range(1, 25):
            instructions_list.append({"instruction": f"set_feeding_interval({feeding_interval})", "device": self.name, "explain": "set feeding interval to " + str(feeding_interval) + ' hour'})
        for feeding_weight in range(0, 101, 10):
            instructions_list.append({"instruction": f"set_feeding_weight({feeding_weight})", "device": self.name}, "explain": "set feeding weight to " + str(feeding_weight) + ' gram')
            if self.attributes["feeding_weight"]["value"] < feeding_weight:
                instructions_list.append({"instruction": f"set_feeding_weight({feeding_weight})", "device": self.name, "explain": "increase  " + str(feeding_weight-self.attributes["feeding_weight"]["value"]) + '  precent'})
            elif self.attributes["feeding_weight"]["value"] > feeding_weight:
                instructions_list.append({"instruction": f"set_feeding_weight({feeding_weight})", "device": self.name, "explain": "decrease  " + str(self.attributes["feeding_weight"]["value"]-feeding_weight) + '  precent'})
        instructions_list.append({"instruction": "feed()", "device": self.name})
        return instructions_list
    
    def generate_unexist_instructions(self):
        instructions_list = []
        if "feeding_interval" not in self.attributes.keys():
            for feeding_interval in range(1, 25):
                    instructions_list.append({"instruction": f"set_feeding_interval({feeding_interval})", "device": self.name})
        if "feeding_weight" not in self.attributes.keys():
            for feeding_weight in range(0, 101, 10):
                    instructions_list.append({"instruction": f"set_feeding_weight({feeding_weight})", "device": self.name})
        return instructions_list

class BedDevice:
    def __init__(self):
        self.name = "bed"
        self.attributes = {
            "angle": {"value": 0, "lowest": 0, "highest": 60},
            "massage": {"value": "off", "options": ["off", "low", "medium", "high"]}
        }

    def set_angle(self, angle: int):
        self.attributes["angle"]["value"] = angle
        print(f"Angle set to {angle}.")

    def set_massage(self, massage: str):
        self.attributes["massage"]["value"] = massage
        print(f"Massage set to {massage}.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "attributes": self.attributes
        }
    
    def random_initialize(self):
        self.attributes["angle"]["value"] = random.randint(0, 60)
        self.attributes["massage"]["value"] = random.choice(["off", "low", "medium", "high"])
        return self.get_status()
    
    def generate_instructions(self):
        instructions_list = []
        for angle in range(0, 61, 10):
            instructions_list.append({"instruction": f"set_angle({angle})", "device": self.name})
            if self.attributes["angle"]["value"] < angle:
                instructions_list.append({"instruction": f"set_angle({angle})", "device": self.name, "explain": "increase  " + str(angle-self.attributes["angle"]["value"]) + '  degree'})
            elif self.attributes["angle"]["value"] > angle:
                instructions_list.append({"instruction": f"set_angle({angle})", "device": self.name, "explain": "decrease  " + str(self.attributes["angle"]["value"]-angle) + '  degree'})
        for massage in ["off", "low", "medium", "high"]:
            instructions_list.append({"instruction": f"set_massage({massage})", "device": self.name})
        return instructions_list
    

        


LightDeviceInitialAttributes = {
    "brightness": {"value": random.randint(0, 100), "lowest": 0, "highest": 100},
    "color": {"value": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
}
def generate_light_subclass(attributes, operations):
    class SubClass(LightDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: LightDeviceInitialAttributes[attr] for attr in attributes if attr in LightDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

LightDeviceSubClass1 = generate_light_subclass([], ["turn_on", "turn_off"])
LightDeviceSubClass2 = generate_light_subclass(["brightness"], ["turn_on", "turn_off", "set_brightness"])
LightDeviceSubClass3 = generate_light_subclass(["color"], ["turn_on", "turn_off", "set_color"])

LightDeviceList = [LightDevice, LightDeviceSubClass1, LightDeviceSubClass2, LightDeviceSubClass3]

AirConditionerDeviceList = [AirConditionerDevice]

HeatingDeviceInitialAttributes = {
    "temperature": {"value": random.randint(30, 100), "lowest": 30, "highest": 100},
    "mode": {"value": random.choice(["heat", "fan_only"]), "options": ["heat", "fan_only"]},
    "fan_speed": {"value": random.choice(["auto", "low", "medium", "high"]), "options": ["auto", "low", "medium", "high"]}
}

def generate_heating_subclass(attributes, operations):
    class SubClass(HeatingDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: HeatingDeviceInitialAttributes[attr] for attr in attributes if attr in HeatingDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

HeatingDeviceSubClass1 = generate_heating_subclass([], ["turn_on", "turn_off"])
HeatingDeviceSubClass2 = generate_heating_subclass(["temperature"], ["turn_on", "turn_off", "set_temperature"])
HeatingDeviceSubClass3 = generate_heating_subclass(["mode"], ["turn_on", "turn_off", "set_mode"])
HeatingDeviceSubClass4 = generate_heating_subclass(["fan_speed"], ["turn_on", "turn_off", "set_fan_speed"])
HeatingDeviceSubClass5 = generate_heating_subclass(["temperature", "mode"], ["turn_on", "turn_off", "set_temperature", "set_mode"])
HeatingDeviceSubClass6 = generate_heating_subclass(["temperature", "fan_speed"], ["turn_on", "turn_off", "set_temperature", "set_fan_speed"])
HeatingDeviceSubClass7 = generate_heating_subclass(["mode", "fan_speed"], ["turn_on", "turn_off", "set_mode", "set_fan_speed"])

HeatingDeviceList = [HeatingDevice, HeatingDeviceSubClass1, HeatingDeviceSubClass2, HeatingDeviceSubClass3, HeatingDeviceSubClass4, HeatingDeviceSubClass5, HeatingDeviceSubClass6, HeatingDeviceSubClass7]

FanDeviceInitialAttributes = {
    "speed": {"value": random.choice(["auto", "low", "medium", "high"]), "options": ["auto", "low", "medium", "high"]},
    "swing": {"value": random.choice(["auto", "up", "middle", "down"]), "options": ["auto", "up", "middle", "down"]}
}

def generate_fan_subclass(attributes, operations):
    class SubClass(FanDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: FanDeviceInitialAttributes[attr] for attr in attributes if attr in FanDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

FanDeviceSubClass1 = generate_fan_subclass([], ["turn_on", "turn_off"])
FanDeviceSubClass2 = generate_fan_subclass(["speed"], ["turn_on", "turn_off", "set_speed"])
FanDeviceSubClass3 = generate_fan_subclass(["swing"], ["turn_on", "turn_off", "set_swing"])

FanDeviceList = [FanDevice, FanDeviceSubClass1, FanDeviceSubClass2, FanDeviceSubClass3]

GarageDoorDeviceList = [GarageDoorDevice]

BlindsDeviceList = [BlindsDevice]

CurtainDeviceList = [CurtainDevice]

AirPurifiersDeviceInitialAttributes = {
    "mode":{"value": random.choice(["auto", "sleep"]), "options": ["auto", "sleep"]},
    "fan_speed": {"value": random.choice(["auto", "low", "medium", "high"]), "options": ["auto", "low", "medium", "high"]}
}

def generate_air_purifiers_subclass(attributes, operations):
    class SubClass(AirPurifiersDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: AirPurifiersDeviceInitialAttributes[attr] for attr in attributes if attr in AirPurifiersDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

AirPurifiersDeviceSubClass1 = generate_air_purifiers_subclass([], ["turn_on", "turn_off"])
AirPurifiersDeviceSubClass2 = generate_air_purifiers_subclass(["mode"], ["turn_on", "turn_off", "set_mode"])
AirPurifiersDeviceSubClass3 = generate_air_purifiers_subclass(["fan_speed"], ["turn_on", "turn_off", "set_fan_speed"])

AirPurifiersDeviceList = [AirPurifiersDevice, AirPurifiersDeviceSubClass1, AirPurifiersDeviceSubClass2, AirPurifiersDeviceSubClass3]

WaterHeaterDeviceInitialAttributes = {
    "temperature": {"value": random.randint(30, 100), "lowest": 30, "highest": 100},
    "mode": {"value": random.choice(["heating", "eco"]), "options": ["heating", "eco"]}
}

def generate_water_heater_subclass(attributes, operations):
    class SubClass(WaterHeaterDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: WaterHeaterDeviceInitialAttributes[attr] for attr in attributes if attr in WaterHeaterDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

WaterHeaterDeviceSubClass1 = generate_water_heater_subclass([], ["turn_on", "turn_off"])
WaterHeaterDeviceSubClass2 = generate_water_heater_subclass(["temperature"], ["turn_on", "turn_off", "set_temperature"])
WaterHeaterDeviceSubClass3 = generate_water_heater_subclass(["mode"], ["turn_on", "turn_off", "set_mode"])

WaterHeaterDeviceList = [WaterHeaterDevice, WaterHeaterDeviceSubClass1, WaterHeaterDeviceSubClass2, WaterHeaterDeviceSubClass3]

MediaPlayerDeviceList = [MediaPlayerDevice]

VacuumRobotrDeviceList = [VacuumRobotrDevice]

AromatherapyDeviceInitialAttributes = {
    "intensity": {"value": random.randint(0, 100), "lowest": 0, "highest": 100},
    "interval": {"value": random.randint(10, 60), "lowest": 10, "highest": 60}
}

def generate_aromatherapy_subclass(attributes, operations):
    class SubClass(AromatherapyDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: AromatherapyDeviceInitialAttributes[attr] for attr in attributes if attr in AromatherapyDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

AromatherapyDeviceSubClass1 = generate_aromatherapy_subclass([], ["turn_on", "turn_off"])
AromatherapyDeviceSubClass2 = generate_aromatherapy_subclass(["intensity"], ["turn_on", "turn_off", "set_intensity"])
AromatherapyDeviceSubClass3 = generate_aromatherapy_subclass(["interval"], ["turn_on", "turn_off", "set_interval"])

AromatherapyDeviceList = [AromatherapyDevice, AromatherapyDeviceSubClass1, AromatherapyDeviceSubClass2, AromatherapyDeviceSubClass3]

TrashDeviceList = [TrashDevice]

HumidifierDeviceInitialAttributes = {
    "mode": {"value": random.choice(["auto", "sleep"]), "options": ["auto", "sleep"]},
    "intensity": {"value": random.randint(0, 100), "lowest": 0, "highest": 100}
}

def generate_humidifier_subclass(attributes, operations):
    class SubClass(HumidifierDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: HumidifierDeviceInitialAttributes[attr] for attr in attributes if attr in HumidifierDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

HumidifierDeviceSubClass1 = generate_humidifier_subclass([], ["turn_on", "turn_off"])
HumidifierDeviceSubClass2 = generate_humidifier_subclass(["mode"], ["turn_on", "turn_off", "set_mode"])
HumidifierDeviceSubClass3 = generate_humidifier_subclass(["intensity"], ["turn_on", "turn_off", "set_intensity"])

HumidifierDeviceList = [HumidifierDevice, HumidifierDeviceSubClass1, HumidifierDeviceSubClass2, HumidifierDeviceSubClass3]

DehumidifiersDeviceInitialAttributes = {
    "mode": {"value": random.choice(["auto", "sleep"]), "options": ["auto", "sleep"]},
    "intensity": {"value": random.randint(0, 100), "lowest": 0, "highest": 100},
}



def generate_dehumidifiers_subclass(attributes, operations):
    class SubClass(DehumidifiersDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])

            return self.get_status()
            
    return SubClass

DehumidifiersDeviceSubClass1 = generate_dehumidifiers_subclass([], ["turn_on", "turn_off"])
DehumidifiersDeviceSubClass2 = generate_dehumidifiers_subclass(["mode"], ["turn_on", "turn_off", "set_mode"])
DehumidifiersDeviceSubClass3 = generate_dehumidifiers_subclass(["intensity"], ["turn_on", "turn_off", "set_intensity"])

DehumidifiersDeviceList = [DehumidifiersDevice, DehumidifiersDeviceSubClass1, DehumidifiersDeviceSubClass2, DehumidifiersDeviceSubClass3]

PetFeederDeviceInitialAttributes = {
    "feeding_interval": {"value": random.randint(1, 24), "lowest": 1, "highest": 24},
    "feeding_weight": {"value": random.randint(0, 100), "lowest": 0, "highest": 100}
}

def generate_pet_feeder_subclass(attributes, operations):
    class SubClass(PetFeederDevice):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}

        def random_initialize(self):
            self.state = random.choice(["on", "off"])
            self.attributes = {attr: PetFeederDeviceInitialAttributes[attr] for attr in attributes if attr in PetFeederDeviceInitialAttributes}
            return self.get_status()
            
    return SubClass

PetFeederDeviceSubClass1 = generate_pet_feeder_subclass([], ["turn_on", "turn_off"])
PetFeederDeviceSubClass2 = generate_pet_feeder_subclass(["feeding_interval"], ["turn_on", "turn_off", "set_feeding_interval"])
PetFeederDeviceSubClass3 = generate_pet_feeder_subclass(["feeding_weight"], ["turn_on", "turn_off", "set_feeding_weight"])

PetFeederDeviceList = [PetFeederDevice, PetFeederDeviceSubClass1, PetFeederDeviceSubClass2, PetFeederDeviceSubClass3]

device_map = {
    "light": LightDevice,
    "heating": HeatingDevice,
    "fan": FanDevice,
    "air_conditioner": AirConditionerDevice,
    "garage_door": GarageDoorDevice,
    "blinds": BlindsDevice,
    "curtain": CurtainDevice,
    "media_player": MediaPlayerDevice,
    "vacuum_robot": VacuumRobotrDevice,
    "trash": TrashDevice,
    "humidifier": HumidifierDevice,
    "dehumidifiers": DehumidifiersDevice,
    "aromatherapy": AromatherapyDevice,
    "water_heater": WaterHeaterDevice,
    "air_purifiers": AirPurifiersDevice,
    "pet_feeder": PetFeederDevice
}