from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import ld_hl_d16

import unittest

class LD_HL_D16_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_hl_d16(self, h, l):

        memory = [0x21, l, h]
        cpu = CPU(memory)
        
        cycles = ld_hl_d16(cpu, cpu.M)

        self.assertEqual(cycles, 12)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, h)
        self.assertEqual(cpu.L, l)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, (h << 8) | l)
        
        self.assertEqual(cpu.PC, 3)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, memory)