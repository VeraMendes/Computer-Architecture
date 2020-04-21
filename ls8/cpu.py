"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.register = [0] * 8
        self.ram = [0] * 256
        self.running = True
        # self.instructions = {}
        self.LDI = 0b10000010
        self.HLT = 0b00000001
        self.PRN = 0b01000111


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  # NOP: Do nothing for this instruction.
            0b00001000,  # this is the number 8
            0b01000111,  # PRN R0
            0b00000000,  # NOP: Do nothing for this instruction.
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        print(self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "FL_DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, address):
        """Return an address in RAM."""

        return self.ram[address]

    def ram_write(self, value, address):
        """Set an address in RAM to a certain value."""

        self.ram[address] = value
    
    def halt(self):
        self.running = False

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

    # # instructions
    # LDI = 0b10000010
    # HLT = 0b00000001
    # PRN = 0b01000111

    def run(self):
        """Run the CPU."""
        self.running = True

        self.load()
        while self.running is True:

            IR = self.ram_read(self.pc)

            if IR == self.LDI:    # LDI
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.ram_write(operand_b, operand_a)
                self.pc += 3
            elif IR == self.PRN:  # PRN
                operand_a = self.ram_read(self.pc + 1)
                self.ram_write(operand_b, operand_a)
                print(f'printing... {self.ram[operand_a]}')           
                self.pc += 2
            elif IR == self.HLT:  # HALT
                self.running = False
            else:    
                print("Unknown instruction")
                self.running = False

