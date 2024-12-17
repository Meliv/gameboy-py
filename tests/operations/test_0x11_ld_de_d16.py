from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import ld_de_d16

import unittest

class LD_DE_D16_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_de_d16(self, d8_1, d8_2):

        memory = [0x00, d8_1, d8_2]
        cpu = CPU(memory)
        
        cycles = ld_de_d16(cpu, cpu.M)

        self.assertEqual(cycles, 12)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, d8_2)
        self.assertEqual(cpu.E, d8_1)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, (d8_2 << 8) | d8_1)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 3)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, memory)        