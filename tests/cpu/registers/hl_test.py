from hypothesis import given
from hypothesis.strategies import integers

from src.cpu import CPU
import unittest

class HL_Test(unittest.TestCase):
    @given(integers(min_value=256, max_value=65535))
    def test_setter(self, hl):
        cpu = CPU()

        cpu.HL = hl
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, ((255 << 8) & hl) >> 8)
        self.assertEqual(cpu.L, 255 & hl)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, hl)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))
        
        
        
    @given(integers(min_value=0, max_value=255), integers(min_value=0, max_value=255))
    def test_getter(self, h, l):
        cpu = CPU()
        
        cpu.H = h
        cpu.L = l
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, 0)        
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, h)
        self.assertEqual(cpu.L, l)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, (h << 8) | l)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))