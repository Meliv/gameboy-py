from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import nop
import unittest

class Register_PC_Test(unittest.TestCase):
    @given(
        integers(min_value=0x0000, max_value=0xffff)
    )
    def test_register_PC(self, pc):
        cpu = CPU(memory=[])

        cpu.PC = pc

        self.assertEqual(cpu.A, 0)
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
        
        self.assertEqual(cpu.PC, pc)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
    
    @given(
        integers(min_value=0x0000, max_value=0xffffffff)
    )
    def test_register_PC_overflow(self, pc):
        cpu = CPU(memory=[])

        cpu.PC = pc
        
        self.assertEqual(cpu.A, 0)
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
        
        self.assertEqual(cpu.PC, pc & 0xffff)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        