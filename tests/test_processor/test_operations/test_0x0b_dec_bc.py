from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import dec_bc

import unittest

class DEC_BC_Test(unittest.TestCase):
    @given(integers(min_value=0x0000, max_value=0xffff))
    def test_dec_bc(self, bc):

        cpu = CPU([])
        cpu.BC = bc
        
        cycles = dec_bc(cpu)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, 0)
        
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, bc-1 >> 8 & 0xff)
        self.assertEqual(cpu.C, bc-1 & 0xff)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, bc-1 & 0xffff)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])