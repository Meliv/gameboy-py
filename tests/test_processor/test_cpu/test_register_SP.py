from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU

import unittest

class Register_SP_Test(unittest.TestCase):
    @given(
        integers(min_value=0x0000, max_value=0xffff)
    )
    def test_register_SP(self, sp):
        cpu = CPU(memory=[])

        cpu.SP = sp

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
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, sp)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0x0000, max_value=0xffffffff)
    )
    def test_register_SP_overflow(self, sp):
        cpu = CPU(memory=[])

        cpu.SP = sp
        
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
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, sp & 0xffff)
        
        self.assertEqual(cpu.M, [])
        