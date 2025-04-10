#!/usr/bin/env python
from . import serial
from machine import Pin


class ModbusRelay(object):
    def __init__(self) -> None:
        self.RelayRegisterMapping = {}

    def add_relay_register(self, reg_adr:int, mapping):
        self.RelayRegisterMapping[f"{mapping.reg_type}-{reg_adr}"] = mapping
    
    def get_relay_register(self, reg_adr:int, reg_type:str):
        key = f"{reg_type}-{reg_adr}"
        if key in self.RelayRegisterMapping:
            return self.RelayRegisterMapping[key]
        else:
            return None


class RelayRegisterMapping():
    def __init__(self, 
                 dev_adr: int, 
                 reg_type: str, 
                 target_register: int,
                 pins, baud, 
                 signed: bool):
        self.pins = pins
        self.baud = baud
        self.dev_adr = dev_adr
        self.reg_type = reg_type
        self.target_register = target_register
        self.signed = signed

    def request_data(self):
        print("Relaying Modbus Request", self.pins, self.baud, self.dev_adr, self.target_register)
        host = serial.Serial(baudrate=self.baud, pins=(Pin(4), Pin(5)), uart_id=1)
        val = None
        if self.reg_type == 'COILS':
            val = host.read_coils(self.dev_adr, self.target_register, 1)
        elif self.reg_type == 'HREGS':
            val = host.read_holding_registers(self.dev_adr, self.target_register, 1, self.signed)
        elif self.reg_type == 'ISTS':
            val = host.read_discrete_inputs(self.dev_adr, self.target_register, 1)
        elif self.reg_type == 'IREGS':
            val = host.read_input_registers(self.dev_adr, self.target_register, 1, self.signed)
        return val
    
    def write_data(self, value):
        print("Relaying Modbus Request", self.pins, self.baud, self.dev_adr, self.target_register)
        host = serial.Serial(baudrate=self.baud, pins=(Pin(4), Pin(5)), uart_id=1)
        val = False
        if self.reg_type == 'COILS':
            val = host.write_single_coil(self.dev_adr, self.target_register, value)
        elif self.reg_type == 'HREGS':
            val = host.write_single_register(self.dev_adr, self.target_register, value, self.signed)
        return val
