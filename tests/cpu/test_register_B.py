from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import nop
import unittest

class Register_B_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_register_B(self, b):
        cpu = CPU(memory=[])

        cpu.B = b

        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, b)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, b << 8)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0xff00, max_value=0xffff)
    )
    def test_register_B_overflow(self, b):
        cpu = CPU(memory=[])

        cpu.B = b
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 255 & b)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, b << 8 & 0xffff)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        