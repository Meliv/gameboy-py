from hypothesis import given
from hypothesis.strategies import integers

from src.cpu import CPU
import unittest

class BC_Test(unittest.TestCase):
    @given(integers(min_value=0x0100, max_value=0xffff))
    def test_setter(self, bc):
        cpu = CPU(memory=[])

        cpu.BC = bc
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, ((255 << 8) & bc) >> 8)
        self.assertEqual(cpu.C, 255 & bc)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))
        
        
        
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff))
    def test_getter(self, b, c):
        cpu = CPU(memory=[])
        
        cpu.B = b
        cpu.C = c
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, b)        
        self.assertEqual(cpu.C, c)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, (b << 8) | c)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))
        