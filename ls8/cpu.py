"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = True


    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename, 'r') as f:
            program = f.readlines()
            for instruction in program:
                instruction = instruction.split('#')
                instruction = instruction[0].strip()

                if instruction == '':
                    continue

                self.ram[address] = int(instruction, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "FL_DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

        return self.reg[reg_a]
    
    def ram_read(self, address):
        """Return an address in RAM."""

        return self.ram[address]

    def ram_write(self, value, address):
        """Set an address in RAM to a certain value."""

        self.ram[address] = value

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
        MULT = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        SP = 7
        self.reg[SP] = 0xF4   # 244 decimal

        self.running = True

        while self.running is True:
            
            IR = self.ram_read(self.pc)
            inst_len = ((IR & 0b11000000) >> 6) + 1 # max 3 operands

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == LDI:
                self.reg[operand_a] = operand_b
                # self.pc += 3
            elif IR == MULT:
                self.alu('MULT', operand_a, operand_b)
                # self.pc += 3
            elif IR == PRN:
                print(f'printing... {self.reg[operand_a]}')           
                # self.pc += 2
            elif IR == PUSH:
                self.reg[SP] -= 1  # decrement SP (stack pointer)
                #copy value from register into ram address pointed by SP
                address = self.reg[SP]
                self.ram_write(self.reg[operand_a], address)
                # self.pc += 2
            elif IR == POP:
                address = self.reg[SP]
                # copy value from the SP address into the given register
                self.reg[operand_a] = self.ram_read(address)
                self.reg[SP] += 1  # increment SP (stack pointer)
                # self.pc += 2
            elif IR == HLT:  # HALT
                self.running = False
            else:    
                print("Unknown instruction")
                self.running = False

            self.pc += inst_len
            # self.trace()
            # print('--------')
