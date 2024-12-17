from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import inc_bc

import unittest

class INC_BC_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_inc_bc(self, b, c):

        cpu = CPU([])
        cpu.B = b
        cpu.C = c
        
        r = ((b << 8) | c) + 1 & 0xffff
        
        cycles = inc_bc(cpu)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, ((255 << 8) & r) >> 8)
        self.assertEqual(cpu.C, 255 & r)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, r)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])        