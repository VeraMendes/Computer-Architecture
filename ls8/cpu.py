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


    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,  # NOP: Do nothing for this instruction.
        #     0b00001000,  # this is the number 8
        #     0b01000111,  # PRN R0
        #     0b00000000,  # NOP: Do nothing for this instruction.
        #     0b00000001,  # HLT
        # ]

        with open(filename, 'r') as f:
            program = f.readlines()
            for instruction in program:
                instruction = instruction.split('#')
                instruction = instruction[0].strip()

                if instruction == '':
                    continue

                self.ram[address] = int(instruction, 2)
                address += 1
                # print(instruction)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1



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

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        self.running = True

        
        while self.running is True:

            IR = self.ram_read(self.pc)

            if IR == LDI:    # LDI
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.register[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:  # PRN
                print(f'printing... {self.register[operand_a]}')           
                self.pc += 2
            elif IR == HLT:  # HALT
                self.running = False
            else:    
                print("Unknown instruction")
                self.running = False


# register [8] [0] [0] [0] [0] [0] [0] [0]
#          0   0b10000010,  # LDI R0,8                                 pc = 0         OPERATION
#          1   0b00000000,  # NOP: Do nothing for this instruction.    pc+1 = operand_a
#          2   0b00001000,  # this is the number 8                     pc+2 = operand_b
#          3   0b01000111,  # PRN R0                                   pc = 3         OPERATION
#          4   0b00000000,  # NOP: Do nothing for this instruction.           operand_a
#          5   0b00000001,  # HLT                                      PC = 5         OPERATION
#          ends