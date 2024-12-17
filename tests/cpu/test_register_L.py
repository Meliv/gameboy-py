from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU

import unittest

class Register_L_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_register_L(self, l):
        cpu = CPU(memory=[])

        cpu.L = l

        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, l)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, l)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0xff00, max_value=0xffff)
    )
    def test_register_L_overflow(self, l):
        cpu = CPU(memory=[])

        cpu.L = l
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 255 & l)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 255 & l)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        