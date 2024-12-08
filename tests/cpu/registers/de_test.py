from hypothesis import given
from hypothesis.strategies import integers

from src.cpu import CPU
import unittest

class DE_Test(unittest.TestCase):
    @given(integers(min_value=0x0100, max_value=0xffff))
    def test_setter(self, de):
        cpu = CPU(memory=[])

        cpu.DE = de
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, ((255 << 8) & de) >> 8)
        self.assertEqual(cpu.E, 255 & de)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, de)
        self.assertEqual(cpu.HL, 0)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))
        
        
        
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff))
    def test_getter(self, d, e):
        cpu = CPU(memory=[])
        
        cpu.D = d
        cpu.E = e
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
        self.assertEqual(cpu.B, 0)        
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, d)        
        self.assertEqual(cpu.E, e)   
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, (d << 8) | e)
        self.assertEqual(cpu.HL, 0)

        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertTrue(all(i == 0x00 for i in cpu.M))     
        