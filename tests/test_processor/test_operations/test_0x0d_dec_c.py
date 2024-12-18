from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import dec_c

import unittest

class DEC_C_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_dec_c(self, c):

        cpu = CPU([])
        cpu.C = c
        
        cycles = dec_c(cpu)

        self.assertEqual(cycles, 4)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, c-1 & 0xff == 0)
        self.assertEqual(cpu.F_N, 1)
        self.assertEqual(cpu.F_H, (c & 0x0f) - 1 > 0xff)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, c-1 & 0xff)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, cpu.C)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])        