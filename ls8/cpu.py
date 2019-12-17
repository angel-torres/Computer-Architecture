"""CPU functionality."""

import sys

HLT = 0b00000001 # LDI
LDI = 0b10000010 # PRN
PRN = 0b01000111 # HLT

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.commands = {
            "HLT": 0b00000001, # LDI
            "LDI": 0b10000010, # PRN
            "PRN": 0b01000111 # HLT
        }

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b01000111, # PRN R0
            0b00000000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        with open(filename) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()

                if n[0] == '':
                    continue

                val = int(n[0], 2)
                self.ram[address] = val
                address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            instruction = self.ram[self.pc]

            if instruction == self.commands["LDI"]: # LDI R0,8
                position  = self.ram[self.pc + 1] # get position
                value = self.ram[self.pc + 2] # get value to store
                self.register[position] = value # save value into register
                self.pc += 2 # increase pc position by 2
            
            elif instruction == self.commands["PRN"]: # PRN R0
                position = self.ram[self.pc + 1] # get position of number to pring
                print(self.register[position]) # print value at given position
                self.pc += 1 # increase pc value by 1
            
            elif instruction == self.commands["HLT"]: # HLT
                halted = True # halt while loop
                self.pc += 1 # increase pc by 1
            
            else:
                self.pc += 1 # if no commands match then increase pc by 1


    def ram_read(self, position):
        """Run the CPU."""
        return self.ram[position]

    def ram_write(self, position, value):
        """Run the CPU."""
        self.ram[position] = value