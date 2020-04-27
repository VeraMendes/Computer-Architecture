"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = True
        self.instructions = {
            LDI: self.LDI,
            PRN: self.PRN,
            ADD: self.ADD,
            MULT: self.MULT,
            PUSH: self.PUSH,
            POP: self.POP,
            HLT: self.HLT,
            CALL: self.CALL,
            RET: self.RET
        }

    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        # self.pc += 3

    def PRN(self, operand_a, operand_b):
        print(f'printing... {self.reg[operand_a]}')
        # self.pc +=2

    def ADD(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)
        # self.pc +=3

    def MULT(self, operand_a, operand_b):
        self.alu('MULT', operand_a, operand_b)
        # self.pc +=3

    def PUSH(self, operand_a, operand_b):
        # decrement SP (stack pointer)
        self.reg[SP] -= 1
        # copy value from register into ram address pointed by SP
        address = self.reg[SP]
        self.ram_write(self.reg[operand_a], address)
        # self.pc += 2

    def POP(self, operand_a, operand_b):
        address = self.reg[SP]
        # copy value from the SP address into the given register
        self.reg[operand_a] = self.ram_read(address)
        # increment SP (stack pointer)
        self.reg[SP] += 1
        # self.pc += 2

    def CALL(self, operand_a, operand_b):
        # address of the instruction directly after CALL
        self.reg[SP] -= 1
        # push that instruction onto the stack
        self.ram_write(self.pc + 2, self.reg[SP])
        # PC is set to the address stored in the given register
        # We jump to that location in RAM
        self.pc = self.reg[operand_a]

    def RET(self, operand_a, operand_b):
        # Pop the value from the top of the stack and store it in the PC.
        address = self.reg[SP]
        self.pc = self.ram_read(address)
        # increment SP (stack pointer)
        self.reg[SP] += 1

    def HLT(self, operand_a, operand_b):
        self.running = False

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
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> reg_b
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << reg_b
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

        while self.running is True:
            IR = self.ram_read(self.pc)
            # max 3 operands
            inst_len = ((IR & 0b11000000) >> 6) + 1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if int(bin(IR), 2) in self.instructions:
                self.instructions[IR](operand_a, operand_b)
            else:
                print("Invalid instruction")
            # if this instruction does not set the PC
            if ~ IR & 0b00010000:
                self.pc += inst_len

            # self.pc += inst_len
            # self.trace()
