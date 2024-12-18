from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import ld_bc_d16

import unittest

class LD_BC_D16_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_bc_d16(self, d8_h, d8_l):
        
        memory = [0x00, d8_l, d8_h]
        cpu = CPU(memory)

        cycles = ld_bc_d16(cpu, cpu.M)

        self.assertEqual(cycles, 12)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, d8_h)
        self.assertEqual(cpu.C, d8_l)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, (d8_h << 8) | d8_l)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 3)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, memory)        