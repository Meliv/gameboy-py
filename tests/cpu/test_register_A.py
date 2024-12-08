from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import nop
import unittest

class Register_A_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_register_A(self, a):
        cpu = CPU(memory=[])

        cpu.A = a

        self.assertEqual(cpu.A, a)
        self.assertEqual(cpu.F, 0)
        
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
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0xff00, max_value=0xffff)
    )
    def test_register_A_overflow(self, a):
        cpu = CPU(memory=[])

        cpu.A = a
        
        self.assertEqual(cpu.A, 255 & a)
        self.assertEqual(cpu.F, 0)
        
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
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        