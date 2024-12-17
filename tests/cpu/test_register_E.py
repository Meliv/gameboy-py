from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU

import unittest

class Register_E_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_register_E(self, e):
        cpu = CPU(memory=[])

        cpu.E = e

        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, e)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, e)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0xff00, max_value=0xffff)
    )
    def test_register_E_overflow(self, e):
        cpu = CPU(memory=[])

        cpu.E = e
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 255 & e)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 255 & e)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        