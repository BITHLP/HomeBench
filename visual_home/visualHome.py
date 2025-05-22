from device import *
import json
import random
import inspect


AllCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","kitchen","bathroom","foyer","corridor","balcony","garage","store room"]
LightCandiateRoom = AllCandiateRoom ## 每个屋子都有
AirConditionerCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room"] ## 每个屋子都有
HeatingCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room"]  
FanCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room"]  ## 风扇加加热器等价于空调
GarageDoorCandiateRoom = ["garage"] 
BlindsCandiateRoom = ["ding room","kitchen","bathroom","garage"]
CurtainsCandiateRoom = ["master bedroom","guest bedroom","living room","study room","balcony"]
AirPurifiersCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room","garage"]
AromatherapyCandiateRoom = AllCandiateRoom 
TrashCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","kitchen","bathroom","balcony","garage","store room"]
HumidifierCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room"]
DehumidifiersCandiateRoom = ["master bedroom","guest bedroom","living room","ding room","study room","store room"]

def generate_instructions():
    instructions = []
    l = LightDevice("on")
    for room in LightCandiateRoom:
        light_instruction = l.generate_instructions()
        for instr in light_instruction:
            instr["room"] = room
            instructions.append(instr)
    a = AirConditionerDevice("on")
    for room in AirConditionerCandiateRoom:
        air_conditioner_instruction = a.generate_instructions()
        for instr in air_conditioner_instruction:
            instr["room"] = room
            instructions.append(instr)
    h = HeatingDevice("on")
    for room in HeatingCandiateRoom:
        heating_instruction = h.generate_instructions()
        for instr in heating_instruction:
            instr["room"] = room
            instructions.append(instr)
    f = FanDevice("on")
    for room in FanCandiateRoom:
        fan_instruction = f.generate_instructions()
        for instr in fan_instruction:
            instr["room"] = room
            instructions.append(instr)
    g = GarageDoorDevice("open")
    for room in GarageDoorCandiateRoom:
        garage_door_instruction = g.generate_instructions()
        for instr in garage_door_instruction:
            instr["room"] = room
            instructions.append(instr)
    b = BlindsDevice("close")
    for room in BlindsCandiateRoom:
        blinds_instruction = b.generate_instructions()
        for instr in blinds_instruction:
            instr["room"] = room
            instructions.append(instr)

    c = CurtainDevice("close")
    for room in CurtainsCandiateRoom:
        curtains_instruction = c.generate_instructions()
        for instr in curtains_instruction:
            instr["room"] = room
            instructions.append(instr)

    a = AirPurifiersDevice("on")
    for room in AirPurifiersCandiateRoom:
        air_purifiers_instruction = a.generate_instructions()
        for instr in air_purifiers_instruction:
            instr["room"] = room
            instructions.append(instr)

    w = WaterHeaterDevice("on")
    water_heater_instruction = w.generate_instructions()
    instructions.extend(water_heater_instruction)

    m = MediaPlayerDevice("play")
    media_player_instruction = m.generate_instructions()
    instructions.extend(media_player_instruction)

    v = VacuumRobotrDevice("on")
    vacuum_robot_instruction = v.generate_instructions()
    instructions.extend(vacuum_robot_instruction)

    a = AromatherapyDevice("on")
    for room in AromatherapyCandiateRoom:
        aromatherapy_instruction = a.generate_instructions()
        for instr in aromatherapy_instruction:
            instr["room"] = room
            instructions.append(instr)

    t = TrashDevice("open")
    for room in TrashCandiateRoom:
        trash_instruction = t.generate_instructions()
        for instr in trash_instruction:
            instr["room"] = room
            instructions.append(instr)

    h = HumidifierDevice("on")
    for room in HumidifierCandiateRoom:
        humidifier_instruction = h.generate_instructions()
        for instr in humidifier_instruction:
            instr["room"] = room
            instructions.append(instr)

    d = DehumidifiersDevice("on")
    for room in DehumidifiersCandiateRoom:
        dehumidifiers_instruction = d.generate_instructions()
        for instr in dehumidifiers_instruction:
            instr["room"] = room
            instructions.append(instr)

    print(len(instructions))

    return instructions

def generate_subclass(base_class,attributes, operations):
    class SubClass(base_class):
        def __init__(self, state: str):
            super().__init__(state)
            # 覆盖 attributes 和 operations
            self.attributes = {attr: self.attributes[attr] for attr in attributes if attr in self.attributes}
            self.operations = {op: self.operations[op] for op in operations if op in self.operations}
    return SubClass

class VisualMasterBedroom:
    def __init__(self) -> None:
        self.name = "master_bedroom"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AirConditionerDeviceList)("on"))
            self.unexist_devices.append(random.choice(HeatingDeviceList)("on"))
            self.unexist_devices.append(random.choice(FanDeviceList)("on"))
        else:
            self.devices.append(random.choice(HeatingDeviceList)("on"))
            self.devices.append(random.choice(FanDeviceList)("on"))
            self.unexist_devices.append(random.choice(AirConditionerDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(CurtainDeviceList)("on"))
        else:
            self.unexist_devices.append(random.choice(CurtainDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AirPurifiersDeviceList)("on"))
        else:
            self.unexist_devices.append(random.choice(AirPurifiersDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AromatherapyDeviceList)("on"))
        else:
            self.unexist_devices.append(random.choice(AromatherapyDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(TrashDeviceList)("on"))
        else:
            self.unexist_devices.append(random.choice(TrashDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(MediaPlayerDeviceList)("play"))
        else:
            self.unexist_devices.append(random.choice(MediaPlayerDeviceList)("play"))

        if random.random() > 0.5:
            self.devices.append(BedDevice())
        else:
            self.unexist_devices.append(BedDevice())
        
        if random.random() > 0.5:
            self.devices.append(random.choice(PetFeederDeviceList)("on"))
        else:
            self.unexist_devices.append(random.choice(PetFeederDeviceList)("on"))


        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    
class VisualGuestBedroom:
    def __init__(self) -> None:
        self.name = "guest_bedroom"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AirConditionerDeviceList)("on"))
            self.unexist_devices.append(random.choice(HeatingDeviceList)("on"))
            self.unexist_devices.append(random.choice(FanDeviceList)("on"))
        else:
            self.devices.append(random.choice(HeatingDeviceList)("on"))
            self.devices.append(random.choice(FanDeviceList)("on"))
            self.unexist_devices.append(random.choice(AirConditionerDeviceList)("on"))

        random.choice([self.devices,self.unexist_devices]).append(random.choice(CurtainDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))

        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))

        random.choice([self.devices,self.unexist_devices]).append(random.choice(AromatherapyDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))

        random.choice([self.devices,self.unexist_devices]).append(random.choice(PetFeederDeviceList)("on")) 
        random.choice([self.devices,self.unexist_devices]).append(BedDevice())

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualLivingRoom:
    def __init__(self) -> None:
        self.name = "living_room"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AirConditionerDeviceList)("on"))
            self.unexist_devices.append(random.choice(HeatingDeviceList)("on"))
            self.unexist_devices.append(random.choice(FanDeviceList)("on"))
        else:
            self.devices.append(random.choice(HeatingDeviceList)("on"))
            self.devices.append(random.choice(FanDeviceList)("on"))
            self.unexist_devices.append(random.choice(AirConditionerDeviceList)("on"))
        
        random.choice([self.devices,self.unexist_devices]).append(random.choice(CurtainDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))

        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))

        random.choice([self.devices,self.unexist_devices]).append(random.choice(AromatherapyDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(MediaPlayerDeviceList)("play"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(PetFeederDeviceList)("on"))

        self.devices.append(PetFeederDevice("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualDingRoom:
    def __init__(self) -> None:
        self.name = "ding_room"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))

        random.choice([self.devices,self.unexist_devices]).append(random.choice(FanDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(BlindsDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))

        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))
        
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualStudyRoom:
    def __init__(self) -> None:
        self.name = "study_room"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(AirConditionerDeviceList)("on"))
            self.unexist_devices.append(random.choice(HeatingDeviceList)("on"))
            self.unexist_devices.append(random.choice(FanDeviceList)("on"))
        else:
            self.devices.append(random.choice(HeatingDeviceList)("on"))
            self.devices.append(random.choice(FanDeviceList)("on"))
            self.unexist_devices.append(random.choice(AirConditionerDeviceList)("on"))
        
        random.choice([self.devices,self.unexist_devices]).append(random.choice(CurtainDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))

        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))
        
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(PetFeederDeviceList)("play"))
        random.choice([self.devices,self.unexist_devices]).append(BedDevice())

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    
class VisualKitchen:
    def __init__(self) -> None:
        self.name = "kitchen"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(FanDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(BlindsDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(WaterHeaterDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    
class VisualBathroom:
    def __init__(self) -> None:
        self.name = "bathroom"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(BlindsDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(HeatingDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualFoyer:
    def __init__(self) -> None:
        self.name = "foyer"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AromatherapyDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    

class VisualCorridor:
    def __init__(self) -> None:
        self.name = "corridor"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AromatherapyDeviceList)("on"))
        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualBalcony:
    def __init__(self) -> None:
        self.name = "balcony"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(CurtainDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AromatherapyDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(MediaPlayerDeviceList)("play"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(PetFeederDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    
class VisualGarage:
    def __init__(self) -> None:
        self.name = "garage"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        self.devices.append(random.choice(GarageDoorDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(TrashDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(BlindsDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(MediaPlayerDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(PetFeederDeviceList)("on"))

        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state

class VisualStoreRoom:
    def __init__(self) -> None:
        self.name = "store_room"
        self.devices = []
        self.unexist_devices = []
        self.devices.append(random.choice(LightDeviceList)("on"))
        random.choice([self.devices,self.unexist_devices]).append(random.choice(AirPurifiersDeviceList)("on"))
        if random.random() > 0.5:
            self.devices.append(random.choice(HumidifierDeviceList)("on"))
            self.unexist_devices.append(random.choice(DehumidifiersDeviceList)("on"))
        else:
            self.devices.append(random.choice(DehumidifiersDeviceList)("on"))
            self.unexist_devices.append(random.choice(HumidifierDeviceList)("on"))
        self.random_initialize()
        self.state = self.get_status()
        self.devices_name_list = [device.name for device in self.devices]


    def random_initialize(self):
        for device in self.devices:
            device.random_initialize()

    def get_status(self):
        state = {"room_name": self.name}
        for device in self.devices:
            state[device.name] = device.get_status()
        return state    
    
    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] == self.name:
                if instr["device"] in self.devices_name_list:
                    device = self.devices[self.devices_name_list.index(instr["device"])]
                    if instr["instruction"] in device.operations.keys():
                        device.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, room_state,methods):
        self.devices = []
        self.devices_name_list = []
        for device in room_state.keys():
            if device == "room_name":
                continue
            else:
                attributes = room_state[device]["attributes"].keys()
                new_device = generate_subclass(device_map[device],attributes,methods[device])
                self.devices.append(new_device(room_state[device]["state"]))
                self.devices_name_list.append(device)
                self.devices[-1].initialize(room_state[device]["state"],room_state[device]["attributes"])
        
        self.state = self.get_status()

        return self.state
    
class VisualHome:
    def __init__(self) -> None:
        self.rooms = []
        self.rooms.append(VisualMasterBedroom())
        self.rooms.append(VisualGuestBedroom())
        self.rooms.append(VisualLivingRoom())
        self.rooms.append(VisualDingRoom())
        self.rooms.append(VisualStudyRoom())
        self.rooms.append(VisualKitchen())
        self.rooms.append(VisualBathroom())
        self.rooms.append(VisualFoyer())
        self.rooms.append(VisualCorridor())
        self.rooms.append(VisualBalcony())
        self.rooms.append(VisualGarage())
        self.rooms.append(VisualStoreRoom())
        if random.random() > 0.5:
            self.VacuumRobot = VacuumRobotrDevice("on")
        self.state = self.get_status()
        self.rooms_name_list = [room.name for room in self.rooms]

    def get_status(self):
        state = {}
        for room in self.rooms:
            state[room.name] = room.get_status()

        if hasattr(self, "VacuumRobot"):
            state["VacuumRobot"] = self.VacuumRobot.get_status()
        return state

    def execute_instructions(self, instructions):
        for instr in instructions:
            if instr["room"] in self.rooms_name_list:
                room = self.rooms[self.rooms_name_list.index(instr["room"])]
                room.execute_instructions([instr])
            elif instr["room"] == "VacuumRobot":
                if hasattr(self, "VacuumRobot"):
                    if instr["instruction"] in self.VacuumRobot.operations.keys():
                        self.VacuumRobot.operations[instr["instruction"]]()

        state = self.get_status()

        return state
    
    def initalzie(self, home_state):
        methods = {}
        methods_list = home_state["method"]
        home_status = home_state["home_status"]
        for method in methods_list:
            if method["room_name"] in methods.keys():
                if method["device_name"] in methods[method["room_name"]].keys():
                    methods[method["room_name"]][method["device_name"]].append(method["operation"])
                else:
                    methods[method["room_name"]][method["device_name"]] = [method["operation"]]
            else:
                methods[method["room_name"]] = {method["device_name"]: [method["operation"]]}
        for room in self.rooms:
            room_state = home_status[room.name]
            room.initalzie(room_state,methods[room.name])
        if "vacuum_robot" in home_status.keys():
            self.VacuumRobot.initialize(home_status["vacuum_robot"]["state"],home_status["vacuum_robot"]["attributes"])

        self.state = self.get_status()

        return self.state
         
        
def generate_visual_home():
    normal_instructions = []
    unexist_attribute_instructions = []
    unexist_device_instructions = []
    visual_home = VisualHome()
    state = visual_home.get_status()
    method = []
    for room in visual_home.rooms:
        for device in room.devices:
            for operation in device.operations.values():
                sig = inspect.signature(operation)
                parameters = []
                for name, parameter in sig.parameters.items():
                    annotation = parameter.annotation
                    param_type = annotation.__name__ if isinstance(annotation, type) else str(annotation)
                    parameters.append({"name": name, "type": param_type})
                method.append({"room": room.name, "device": device.name, "operation": operation.__name__, "parameters": parameters})

            normal_instruction = device.generate_instructions()
            for instr in normal_instruction:
                instr["room"] = room.name
                instr["type"] = "normal"          
                normal_instructions.append(instr)
            if hasattr(device, "generate_unexist_instructions"):               
                unexist_attribute_instruction = device.generate_unexist_instructions()
                for instr in unexist_attribute_instruction:
                    instr["room"] = room.name
                    instr["type"] = "unexist_attribute"
                    unexist_attribute_instructions.append(instr)
        for device in room.unexist_devices:
            unexist_device_instruction = device.generate_instructions()
            for instr in unexist_device_instruction:
                instr["room"] = room.name
                instr["type"] = "unexist_device"
                unexist_device_instructions.append(instr)
    if hasattr(visual_home, "VacuumRobot"):
        print("1")
        for operation in visual_home.VacuumRobot.operations.values():
            sig = inspect.signature(operation)
            parameters = []
            for name, parameter in sig.parameters.items():
                annotation = parameter.annotation
                param_type = annotation.__name__ if isinstance(annotation, type) else str(annotation)
                parameters.append({"name": name, "type": param_type})            
                method.append({"room": "None", "device": "vacuum_robot", "operation": operation.__name__, "parameters": parameters})
        for instr in visual_home.VacuumRobot.generate_instructions():
            instr["room"] = "None"
            instr["type"] = "normal"
            normal_instructions.append(instr)

    all_instructions = normal_instructions + unexist_attribute_instructions + unexist_device_instructions
    sample_10 = [random.sample(all_instructions, 10) for _ in range(50)]
    sample_9 = [random.sample(all_instructions, 9) for _ in range(50)]
    sample_8 = [random.sample(all_instructions, 8) for _ in range(50)]
    sample_7 = [random.sample(all_instructions, 7) for _ in range(50)]
    sample_6 = [random.sample(all_instructions, 6) for _ in range(50)]
    sample_5 = [random.sample(all_instructions, 5) for _ in range(50)]
    sample_4 = [random.sample(all_instructions, 4) for _ in range(50)]
    sample_3 = [random.sample(all_instructions, 3) for _ in range(50)]
    sample_2 = [random.sample(all_instructions, 2) for _ in range(50)]
    sample = sample_2 + sample_3 + sample_4 + sample_5 + sample_6 + sample_7 + sample_8 + sample_9 + sample_10

    return all_instructions, state, method, sample

def check_instruction(instruction):
    room_device = []
    for instr in instruction:
        if (instr["room"], instr["device"]) in room_device:
            return False
        else:
            room_device.append((instr["room"], instr["device"]))

    return True

def check_instruction2(instruction):
    room_device = []
    type_set = set()
    for instr in instruction:
        if (instr["room"], instr["device"]) in room_device and instr["type"] is "normal":
            return False
        elif instr["type"] is "normal":
            room_device.append((instr["room"], instr["device"]))

        type_set.add(instr["type"])

    if len(type_set) < 2:
        return False

    return True

def generate_visual_home_ood():
    normal_bed_instructions = []
    normal_petfeeder_instructions = []
    unexist_attribute_instructions = []
    unexist_device_instructions = []
    visual_home = VisualHome()
    state = visual_home.get_status()
    method = []
    for room in visual_home.rooms:
        for device in room.devices:
            if device.name == "bed":
                normal_instruction = device.generate_instructions()
                for instr in normal_instruction:
                    instr["room"] = room.name
                    instr["type"] = "normal"          
                    normal_bed_instructions.append(instr)
            if device.name == "pet_feeder":
                normal_instruction = device.generate_instructions()
                for instr in normal_instruction:
                    instr["room"] = room.name
                    instr["type"] = "normal"          
                    normal_petfeeder_instructions.append(instr)
                if hasattr(device, "generate_unexist_instructions"):  
                    unexist_attribute_instruction = device.generate_unexist_instructions()
                    for instr in unexist_attribute_instruction:
                        instr["room"] = room.name
                        instr["type"] = "unexist_attribute"
                        unexist_attribute_instructions.append(instr)
        for device in room.unexist_devices:
            if device.name == "bed" or device.name == "pet_feeder":
                unexist_device_instruction = device.generate_instructions()
                for instr in unexist_device_instruction:
                    instr["room"] = room.name
                    instr["type"] = "unexist_device"
                    unexist_device_instructions.append(instr)

    tmp = [random.sample(normal_bed_instructions+normal_petfeeder_instructions, 2) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions, 3) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions, 4) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions, 5) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions, 6) for _ in range(10)] 
    mn = []
    for i in tmp:
        if check_instruction(i):
            mn.append(i)
    tmp = [random.sample(unexist_attribute_instructions+unexist_device_instructions, 2) for _ in range(10)] + \
            [random.sample(unexist_attribute_instructions+unexist_device_instructions, 3) for _ in range(10)] + \
            [random.sample(unexist_attribute_instructions+unexist_device_instructions, 4) for _ in range(10)] + \
            [random.sample(unexist_attribute_instructions+unexist_device_instructions, 5) for _ in range(10)]
    me = tmp
    mix = [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 2) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 3) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 4) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 5) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 6) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 7) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 8) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 9) for _ in range(10)] + \
            [random.sample(normal_bed_instructions+normal_petfeeder_instructions+unexist_attribute_instructions+unexist_device_instructions, 10) for _ in range(10)]
    
    mix = [i for i in mix if check_instruction2(i)]

    return normal_bed_instructions+normal_petfeeder_instructions, unexist_attribute_instructions+unexist_device_instructions, state, method, mn, me, mix



    
    


                

            