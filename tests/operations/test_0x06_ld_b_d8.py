from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import ld_b_d8
import unittest

class LD_B_D8_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_b_d8(self, b):

        memory = [0x06, b]
        cpu = CPU(memory)
        
        cycles = ld_b_d8(cpu, memory)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, b)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, (b << 8) | cpu.C)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 2)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, memory)        