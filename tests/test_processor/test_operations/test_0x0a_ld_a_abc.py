from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import ld_a_abc

import unittest

class LD_A_ABC_Test(unittest.TestCase):
    @given(
        integers(min_value=0x0000, max_value=0xffff),
        integers(min_value=0x01, max_value=0xff)
    )
    def test_ld_a_abc(self, bc, a):

        cpu = CPU()
        cpu.M[bc] = a
        cpu.BC = bc
        
        cycles = ld_a_abc(cpu, cpu.M)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, a)
        
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, bc >> 8)
        self.assertEqual(cpu.C, bc & 255)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual([m for m in cpu.M if m != 0x0], [a])
        
    @given(integers(min_value=0x0000, max_value=0xffff))
    def test_ld_a_abc_a_is_zero(self, bc):
        
        cpu = CPU()
        cpu.M[bc] = 0
        cpu.BC = bc
        
        cycles = ld_a_abc(cpu, cpu.M)

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
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual([m for m in cpu.M if m != 0x0], [])