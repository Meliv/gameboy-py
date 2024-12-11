from src.cpu import CPU

from src.operations import rlca
import unittest

class RLCA_Test(unittest.TestCase):
    def test_rlca(self):

        cases = [
            (0, 0, 0),
            (1, 2, 0),
            (7, 14, 0),
            (15, 30, 0),
            (128, 1, 1),
            (170, 85, 1),
            (200, 145, 1),
            (64, 128, 0),
            (42, 84, 0),
        ]

        for a, expected, carry in cases:
            cpu = CPU([])
            
            cpu.A = a
            
            cycles = rlca(cpu)

            self.assertEqual(cycles, 4)
            
            self.assertEqual(cpu.A, expected)
            
            self.assertEqual(cpu.F_Z, 0)
            self.assertEqual(cpu.F_N, 0)
            self.assertEqual(cpu.F_H, 0)
            self.assertEqual(cpu.F_C, carry)
            
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