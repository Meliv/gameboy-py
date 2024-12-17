from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import add_hl_bc

import unittest

class ADD_HL_BC_Test(unittest.TestCase):
    @given(
        integers(min_value=0x0000, max_value=0xffff),
        integers(min_value=0x0000, max_value=0xffff)
    )
    def test_add_hl_bc(self, hl, bc):

        cpu = CPU([])
        cpu.HL = hl
        cpu.BC = bc
        
        cycles = add_hl_bc(cpu)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, bc >> 8)
        self.assertEqual(cpu.C, bc & 255)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, (hl + bc & 0xffff) >> 8)
        self.assertEqual(cpu.L, (hl + bc) & 255)
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, (hl + bc) & 0xffff)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])