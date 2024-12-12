from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import ld_a16_sp
import unittest

class LD_A16_SP_Test(unittest.TestCase):
    @given(
        integers(min_value=0x03, max_value=0xff),
        integers(min_value=0x00, max_value=0xff),
        integers(min_value=0x03, max_value=0xff),
        integers(min_value=0x00, max_value=0xff)
    )
    def test_ld_a16_sp(self, sp_l, sp_h, mem_l, mem_h):

        cpu = CPU()
        cpu.M[0x01] = mem_l
        cpu.M[0x02] = mem_h

        cpu.SP = (sp_h << 8) | sp_l       
        
        cycles = ld_a16_sp(cpu, cpu.M)

        self.assertEqual(cycles, 20)
        
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
        
        self.assertEqual(cpu.PC, 3)
        self.assertEqual(cpu.SP, (sp_h << 8) | sp_l)
        
        self.assertEqual(cpu.M[(mem_h << 8) | mem_l], sp_l)        
        self.assertEqual(cpu.M[((mem_h << 8) | mem_l)+1], sp_h)   
        
        populated_m_locations = [
            0x00,
            0x01,
            0x02,
            (mem_h << 8) | mem_l,
            ((mem_h << 8) | mem_l) + 1
        ]
        
        x = [m for i,m in enumerate(cpu.M) if i not in populated_m_locations and m != 0x00]
        self.assertFalse(any(x))
        