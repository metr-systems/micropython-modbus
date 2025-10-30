#!/usr/bin/env python
from . import serial
from machine import Pin


class ModbusRelay(object):
    BAUD = 19200
    UART = 1
    TXPIN = 8
    RXPIN = 9
    STOPBITS = 1
    DATABITS = 8
    PARITY = None
    CTRLPIN = 0
    CTRLPINRE = 0

    def __init__(self, baud: int, pins, uart: int, stopbits: int, databits: int, parity, ctrl_pins) -> None:
        self.RelayRegisterMapping = {}
        ModbusRelay.BAUD = baud
        ModbusRelay.UART = uart
        ModbusRelay.TXPIN = pins[0]
        ModbusRelay.RXPIN = pins[1]
        ModbusRelay.STOPBITS = stopbits
        ModbusRelay.DATABITS = databits
        ModbusRelay.PARITY = parity
        ModbusRelay.CTRLPIN = ctrl_pins[0]
        ModbusRelay.CTRLPINRE = ctrl_pins[1]

    def add_relay_register(self, reg_adr: int, mapping):
        self.RelayRegisterMapping[f"{mapping.reg_type}-{reg_adr}"] = mapping

    def get_relay_register(self, reg_adr: int, reg_type: str):
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
                 signed: bool):
        self.dev_adr = dev_adr
        self.reg_type = reg_type
        self.target_register = target_register
        self.signed = signed

    def request_data(self):
        host = serial.Serial(
            baudrate=ModbusRelay.BAUD,
            pins=(Pin(ModbusRelay.TXPIN), Pin(ModbusRelay.RXPIN)),
            uart_id=ModbusRelay.UART,
            data_bits=ModbusRelay.DATABITS,
            stop_bits=ModbusRelay.STOPBITS,
            parity=ModbusRelay.PARITY,
            ctrl_pins=(Pin(ModbusRelay.CTRLPIN), Pin(ModbusRelay.CTRLPINRE)))
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
        host = serial.Serial(
            baudrate=ModbusRelay.BAUD,
            pins=(Pin(ModbusRelay.TXPIN), Pin(ModbusRelay.RXPIN)),
            uart_id=ModbusRelay.UART,
            data_bits=ModbusRelay.DATABITS,
            stop_bits=ModbusRelay.STOPBITS,
            parity=ModbusRelay.PARITY,
            ctrl_pins=(Pin(ModbusRelay.CTRLPIN), Pin(ModbusRelay.CTRLPINRE)))
        val = False
        if self.reg_type == 'COILS':
            val = host.write_single_coil(self.dev_adr, self.target_register, value)
        elif self.reg_type == 'HREGS':
            val = host.write_single_register(self.dev_adr, self.target_register, value, self.signed)
        return val
