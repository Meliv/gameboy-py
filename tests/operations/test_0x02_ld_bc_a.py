from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import ld_bc_a
import unittest

class LD_BC_A_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_bc_a(self, a, b, c):
        
        bc = (b << 8) | c
        
        cpu = CPU()
        cpu.A = a
        cpu.B = b
        cpu.C = c
        
        cycles = ld_bc_a(cpu, cpu.M)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, a)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, b)
        self.assertEqual(cpu.C, c)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M[bc], cpu.A)
        self.assertTrue(not all(m for i,m in enumerate(cpu.M) if i != bc))        