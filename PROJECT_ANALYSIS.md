# gameboy-py: Detailed Project Analysis

Analysis date: February 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture and Code Structure](#2-architecture-and-code-structure)
3. [CPU Implementation - What's Done](#3-cpu-implementation---whats-done)
4. [Opcode Coverage - Detailed Breakdown](#4-opcode-coverage---detailed-breakdown)
5. [Test Suite Analysis](#5-test-suite-analysis)
6. [Bugs and Correctness Issues](#6-bugs-and-correctness-issues)
7. [Missing Emulator Subsystems](#7-missing-emulator-subsystems)
8. [Scalability Concerns and Refactoring Opportunities](#8-scalability-concerns-and-refactoring-opportunities)
9. [Suggested Parameterised Test Approach](#9-suggested-parameterised-test-approach)
10. [Recommended Next Steps](#10-recommended-next-steps)

---

## 1. Project Overview

This is an early-stage Game Boy (DMG) emulator written in Python. The Game Boy uses a Sharp LR35902 CPU,
which is often informally called a "Z80-like" processor but is actually its own distinct instruction set -
it shares some opcodes with the Z80 and Intel 8080 but has unique instructions and is missing many Z80
instructions (like the IX/IY register operations).

The project currently consists of:

- **~316 lines** of source code across 5 files
- **~1,637 lines** of test code across 31 test files
- **21 implemented opcodes** out of ~500 usable ones (the full 512 includes some illegal/unused slots)
- **No subsystems beyond the CPU** - no graphics, audio, memory mapping, interrupts, input, or cartridge support

The test-to-source ratio of roughly 5:1 reflects the thorough property-based testing approach using
Hypothesis. This is commendable but, as discussed later, may not scale well to 500+ opcodes without
a change in strategy.

### File Tree

```
gameboy-py/
+-- src/
|   +-- __main__.py                  # Entry point - loads bootrom, runs CPU loop
|   +-- processor/
|       +-- __init__.py              # Re-exports op_codes.process
|       +-- cpu.py                   # CPU class: registers, flags, memory, execution loop
|       +-- operations.py            # Individual opcode function implementations
|       +-- op_codes.py             # Opcode number -> function dispatch table
+-- tests/
|   +-- __init__.py
|   +-- test_processor/
|       +-- __init__.py
|       +-- test_cpu/                # 10 files: one per register/register-pair
|       |   +-- test_register_A.py
|       |   +-- test_register_B.py
|       |   +-- test_register_C.py
|       |   +-- test_register_D.py
|       |   +-- test_register_E.py
|       |   +-- test_register_F.py
|       |   +-- test_register_H.py
|       |   +-- test_register_L.py
|       |   +-- test_register_PC.py
|       |   +-- test_register_SP.py
|       +-- test_operations/         # 21 files: one per implemented opcode
|           +-- test_0x00_nop.py
|           +-- test_0x01_ld_bc_d16.py
|           +-- test_0x02_ld_bc_a.py
|           +-- test_0x03_inc_bc.py
|           +-- test_0x04_inc_b.py
|           +-- test_0x05_dec_b.py
|           +-- test_0x06_ld_b_d8.py
|           +-- test_0x07_rlca.py
|           +-- test_0x08_ld_a16_sp.py
|           +-- test_0x09_add_hl_bc.py
|           +-- test_0x0a_ld_a_abc.py
|           +-- test_0x0b_dec_bc.py
|           +-- test_0x0c_inc_c.py
|           +-- test_0x0d_dec_c.py
|           +-- test_0x10_stop.py
|           +-- test_0x11_ld_de_d16.py
|           +-- test_0x20_jr_nz_r8.py
|           +-- test_0x21_ld_hl_d16.py
|           +-- test_0x30_jr_nc_r8.py
|           +-- test_0x31_ld_sp_d16.py
|           +-- test_0xaf_xor_a.py
+-- README.md
+-- requirements.txt                 # hypothesis, pygame, pytest
+-- setup.py
+-- .coveragerc
```

### Dependencies

- `hypothesis` (6.122.1) - property-based testing framework
- `pygame` (2.6.1) - presumably for future display/input handling (not yet used)
- `pytest` - test runner
- Standard library only for the emulator core

---

## 2. Architecture and Code Structure

### cpu.py - The CPU Class (129 lines)

This is the central class. It models the Sharp LR35902's register file using Python properties
with automatic bit-width clamping.

**Registers modelled:**

| Register | Width | Getter | Setter | Clamping |
|----------|-------|--------|--------|----------|
| A | 8-bit | `self._a` | `value & 0xff` | Yes |
| B | 8-bit | `self._b` | `value & 0xff` | Yes |
| C | 8-bit | `self._c` | `value & 0xff` | Yes |
| D | 8-bit | `self._d` | `value & 0xff` | Yes |
| E | 8-bit | `self._e` | `value & 0xff` | Yes |
| H | 8-bit | `self._h` | `value & 0xff` | Yes |
| L | 8-bit | `self._l` | `value & 0xff` | Yes |
| BC | 16-bit pair | `(B << 8) \| C` | Splits into B and C | Yes |
| DE | 16-bit pair | `(D << 8) \| E` | Splits into D and E | Yes |
| HL | 16-bit pair | `(H << 8) \| L` | Splits into H and L | Yes |
| PC | 16-bit | `self._pc` | `value & 0xffff` | Yes |
| SP | 16-bit | `self._sp` | `value & 0xffff` | Yes |

**Flag register (F):**

The lower 4 bits of the F register are always 0 on real hardware. The upper 4 bits are individual flags:

| Flag | Bit | Getter | Setter |
|------|-----|--------|--------|
| Z (Zero) | 7 | `((1 << 7) & self._f) >> 7` | `(1 & value) << 7 \| self._f` |
| N (Subtract) | 6 | `((1 << 6) & self._f) >> 6` | `(1 & value) << 6 \| self._f` |
| H (Half-carry) | 5 | `((1 << 5) & self._f) >> 5` | `(1 & value) << 5 \| self._f` |
| C (Carry) | 4 | `((1 << 4) & self._f) >> 4` | `(1 & value) << 4 \| self._f` |

**Note:** The F register is stored as `self._f` but there's no `F` property to read/write it as a
whole byte. The real Game Boy exposes AF as a 16-bit pair (used with PUSH AF / POP AF). This will
need to be added.

**Memory:** Stored as a flat Python list of `0x10001` (65537) elements, initialised to `0x0`. The
extra byte beyond 0x10000 is presumably to avoid off-by-one issues but this is unconventional. Real
Game Boy address space is exactly 0x0000-0xFFFF (65536 bytes).

**Execution loop** (`start` method): Runs a simple cycle-counted loop targeting 69,905 cycles per
frame (4,194,304 Hz / 60 fps). Currently runs one frame and stops. There's a comment placeholder
for graphics updates but no implementation. The loop also has no mechanism to break out or handle
HALT/STOP states.

### operations.py - Opcode Implementations (158 lines)

Each opcode is implemented as a standalone function that:
1. Takes a `CPU` instance (and optionally a memory reference)
2. Performs the operation (modify registers, read/write memory)
3. Advances the Program Counter by the instruction's byte length
4. Returns the cycle count for that instruction

This is a clean design. The functions are small and testable in isolation. However, many operations
that differ only by which register they target (e.g., INC B vs INC C vs INC D) are written as
completely separate functions with duplicated logic. This will become a maintenance burden at scale.

### op_codes.py - Dispatch Table (32 lines)

Maps opcode byte values to lambda wrappers around the operation functions. The dispatch dictionary
is **recreated on every call** to `process()` - it's defined inside the function body, not at module
level. This means every single instruction executed allocates a new dictionary with all entries. For
an emulator running millions of instructions per second, this is a significant performance overhead.

The lambda wrappers also serve the purpose of injecting `cpu.M` (memory) into operations that need
it, since some operations access memory and some don't.

### __main__.py - Entry Point (12 lines)

Loads a boot ROM from `etc/roms/bootrom.bin` (this directory doesn't exist in the repo) into memory
starting at address 0, prints each byte, then calls `cpu.start()`. This is minimal scaffolding - it
would fail immediately since the boot ROM would encounter unimplemented opcodes.

---

## 3. CPU Implementation - What's Done

### Register System

The register property system is the most complete part of the project and is well-designed. The key
design decisions:

**8-bit register clamping:** Every 8-bit register setter masks with `0xff`, so writing `cpu.B = 256`
results in `cpu.B == 0`. This correctly models 8-bit overflow/wraparound.

**16-bit register pairs:** BC, DE, and HL are computed properties that compose/decompose from their
constituent 8-bit registers. Writing `cpu.BC = 0x1234` sets B=0x12 and C=0x34. Reading `cpu.BC`
when B=0x12 and C=0x34 returns 0x1234. The splitting logic uses `((255 << 8) & value) >> 8` for the
high byte and `255 & value` for the low byte, which is correct.

**16-bit registers:** PC and SP have their own backing stores clamped to `0xffff`.

### What's Missing From the Register System

- **AF register pair:** The Game Boy allows pushing/popping AF as a 16-bit pair. There's no AF
  property. The F register itself has no whole-byte getter/setter, only individual flag bit access.
  When you implement PUSH AF / POP AF, you'll need `cpu.AF` that composes `(A << 8) | F` and
  ensures the lower 4 bits of F are always 0.

- **Interrupt Master Enable (IME):** A boolean flag that controls whether interrupts are serviced.
  Toggled by EI, DI, and RETI instructions. Not part of the register file per se, but essential
  CPU state.

- **HALT state:** A boolean indicating the CPU is halted (waiting for an interrupt). The HALT
  instruction sets this, and an interrupt clears it.

### Execution Loop

The `start()` method runs a single frame's worth of cycles (69,905) and stops. On real hardware
this would run indefinitely, rendering a frame every 69,905 cycles. The current implementation:

```python
MAX_CYCLES, cycles = 69905, 0
while cycles < MAX_CYCLES:
    c = self.execute_next_instruction()
    cycles += c
```

This is fine as a starting skeleton but needs:

- An outer loop for continuous execution
- Integration with a display refresh cycle
- Interrupt checking between instructions
- HALT/STOP state handling (skip execution, still count cycles)
- Timer increment logic
- Input polling

---

## 4. Opcode Coverage - Detailed Breakdown

### Implemented Opcodes (21 of ~500)

The Game Boy CPU has 256 base opcodes (0x00-0xFF) and 256 CB-prefixed opcodes (accessed via the 0xCB
prefix byte). Of the 256 base opcodes, about 11 are illegal/unused. Of the 256 CB-prefixed opcodes,
all are valid.

Below is every implemented opcode with its actual behaviour in your code:

| Opcode | Mnemonic | Bytes | Cycles | What It Does | Status |
|--------|----------|-------|--------|--------------|--------|
| 0x00 | NOP | 1 | 4 | Advances PC by 1, does nothing else | Correct |
| 0x01 | LD BC, d16 | 3 | 12 | Loads 16-bit immediate into BC (little-endian) | Correct |
| 0x02 | LD (BC), A | 1 | 8 | Writes A to memory address pointed to by BC | Correct |
| 0x03 | INC BC | 1 | 8 | Increments BC by 1 (no flags affected) | Correct |
| 0x04 | INC B | 1 | 4 | Increments B, sets Z/N/H flags | Buggy (see section 6) |
| 0x05 | DEC B | 1 | 4 | Decrements B, sets Z/N/H flags | Buggy (see section 6) |
| 0x06 | LD B, d8 | 2 | 8 | Loads 8-bit immediate into B | Correct |
| 0x07 | RLCA | 1 | 4 | Rotates A left, old bit 7 to carry and bit 0 | Buggy (see section 6) |
| 0x08 | LD (a16), SP | 3 | 20 | Stores SP at 16-bit address (little-endian) | Broken dispatch (see section 6) |
| 0x09 | ADD HL, BC | 1 | 8 | Adds BC to HL, sets N/H/C flags | Buggy (see section 6) |
| 0x0A | LD A, (BC) | 1 | 8 | Loads byte at address BC into A | Correct |
| 0x0B | DEC BC | 1 | 8 | Decrements BC by 1 (no flags affected) | Correct |
| 0x0C | INC C | 1 | 4 | Increments C, sets Z/N/H flags | Buggy (same as INC B) |
| 0x0D | DEC C | 1 | 4 | Decrements C, sets Z/N/H flags | Buggy (same as DEC B) |
| 0x10 | STOP | 2 | 4 | Stub - just advances PC by 2 | Incomplete |
| 0x11 | LD DE, d16 | 3 | 12 | Loads 16-bit immediate into DE (little-endian) | Correct |
| 0x20 | JR NZ, r8 | 2 | 12/8 | Jumps relative if Z flag is 0 | Buggy (see section 6) |
| 0x21 | LD HL, d16 | 3 | 12 | Loads 16-bit immediate into HL (little-endian) | Correct |
| 0x30 | JR NC, r8 | 2 | 12/8 | Jumps relative if C flag is 0 | Buggy (see section 6) |
| 0x31 | LD SP, d16 | 3 | 12 | Loads 16-bit immediate into SP | Correct |
| 0xAF | XOR A | 1 | 4 | XORs A with itself (always produces 0) | Buggy (see section 6) |

**Summary: 9 correct, 10 buggy, 1 broken dispatch, 1 incomplete stub.**

### What's Missing - Base Opcodes (0x00-0xFF)

Here is a breakdown of the remaining ~235 base opcodes organised by category. This gives you a sense
of the patterns and how many opcodes fall into each family:

#### 8-bit Load Instructions (~70 opcodes)

The 0x40-0x7F range is almost entirely `LD r, r'` instructions - load from one register to another.
That's 49 opcodes (7x7 register combinations, plus 7 loads from (HL) and 7 loads to (HL), minus
LD (HL),(HL) which is HALT). These are the simplest instructions to implement and highly repetitive.

Additionally there are:
- `LD r, d8` for each register (0x06, 0x0E, 0x16, 0x1E, 0x26, 0x2E, 0x36, 0x3E) - only 0x06 done
- `LD A, (DE)`, `LD A, (HL+)`, `LD A, (HL-)`, `LD (DE), A`, `LD (HL+), A`, `LD (HL-), A`
- `LD A, (a16)`, `LD (a16), A`
- `LDH A, (a8)`, `LDH (a8), A`, `LDH A, (C)`, `LDH (C), A` (high-page I/O instructions)

#### 16-bit Load Instructions (~10 opcodes)

- `LD rr, d16` for BC/DE/HL/SP - 3 of 4 done (missing LD HL which is actually 0x21, done, but
  the pattern is `LD rr, d16` at 0x01/0x11/0x21/0x31 - all 4 are done)
- `PUSH rr` / `POP rr` for BC/DE/HL/AF (8 opcodes) - none done
- `LD SP, HL`
- `LD HL, SP+r8`

#### 8-bit Arithmetic/Logic (~72 opcodes)

The 0x80-0xBF range is ALU operations with register operands:
- `ADD A, r` (8 opcodes: B, C, D, E, H, L, (HL), A)
- `ADC A, r` (8 opcodes - add with carry)
- `SUB r` (8 opcodes)
- `SBC A, r` (8 opcodes - subtract with carry)
- `AND r` (8 opcodes)
- `XOR r` (8 opcodes) - only XOR A (0xAF) done, and it's buggy
- `OR r` (8 opcodes)
- `CP r` (8 opcodes - compare, like SUB but discards result)

Plus immediate variants: `ADD A, d8`, `ADC A, d8`, `SUB d8`, `SBC A, d8`, `AND d8`, `XOR d8`,
`OR d8`, `CP d8` (8 more opcodes at 0xC6/0xCE/0xD6/0xDE/0xE6/0xEE/0xF6/0xFE)

#### 16-bit Arithmetic (~10 opcodes)

- `ADD HL, rr` for BC/DE/HL/SP - only BC done
- `INC rr` for BC/DE/HL/SP - only BC done
- `DEC rr` for BC/DE/HL/SP - only BC done
- `ADD SP, r8`

#### 8-bit INC/DEC (~12 opcodes)

- `INC r` for B/C/D/E/H/L/(HL)/A - only B and C done
- `DEC r` for B/C/D/E/H/L/(HL)/A - only B and C done

#### Rotate/Shift (4 base opcodes)

- `RLCA` (done), `RLA`, `RRCA`, `RRA`

#### Jump Instructions (~12 opcodes)

- `JP a16`, `JP cc, a16` (4 condition variants)
- `JP (HL)`
- `JR r8` (unconditional), `JR cc, r8` (4 condition variants) - NZ and NC done
- Missing: `JR Z, r8` (0x28), `JR C, r8` (0x38), `JR r8` (0x18)

#### Call/Return Instructions (~10 opcodes)

- `CALL a16`, `CALL cc, a16` (4 variants)
- `RET`, `RET cc` (4 variants), `RETI`
- `RST n` (8 variants at 0xC7/0xCF/0xD7/0xDF/0xE7/0xEF/0xF7/0xFF)

#### Miscellaneous (~15 opcodes)

- `DAA` (decimal adjust after addition - notoriously tricky to implement correctly)
- `CPL` (complement A)
- `CCF` (complement carry flag)
- `SCF` (set carry flag)
- `HALT`
- `DI`, `EI` (disable/enable interrupts)
- `CB` prefix (gateway to 256 more opcodes)

### CB-Prefixed Opcodes (0xCB00-0xCBFF) - 256 opcodes, 0 implemented

The CB prefix unlocks the bit manipulation instruction set. These are highly regular:

| Range | Operation | Count |
|-------|-----------|-------|
| 0xCB00-0xCB07 | RLC r | 8 |
| 0xCB08-0xCB0F | RRC r | 8 |
| 0xCB10-0xCB17 | RL r | 8 |
| 0xCB18-0xCB1F | RR r | 8 |
| 0xCB20-0xCB27 | SLA r | 8 |
| 0xCB28-0xCB2F | SRA r | 8 |
| 0xCB30-0xCB37 | SWAP r | 8 |
| 0xCB38-0xCB3F | SRL r | 8 |
| 0xCB40-0xCB7F | BIT b, r | 64 (8 bits x 8 registers) |
| 0xCB80-0xCBBF | RES b, r | 64 |
| 0xCBC0-0xCBFF | SET b, r | 64 |

These are extremely regular. Each group of 8 does the same operation on registers
B, C, D, E, H, L, (HL), A in that order. A table-driven approach can generate all 256 with
minimal code.

### Overall Opcode Completion

| Category | Implemented | Total | % |
|----------|-------------|-------|---|
| Base opcodes (0x00-0xFF) | 21 | ~245 valid | ~8.6% |
| CB-prefixed (0xCB00-0xCBFF) | 0 | 256 | 0% |
| **Total** | **21** | **~501** | **~4.2%** |

---

## 5. Test Suite Analysis

### Testing Philosophy

The project uses a combination of:
1. **Property-based testing via Hypothesis** - generates random inputs and verifies properties hold
2. **Table-driven tests** - explicit input/output cases (used for RLCA)
3. **Single-case tests** - for trivial opcodes like NOP and STOP

Every test verifies the **complete CPU state** after an operation - not just the registers directly
affected, but *every* register, *every* flag, PC, SP, and memory. This is extremely thorough and
catches side-effect bugs that narrower tests would miss.

### Register Tests (10 files)

Each register has a dedicated test file that:
- Sets one register to a random value in its valid range
- Asserts that register holds the value
- Asserts all other registers are still 0
- Tests overflow behaviour (e.g., writing 0xFF01 to an 8-bit register gives 0x01)

The flag register test (`test_register_F.py`) uses `hypothesis.strategies.booleans()` to test
all 16 combinations of the four flag bits. **However**, this test would not catch the flag setter
bug described in section 6, because it only tests setting flags on a fresh CPU (where `_f` starts
at 0). It never tests clearing a flag that was previously set to 1.

### Opcode Tests (21 files)

Each implemented opcode has a dedicated test file. The pattern is consistent:

```python
class OPCODE_Test(unittest.TestCase):
    @given(integers(min_value=0x00, max_value=0xff))
    def test_opcode(self, input_value):
        cpu = CPU(memory)
        # Set up initial state
        cycles = operation_function(cpu, cpu.M)
        # Assert cycles
        # Assert EVERY register
        # Assert EVERY flag
        # Assert PC and SP
        # Assert memory state
```

**Strengths:**
- Full state verification catches unintended side effects
- Hypothesis generates hundreds of random test cases per test method
- Memory state is verified (not just registers)
- Cycle counts are checked

**Weaknesses:**

1. **Tests duplicate the implementation's logic in assertions.** For example, `test_0x04_inc_b.py`
   asserts `cpu.F_Z == (b+1 & 0xff == 0)` - which is the exact same expression as the
   implementation. If the expression is wrong (and it is - see section 6), both implementation and
   test will agree on the wrong answer. The test should instead use independently computed expected
   values, e.g.:
   ```python
   expected_b = (b + 1) & 0xff
   expected_z = 1 if expected_b == 0 else 0
   self.assertEqual(cpu.F_Z, expected_z)
   ```

2. **Tests call operation functions directly, bypassing the dispatch table.** The dispatch table
   (`op_codes.py`) is where the 0x08 bug lives (missing memory parameter). Direct-call tests won't
   catch dispatch-level bugs.

3. **One file per opcode doesn't scale.** At 500 opcodes, that's 500 test files. With many opcodes
   being the same operation on different registers (INC B, INC C, INC D...), this creates massive
   duplication. See section 9 for a parameterised alternative.

4. **Jump tests don't test signed offsets.** The tests for JR NZ (0x20) and JR NC (0x30) generate
   r8 values from 0x00-0xFF but treat them as unsigned, matching the implementation bug. A correct
   test would verify backward jumps (e.g., r8=0xFE means jump back 2 bytes).

5. **No integration tests.** There are no tests that run a sequence of instructions through the
   dispatch table to verify multi-instruction behaviour. For example, testing that a loop works:
   `LD B, 5 / DEC B / JR NZ, -2`.

---

## 6. Bugs and Correctness Issues

### BUG 1: Flag Setters Cannot Clear Flags (CRITICAL)

**Location:** `src/processor/cpu.py` lines 93, 98, 103, 108

**The Problem:**

All four flag setters use OR to set the bit but never clear it first:

```python
# Current code (line 93):
def F_Z(self, value): self._f = (1 & value) << 7 | self._f
```

When `value` is 0, this computes `(1 & 0) << 7 | self._f` which is `0 | self._f` - the flag
remains unchanged. Once a flag is set to 1, it can **never be cleared** through the property setter.

**Walkthrough:**

```
Initial state: self._f = 0b10000000  (Z flag is set)

Setting Z to 0:
  (1 & 0) << 7 | self._f
  = 0 << 7 | 0b10000000
  = 0 | 0b10000000
  = 0b10000000  <-- Z is STILL 1!

Setting Z to 1:
  (1 & 1) << 7 | self._f
  = 1 << 7 | 0b10000000
  = 0b10000000 | 0b10000000
  = 0b10000000  <-- works, but only because it was already 1
```

**Impact:** This is the most critical bug. Nearly every arithmetic/logic instruction sets flags,
and many instructions need to clear flags. For example, INC B should clear the N flag. If N was
previously set by a DEC instruction, INC B will fail to clear it. This means any sequence of
instructions that depends on flag state will produce incorrect results.

**Correct implementation:**

```python
@F_Z.setter
def F_Z(self, value):
    self._f = (self._f & ~(1 << 7)) | ((1 & value) << 7)
```

This first clears bit 7 with `& ~(1 << 7)` (AND with 0b01111111), then ORs in the new value.

**Why tests don't catch this:** Every test creates a fresh CPU with `_f = 0`. Flags only get set
during the operation under test. Since tests don't run sequences of operations, there's never a
scenario where a flag needs to be cleared after being set by a previous operation.

---

### BUG 2: ADD HL, BC Flag Calculation Always Produces False (CRITICAL)

**Location:** `src/processor/operations.py` lines 72-73

**The Problem:**

```python
cpu.F_H = (cpu.HL + cpu.BC) & 0x0fff > 0x0fff
cpu.F_C = (cpu.HL + cpu.BC) & 0xffff > 0xffff
```

The expression `X & 0x0fff` produces a value in the range `[0, 0x0fff]`. A value in this range
can never be `> 0x0fff`. Therefore `cpu.F_H` is **always False**.

Similarly, `X & 0xffff` produces a value in `[0, 0xffff]`, which can never be `> 0xffff`.
Therefore `cpu.F_C` is **always False**.

**Correct implementation:**

For ADD HL, rr on the Game Boy:
- Half-carry (H) is set if there's a carry from bit 11 to bit 12
- Carry (C) is set if the result exceeds 0xFFFF

```python
cpu.F_H = ((cpu.HL & 0x0fff) + (cpu.BC & 0x0fff)) > 0x0fff
cpu.F_C = (cpu.HL + cpu.BC) > 0xffff
```

**Why tests don't catch this:** The test at `test_0x09_add_hl_bc.py` line 27-28 uses the exact
same incorrect expressions for its expected values:

```python
self.assertEqual(cpu.F_H, (hl + bc) & 0x0fff > 0x0fff)  # Also always False
self.assertEqual(cpu.F_C, (hl + bc) & 0xffff > 0xffff)  # Also always False
```

Both the implementation and the test agree that these flags should always be 0, so the test passes.
This is a textbook example of why test assertions should not duplicate implementation logic.

---

### BUG 3: Opcode 0x08 Missing Memory Parameter (BROKEN)

**Location:** `src/processor/op_codes.py` line 13

**The Problem:**

```python
0x08: lambda cpu: operations.ld_a16_sp(cpu),
```

The `ld_a16_sp` function signature is `def ld_a16_sp(cpu: CPU, mem: list[int])`. The lambda only
passes `cpu`, not `cpu.M`. This will raise `TypeError: ld_a16_sp() missing 1 required positional
argument: 'mem'` when opcode 0x08 is encountered during execution.

**Fix:**

```python
0x08: lambda cpu: operations.ld_a16_sp(cpu, cpu.M),
```

**Why tests don't catch this:** The test calls `ld_a16_sp(cpu, cpu.M)` directly, bypassing the
dispatch table entirely.

---

### BUG 4: Relative Jumps Treat Offset as Unsigned (CRITICAL)

**Location:** `src/processor/operations.py` lines 127 and 140

**The Problem:**

```python
# 0x20 JR NZ, r8 (line 127):
cpu.PC += mem[cpu.PC+1]

# 0x30 JR NC, r8 (line 140):
cpu.PC += mem[cpu.PC+1]
```

The `r8` operand in JR instructions is a **signed** 8-bit offset (-128 to +127). A byte value
of 0xFE means -2, not 254. The current code treats it as unsigned, so backward jumps (the primary
use case for conditional JR instructions in loops) will instead jump forward by a huge amount.

**The Game Boy boot ROM depends heavily on JR for loops.** Without signed offset handling, the
boot ROM cannot execute correctly.

**Additionally:** Neither JR implementation accounts for the instruction's own length. The offset is
relative to the instruction **after** the JR instruction. Since JR is 2 bytes long, the correct
behaviour is:

```python
offset = mem[cpu.PC + 1]
if offset > 127:
    offset -= 256  # Convert to signed
cpu.PC += 2 + offset  # +2 for the JR instruction itself
```

Or equivalently using two's complement:

```python
import ctypes
offset = ctypes.c_int8(mem[cpu.PC + 1]).value
cpu.PC += 2 + offset
```

The current code also doesn't add 2 for the instruction length when the jump is taken, which
compounds the error.

For the non-jumping case, the code does `cpu.PC += 1` but should do `cpu.PC += 2` (JR is a 2-byte
instruction). Let me check the actual code more carefully:

- `jr_nz_r8`: When Z is set (no jump), does `cpu.PC += 1` - should be `+= 2`
- `jr_nc_r8`: When C is set (no jump), does `cpu.PC += 1` - should be `+= 2`

So the non-jumping branch also has a bug: it only advances PC by 1 instead of 2.

---

### BUG 5: Typo in xor_a - `cpu.FZ` vs `cpu.F_Z` (MEDIUM)

**Location:** `src/processor/operations.py` line 155

**The Problem:**

```python
def xor_a(cpu: CPU):
    cpu.A ^= cpu.A
    if cpu.A: cpu.FZ = 0      # <-- "FZ" instead of "F_Z"
    else: cpu.F_Z = 1
    cpu.PC += 1
    return 4
```

`cpu.FZ` doesn't exist as a property. This would raise `AttributeError` at runtime. However,
`XOR A` with itself **always** produces 0 (any value XOR itself is 0), so `cpu.A` is always
falsy after the XOR, and the `if` branch is never reached - only the `else` branch runs.

The function also doesn't clear the N, H, and C flags. On real hardware, XOR always clears N, H,
and C to 0. Since the CPU initialises all flags to 0 and the flag setters can't clear flags anyway
(Bug 1), this hasn't surfaced yet, but it's still incorrect.

**Additionally:** `XOR A` is implemented as a special case that only XORs A with itself. The real
opcode 0xAF is indeed XOR A,A, but there are 7 other XOR opcodes (XOR B, XOR C, etc.) that XOR A
with other registers. When you implement those, XOR with a non-zero register followed by XOR A
would hit the buggy `cpu.FZ` line.

---

### BUG 6: RLCA Doesn't Clear Z Flag Correctly (SUBTLE)

**Location:** `src/processor/operations.py` lines 53-58

**The Problem:**

```python
def rlca(cpu: CPU):
    cpu.F_Z = 0
    cpu.F_N = 0
    cpu.F_H = 0
    cpu.F_C = ((cpu.A << 1) & 256) >> 8
    cpu.A = ((cpu.A << 1) & 255) | cpu.F_C
    cpu.PC += 1
    return 4
```

Due to Bug 1 (flag setters can't clear), `cpu.F_Z = 0` is a no-op if Z was previously set.
The RLCA instruction should always clear Z, N, and H. If any of these were set by a prior
instruction, they'll remain set incorrectly.

This applies to **every opcode that attempts to clear a flag**, which is most of them.

---

### BUG 7: Operator Precedence in INC/DEC Zero Flag Check (SUBTLE)

**Location:** `src/processor/operations.py` lines 29, 38, 92, 101

**The Problem:**

```python
# INC B (line 29):
cpu.F_Z = cpu.B+1 & 0xff == 0

# DEC B (line 38):
cpu.F_Z = cpu.B-1 & 0xff == 0
```

Python's operator precedence means `==` binds tighter than `&`. So this actually parses as:

```python
cpu.F_Z = cpu.B+1 & (0xff == 0)
cpu.F_Z = cpu.B+1 & False
cpu.F_Z = cpu.B+1 & 0
cpu.F_Z = 0  # Always!
```

Wait, let me re-check. Python precedence: `+` > `&` > `==`. Actually:

- `+` has higher precedence than `&`
- `==` has lower precedence than `&`... no wait.

Actually in Python: `+` (13) > `==` (8) > `&` (7). So:

```
cpu.B+1 & 0xff == 0
= (cpu.B+1) & (0xff == 0)
= (cpu.B+1) & False
= (cpu.B+1) & 0
= 0
```

No wait, `&` is actually precedence 9, and `==` is precedence 8. Let me get this right.

Python operator precedence (higher number = higher precedence):
- `+` `-` : 12
- `<<` `>>` : 11
- `&` : 10
- `^` : 9
- `|` : 8
- `==` `!=` `<` `>` : 7

So `&` binds tighter than `==`. The expression `cpu.B+1 & 0xff == 0` parses as:

```
((cpu.B+1) & 0xff) == 0
```

Which is actually **correct** - it checks if `(B+1) & 0xFF` equals zero. The parentheses aren't
needed here because `&` already has higher precedence than `==`. So this is fine, just hard to
read without explicit parentheses.

**Update: This is NOT a bug - the precedence works out correctly.** But it's still worth adding
parentheses for readability: `(cpu.B + 1) & 0xff == 0` could be written as `((cpu.B + 1) & 0xff) == 0`.

---

### BUG 8: DEC Half-Carry Uses Wrong Check (MEDIUM)

**Location:** `src/processor/operations.py` lines 40, 103

**The Problem:**

```python
# DEC B (line 40):
cpu.F_H = (cpu.B & 0x0f) - 1 > 0xff

# DEC C (line 103):
cpu.F_H = (cpu.C & 0x0f) - 1 > 0xff
```

`(cpu.B & 0x0f)` produces a value in [0, 15]. Subtracting 1 gives [-1, 14]. In Python, -1 is
a true negative integer (not an unsigned underflow like in C). So `-1 > 0xff` is `-1 > 255`
which is `False`. For any non-negative result, `X > 255` is also `False` when X is at most 14.

Wait - actually when `cpu.B & 0x0f` is 0 (i.e. B's lower nibble is 0), then `0 - 1 = -1`. In
Python, `-1 > 0xff` evaluates to `False`. But the half-carry flag for DEC **should** be set when
there's a borrow from bit 4 - which happens exactly when the lower nibble is 0.

The correct check for DEC half-carry:

```python
cpu.F_H = (cpu.B & 0x0f) == 0  # Borrow from bit 4 occurs when lower nibble is 0
```

Or equivalently:

```python
cpu.F_H = ((cpu.B & 0x0f) - 1) < 0  # Underflow in lower nibble
```

**Impact:** The half-carry flag is never set correctly for DEC operations. Some games and the
boot ROM use DAA (decimal adjust) which depends on the H flag, so this will cause incorrect
BCD arithmetic.

**Note:** The tests use the same incorrect expression, so they pass despite the bug.

---

### Summary of Bugs

| # | Severity | Location | Description |
|---|----------|----------|-------------|
| 1 | CRITICAL | cpu.py flag setters | Flags can never be cleared once set |
| 2 | CRITICAL | add_hl_bc | H and C flags always read as 0 |
| 3 | BROKEN | op_codes.py 0x08 | Missing memory parameter crashes at runtime |
| 4 | CRITICAL | jr_nz_r8, jr_nc_r8 | Unsigned offset (can't jump backwards) + wrong PC advance |
| 5 | MEDIUM | xor_a | Typo `FZ` vs `F_Z`, missing flag clears |
| 6 | SUBTLE | rlca + all flag-clearing ops | Flag clears are no-ops (consequence of Bug 1) |
| 7 | NOT A BUG | inc/dec Z flag | Precedence is actually correct, just hard to read |
| 8 | MEDIUM | dec_b, dec_c | Half-carry check can never be True |

---

## 7. Missing Emulator Subsystems

### 7.1 Memory Management Unit (MMU)

**Current state:** Memory is a flat list of 65537 integers. No address decoding, no I/O registers,
no ROM/RAM banking.

**What the Game Boy actually has:**

The Game Boy's 16-bit address space (0x0000-0xFFFF) is divided into distinct regions:

| Address Range | Size | Purpose |
|---------------|------|---------|
| 0x0000-0x3FFF | 16 KB | ROM Bank 0 (fixed) |
| 0x4000-0x7FFF | 16 KB | ROM Bank N (switchable) |
| 0x8000-0x9FFF | 8 KB | Video RAM (VRAM) |
| 0xA000-0xBFFF | 8 KB | External/Cartridge RAM |
| 0xC000-0xCFFF | 4 KB | Work RAM Bank 0 |
| 0xD000-0xDFFF | 4 KB | Work RAM Bank 1 |
| 0xE000-0xFDFF | ~8 KB | Echo RAM (mirror of C000-DDFF) |
| 0xFE00-0xFE9F | 160 B | OAM (Sprite Attribute Table) |
| 0xFEA0-0xFEFF | 96 B | Unusable |
| 0xFF00-0xFF7F | 128 B | I/O Registers |
| 0xFF80-0xFFFE | 127 B | High RAM (HRAM) |
| 0xFFFF | 1 B | Interrupt Enable Register |

**Why this matters:** Reading/writing to the I/O register range (0xFF00-0xFF7F) has side effects.
For example:
- Writing to 0xFF40 (LCDC) enables/disables the LCD
- Writing to 0xFF46 (DMA) triggers a 160-byte OAM DMA transfer
- Reading 0xFF00 (JOYP) returns joypad state
- Writing to 0xFF04 (DIV) resets the divider counter

A flat list can't model any of this. You'll need a class that intercepts reads and writes to
specific address ranges and routes them to the appropriate subsystem.

### 7.2 Picture Processing Unit (PPU / GPU)

**Current state:** Not implemented at all.

**What it needs to do:**

The PPU renders 160x144 pixel frames at ~59.7 fps. It operates on a scanline-by-scanline basis,
with each scanline taking exactly 456 CPU cycles. The screen has 144 visible scanlines plus 10
V-Blank scanlines (154 total).

Each scanline goes through these modes:

| Mode | Duration | What Happens |
|------|----------|-------------|
| Mode 2: OAM Search | 80 cycles | Scans OAM for sprites on this line |
| Mode 3: Pixel Transfer | 168-291 cycles (variable) | Renders pixels to LCD |
| Mode 0: H-Blank | Remainder of 456 cycles | CPU can access VRAM/OAM |
| Mode 1: V-Blank | 10 scanlines (4560 cycles) | Frame complete, CPU can access VRAM/OAM |

The PPU uses:
- **Background tiles:** 32x32 grid of 8x8 pixel tiles, scrollable via SCX/SCY registers
- **Window:** An overlay layer, positioned via WX/WY registers
- **Sprites:** Up to 40 sprites, 8x8 or 8x16 pixels, max 10 per scanline
- **Palettes:** 4 shades of grey (DMG), selectable via BGP, OBP0, OBP1 registers
- **Tile data:** Stored in VRAM at 0x8000-0x97FF (384 tiles)
- **Tile maps:** Two 32x32 maps at 0x9800-0x9BFF and 0x9C00-0x9FFF

This is the most complex subsystem to implement. The timing is critical - many games rely on
mid-scanline register changes (raster effects) for visual effects.

**Minimum viable PPU:** For a first pass, you could implement a scanline renderer that draws the
background layer without scrolling or sprites. This would be enough to see output from the boot
ROM (the Nintendo logo scroll).

### 7.3 Audio Processing Unit (APU)

**Current state:** Not implemented.

**What it does:** The Game Boy has 4 audio channels:

| Channel | Type | Description |
|---------|------|-------------|
| CH1 | Square wave | With frequency sweep, envelope, duty cycle |
| CH2 | Square wave | Envelope and duty cycle (no sweep) |
| CH3 | Waveform | Plays custom 4-bit waveform samples |
| CH4 | Noise | LFSR-based noise with envelope |

Audio is controlled through I/O registers at 0xFF10-0xFF3F. The APU runs independently of the
CPU and generates samples at the system clock rate.

**Priority:** Low. You can get a fully playable emulator without audio. Implement this last.

### 7.4 Interrupt System

**Current state:** Not implemented.

**What it does:** The Game Boy has 5 interrupt sources:

| Bit | Priority | Address | Source |
|-----|----------|---------|--------|
| 0 | Highest | 0x0040 | V-Blank (PPU finished frame) |
| 1 | | 0x0048 | LCD STAT (PPU mode/LYC match) |
| 2 | | 0x0050 | Timer overflow |
| 3 | | 0x0058 | Serial transfer complete |
| 4 | Lowest | 0x0060 | Joypad input |

When an interrupt fires:
1. The corresponding bit is set in the IF register (0xFF0F)
2. If IME (Interrupt Master Enable) is set AND the corresponding bit in IE (0xFFFF) is set:
   - IME is cleared
   - Current PC is pushed to stack
   - PC jumps to the interrupt handler address

The `DI` instruction clears IME, `EI` sets it (with one instruction delay), `RETI` returns from
interrupt and re-enables IME.

**Priority:** High. The boot ROM relies on V-Blank interrupts. Most games won't function without
the interrupt system.

### 7.5 Timer

**Current state:** Not implemented.

**What it does:** Four I/O registers control the timer:

| Address | Name | Function |
|---------|------|----------|
| 0xFF04 | DIV | Divider register - increments at 16384 Hz, resets on write |
| 0xFF05 | TIMA | Timer counter - increments at selectable rate |
| 0xFF06 | TMA | Timer modulo - TIMA reloads this value on overflow |
| 0xFF07 | TAC | Timer control - enable bit + clock select |

When TIMA overflows (exceeds 0xFF), it triggers a timer interrupt and reloads from TMA.

**Priority:** Medium. Many games use the timer for game logic timing.

### 7.6 Joypad Input

**Current state:** Not implemented.

**What it does:** The joypad has 8 buttons read through a single I/O register at 0xFF00 (JOYP).
The register uses a multiplexed design:

- Write bit 4 low to select D-pad buttons (Right, Left, Up, Down)
- Write bit 5 low to select action buttons (A, B, Select, Start)
- Read bits 0-3 for the selected button states (0 = pressed)

Pressing any button can trigger a joypad interrupt (INT 4).

This would map to pygame's keyboard input or controller input.

### 7.7 Cartridge / MBC (Memory Bank Controller)

**Current state:** Not implemented.

**What it does:** Game Boy cartridges contain varying amounts of ROM and optionally RAM, controlled
by a Memory Bank Controller chip. The MBC type is specified in the cartridge header at address
0x0147.

| MBC Type | ROM Size | RAM | Notes |
|----------|----------|-----|-------|
| ROM Only | 32 KB | No | Tetris, simple games |
| MBC1 | Up to 2 MB | Up to 32 KB | Most common early MBC |
| MBC2 | Up to 256 KB | 512x4 bits | Built-in RAM |
| MBC3 | Up to 2 MB | Up to 32 KB | Has real-time clock |
| MBC5 | Up to 8 MB | Up to 128 KB | Used by later games |

Writing to the ROM address space (0x0000-0x7FFF) doesn't actually write to ROM - it sends
commands to the MBC to switch banks, enable/disable RAM, etc.

**Priority:** Medium. You need at minimum ROM-only support to run simple games, and MBC1 to run
most commercial titles.

### 7.8 Serial I/O

**Current state:** Not implemented.

Used for Link Cable communication. Low priority unless you want multiplayer support. However,
some test ROMs use serial output to report test results (writing to 0xFF01/0xFF02).

### 7.9 Boot ROM

**Current state:** The entry point references `etc/roms/bootrom.bin` which doesn't exist.

The Game Boy boot ROM is a 256-byte program that:
1. Initialises the hardware
2. Reads the Nintendo logo from the cartridge header
3. Scrolls it down the screen
4. Plays the startup sound
5. Verifies the logo matches Nintendo's (anti-piracy check)
6. Unmaps itself, leaving the cartridge ROM visible at 0x0000-0x00FF

You can skip boot ROM emulation entirely by initialising registers to the post-boot-ROM values:
```
A=0x01  F=0xB0  B=0x00  C=0x13  D=0x00  E=0xD8  H=0x01  L=0x4D
SP=0xFFFE  PC=0x0100
```

This is what most emulators do and lets you jump straight to running cartridge code.

---

## 8. Scalability Concerns and Refactoring Opportunities

### 8.1 Dispatch Table Recreated Per Instruction

**Current code:**

```python
def process(c, cpu):
    codes = {
        0x00: lambda cpu: operations.nop(cpu),
        # ... 21 entries ...
    }
    return codes[c](cpu)
```

The dictionary `codes` is constructed inside the function body, so it's rebuilt on **every single
instruction execution**. At 4.19 MHz, that's 4.19 million dictionary constructions per second of
emulated time. Each construction allocates a new dict, creates new lambda objects, and immediately
discards them.

**Fix:** Move the dictionary to module level, or make it a class attribute, so it's built once:

```python
_CODES = {
    0x00: lambda cpu: operations.nop(cpu),
    # ...
}

def process(c, cpu):
    return _CODES[c](cpu)
```

Or even better, use a list (array) indexed by opcode for O(1) access without hashing:

```python
_CODES = [None] * 256
_CODES[0x00] = lambda cpu: operations.nop(cpu)
# ...

def process(c, cpu):
    handler = _CODES[c]
    if handler is None:
        raise ValueError(f"Unimplemented opcode: 0x{c:02X}")
    return handler(cpu)
```

### 8.2 One Function Per Opcode Doesn't Scale

Many opcodes are the same operation on different registers. Currently you have separate functions
for `inc_b` and `inc_c`, which are identical except for which register they touch. There are 8
INC register opcodes (B, C, D, E, H, L, (HL), A). Writing 8 separate functions means 8x the
code and 8x the maintenance burden.

**Alternative - Generic operations:**

```python
def inc_r8(cpu: CPU, reg: str):
    val = getattr(cpu, reg)
    result = (val + 1) & 0xff
    cpu.F_Z = int(result == 0)
    cpu.F_N = 0
    cpu.F_H = int((val & 0x0f) + 1 > 0x0f)
    setattr(cpu, reg, result)
    cpu.PC += 1
    return 4
```

Then the dispatch table becomes:

```python
0x04: lambda cpu: inc_r8(cpu, 'B'),
0x0C: lambda cpu: inc_r8(cpu, 'C'),
0x14: lambda cpu: inc_r8(cpu, 'D'),
0x1C: lambda cpu: inc_r8(cpu, 'E'),
0x24: lambda cpu: inc_r8(cpu, 'H'),
0x2C: lambda cpu: inc_r8(cpu, 'L'),
0x3C: lambda cpu: inc_r8(cpu, 'A'),
```

This pattern can be applied to most opcode families: INC, DEC, ADD, ADC, SUB, SBC, AND, XOR, OR,
CP, LD r,r', and all CB-prefix operations.

### 8.3 Memory Abstraction

The current design passes `mem: list[int]` directly to operations. When you implement an MMU,
you'll want reads and writes to go through accessor methods that can intercept I/O register
accesses. This means changing from:

```python
value = mem[address]
mem[address] = value
```

To:

```python
value = mmu.read(address)
mmu.write(address, value)
```

Every operation that accesses memory will need updating. Consider doing this refactor before
adding more opcodes, so you don't have to change hundreds of functions later.

### 8.4 The Test File Explosion

With the one-file-per-opcode approach:
- Current: 21 test files for 21 opcodes
- Full CPU: ~500 test files for ~500 opcodes
- Many would be near-identical copies (e.g., test_inc_b, test_inc_c, test_inc_d...)

See section 9 for a parameterised approach that can collapse these into a handful of test files.

---

## 9. Suggested Parameterised Test Approach

Instead of one test file per opcode, you can use `pytest.mark.parametrize` or `unittest.subTest`
to test families of similar opcodes from a single test class. Here are concrete examples:

### Example 1: Parameterised INC r8 Tests

This single test file replaces 7 separate test files (test_0x04_inc_b.py, test_0x0c_inc_c.py, etc.):

```python
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor import operations

# Define the family: (opcode, operation_func, register_name)
INC_R8_CASES = [
    (0x04, operations.inc_b, 'B'),
    (0x0C, operations.inc_c, 'C'),
    # When you implement these, just add rows:
    # (0x14, operations.inc_d, 'D'),
    # (0x1C, operations.inc_e, 'E'),
    # (0x24, operations.inc_h, 'H'),
    # (0x2C, operations.inc_l, 'L'),
    # (0x3C, operations.inc_a, 'A'),
]


class TestIncR8:
    """Tests for all INC r8 instructions.

    All INC r8 instructions behave identically:
    - Increment the target register (wrapping at 0xFF -> 0x00)
    - Set Z if result is 0
    - Clear N
    - Set H if carry from bit 3 to bit 4
    - Don't touch C flag
    - Advance PC by 1
    - Take 4 cycles
    """

    @pytest.mark.parametrize("opcode,op_func,reg", INC_R8_CASES,
                             ids=[f"0x{op:02X}_INC_{reg}" for op, _, reg in INC_R8_CASES])
    @given(value=integers(min_value=0x00, max_value=0xFF))
    def test_inc_r8(self, opcode, op_func, reg, value):
        cpu = CPU([])
        setattr(cpu, reg, value)

        cycles = op_func(cpu)

        expected_result = (value + 1) & 0xFF

        # Cycle count
        assert cycles == 4

        # Target register
        assert getattr(cpu, reg) == expected_result

        # Flags
        assert cpu.F_Z == (1 if expected_result == 0 else 0)
        assert cpu.F_N == 0
        assert cpu.F_H == (1 if (value & 0x0F) + 1 > 0x0F else 0)
        assert cpu.F_C == 0  # Unchanged (and starts at 0)

        # PC
        assert cpu.PC == 1

    @pytest.mark.parametrize("opcode,op_func,reg", INC_R8_CASES,
                             ids=[f"0x{op:02X}_INC_{reg}_overflow" for op, _, reg in INC_R8_CASES])
    def test_inc_r8_overflow(self, opcode, op_func, reg):
        """Specific test: INC 0xFF should wrap to 0x00 and set Z flag."""
        cpu = CPU([])
        setattr(cpu, reg, 0xFF)

        cycles = op_func(cpu)

        assert getattr(cpu, reg) == 0x00
        assert cpu.F_Z == 1
        assert cpu.F_H == 1  # 0x0F + 1 > 0x0F

    @pytest.mark.parametrize("opcode,op_func,reg", INC_R8_CASES,
                             ids=[f"0x{op:02X}_INC_{reg}_half_carry" for op, _, reg in INC_R8_CASES])
    def test_inc_r8_half_carry_boundary(self, opcode, op_func, reg):
        """Specific test: INC 0x0F should set H flag (carry from bit 3)."""
        cpu = CPU([])
        setattr(cpu, reg, 0x0F)

        cycles = op_func(cpu)

        assert getattr(cpu, reg) == 0x10
        assert cpu.F_Z == 0
        assert cpu.F_H == 1

    @pytest.mark.parametrize("opcode,op_func,reg", INC_R8_CASES,
                             ids=[f"0x{op:02X}_INC_{reg}_no_half_carry" for op, _, reg in INC_R8_CASES])
    def test_inc_r8_no_half_carry(self, opcode, op_func, reg):
        """Specific test: INC 0x0E should NOT set H flag."""
        cpu = CPU([])
        setattr(cpu, reg, 0x0E)

        cycles = op_func(cpu)

        assert getattr(cpu, reg) == 0x0F
        assert cpu.F_H == 0
```

### Example 2: Parameterised LD rr, d16 Tests

Replaces test_0x01_ld_bc_d16.py, test_0x11_ld_de_d16.py, test_0x21_ld_hl_d16.py,
test_0x31_ld_sp_d16.py:

```python
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor import operations

LD_RR_D16_CASES = [
    (0x01, operations.ld_bc_d16, 'BC'),
    (0x11, operations.ld_de_d16, 'DE'),
    (0x21, operations.ld_hl_d16, 'HL'),
    (0x31, operations.ld_sp_d16, 'SP'),
]


class TestLdRrD16:
    """Tests for all LD rr, d16 instructions.

    All load 16-bit immediate into a register pair:
    - Read 2 bytes after opcode (little-endian)
    - Store in target register pair
    - No flags affected
    - Advance PC by 3
    - Take 12 cycles
    """

    @pytest.mark.parametrize("opcode,op_func,reg", LD_RR_D16_CASES,
                             ids=[f"0x{op:02X}_LD_{reg}_d16" for op, _, reg in LD_RR_D16_CASES])
    @given(
        low_byte=integers(min_value=0x00, max_value=0xFF),
        high_byte=integers(min_value=0x00, max_value=0xFF),
    )
    def test_ld_rr_d16(self, opcode, op_func, reg, low_byte, high_byte):
        memory = [opcode, low_byte, high_byte]
        cpu = CPU(memory)

        cycles = op_func(cpu, cpu.M)

        expected_value = (high_byte << 8) | low_byte

        assert cycles == 12
        assert getattr(cpu, reg) == expected_value
        assert cpu.PC == 3

        # No flags affected
        assert cpu.F_Z == 0
        assert cpu.F_N == 0
        assert cpu.F_H == 0
        assert cpu.F_C == 0
```

### Example 3: Parameterised ALU Tests (for when you implement 0x80-0xBF)

This pattern would handle all 64 ALU register operations (ADD/ADC/SUB/SBC/AND/XOR/OR/CP x
B/C/D/E/H/L/(HL)/A):

```python
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU

REGISTERS = ['B', 'C', 'D', 'E', 'H', 'L', 'A']

# Build test cases programmatically
ADD_A_CASES = [
    (0x80, 'B'), (0x81, 'C'), (0x82, 'D'), (0x83, 'E'),
    (0x84, 'H'), (0x85, 'L'), (0x87, 'A'),
]


class TestAddAR8:
    @pytest.mark.parametrize("opcode,reg", ADD_A_CASES,
                             ids=[f"0x{op:02X}_ADD_A_{reg}" for op, reg in ADD_A_CASES])
    @given(
        a=integers(min_value=0x00, max_value=0xFF),
        r=integers(min_value=0x00, max_value=0xFF),
    )
    def test_add_a_r8(self, opcode, reg, a, r):
        cpu = CPU([])
        cpu.A = a
        if reg != 'A':
            setattr(cpu, reg, r)
            operand = r
        else:
            operand = a  # ADD A, A uses the same value for both

        # Call the operation (assuming generic implementation)
        # cycles = add_a_r8(cpu, reg)

        expected = (a + operand) & 0xFF
        expected_z = 1 if expected == 0 else 0
        expected_n = 0
        expected_h = 1 if (a & 0x0F) + (operand & 0x0F) > 0x0F else 0
        expected_c = 1 if a + operand > 0xFF else 0

        # assert cpu.A == expected
        # assert cpu.F_Z == expected_z
        # ... etc
```

### Example 4: Parameterised CB-Prefix Tests

The CB opcodes are the most regular and benefit the most from parameterisation. All 256 can be
tested from a small number of test classes:

```python
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU

REGISTERS = ['B', 'C', 'D', 'E', 'H', 'L', 'A']  # (HL) handled separately

# RLC r: opcodes 0xCB00-0xCB07
RLC_CASES = [(0x00 + i, reg) for i, reg in enumerate(REGISTERS)]

# BIT b, r: opcodes 0xCB40-0xCB7F
BIT_CASES = [
    (0x40 + bit * 8 + reg_idx, bit, reg)
    for bit in range(8)
    for reg_idx, reg in enumerate(REGISTERS)
]


class TestCbBit:
    """Tests all 56 BIT b, r instructions (excluding (HL) variants)."""

    @pytest.mark.parametrize("opcode,bit,reg", BIT_CASES,
                             ids=[f"0xCB{op:02X}_BIT_{bit}_{reg}" for op, bit, reg in BIT_CASES])
    @given(value=integers(min_value=0x00, max_value=0xFF))
    def test_bit_b_r(self, opcode, bit, reg, value):
        cpu = CPU([0xCB, opcode])
        setattr(cpu, reg, value)

        # cycles = cb_bit(cpu, bit, reg)

        # BIT sets Z to the complement of the tested bit
        expected_z = 0 if (value >> bit) & 1 else 1

        # assert cpu.F_Z == expected_z
        # assert cpu.F_N == 0
        # assert cpu.F_H == 1  # Always set for BIT
        # C flag unaffected
```

### Key Benefits of This Approach

1. **Adding a new opcode = adding one row to a list.** No new file, no copy-paste.
2. **Test logic is written once and verified once.** If the expected value computation is correct
   for INC B, it's correct for INC C through INC A.
3. **Expected values are computed independently of the implementation.** Instead of
   `assert cpu.F_Z == (b+1 & 0xff == 0)` (which duplicates the implementation), you compute the
   expected value step by step in a way that's obviously correct.
4. **pytest output clearly identifies which opcode/register combination failed.**
5. **Scales to 500 opcodes in ~10-15 test files** instead of ~500 test files.

### Migration Path

You don't have to rewrite all existing tests at once. You could:
1. Create new parameterised test files alongside the old ones
2. Migrate one opcode family at a time (e.g., move all INC tests into one file)
3. Delete the old individual files once the parameterised versions are passing
4. Write all new opcodes using the parameterised approach from the start

---

## 10. Recommended Next Steps

Here's a prioritised roadmap for getting the emulator to a functional state, ordered by what
unblocks the most progress:

### Phase 1: Fix Critical Bugs

Before writing any new opcodes, fix the bugs in existing code. Every new arithmetic/logic opcode
will be broken by the flag setter bug.

1. **Fix flag setters** in `cpu.py` (Bug 1) - this is the single most impactful fix
2. **Fix ADD HL, BC flag calculations** (Bug 2)
3. **Fix relative jump signed offset + PC advance** (Bug 4)
4. **Fix opcode 0x08 dispatch** (Bug 3)
5. **Fix XOR A** - typo and missing flag clears (Bug 5)
6. **Fix DEC half-carry** (Bug 8)
7. **Update tests** to use independently-computed expected values so they actually catch bugs
8. **Add AF register pair property** to the CPU class

### Phase 2: Refactor for Scale

Before grinding through 480 more opcodes, set up the infrastructure to make it painless:

1. **Move dispatch table to module level** (or use a list)
2. **Create generic operation functions** for repeated patterns (inc_r8, dec_r8, ld_r_r, etc.)
3. **Set up parameterised tests** so adding a new opcode is one line
4. **Introduce an MMU class** with read/write methods, even if it's just a wrapper around the
   flat list initially. This avoids having to change every operation function later.

### Phase 3: Complete the CPU

Work through the opcode table systematically. With generic operations, most families can be
knocked out quickly:

1. **LD r, r' block** (0x40-0x7F) - 49 opcodes from one generic function
2. **ALU block** (0x80-0xBF) - 64 opcodes from 8 generic functions
3. **Remaining 0x00-0x3F** - miscellaneous loads, INC/DEC, rotates, JR
4. **0xC0-0xFF** - control flow (CALL, RET, RST, PUSH, POP), remaining loads, ALU immediates
5. **CB prefix** (0xCB00-0xCBFF) - 256 opcodes from ~11 generic functions
6. **DAA** - implement this carefully, it's the trickiest single opcode

### Phase 4: Build the Skeleton of Other Subsystems

1. **Interrupt system** - IME flag, IE/IF registers, interrupt dispatch
2. **Timer** - DIV, TIMA, TMA, TAC registers and timer interrupt
3. **Basic PPU** - scanline counter, mode transitions, V-Blank interrupt, LCDC/STAT registers
4. **Skip boot ROM** - initialise registers to post-boot values, start PC at 0x0100

At this point you could potentially run simple test ROMs (like Blargg's cpu_instrs) that output
results via serial or memory.

### Phase 5: Display Output

1. **Background rendering** - read tile map, look up tile data, render scanlines
2. **Integrate with pygame** - create a 160x144 window, blit framebuffer
3. **Scrolling** - SCX/SCY register support
4. **Window layer** - WX/WY support

This is the milestone where you'd first see output on screen.

### Phase 6: Playability

1. **Joypad input** - map keyboard/controller to JOYP register
2. **Sprite rendering** - OAM parsing, sprite priority, 10-per-line limit
3. **MBC1 cartridge support** - ROM banking to run commercial games
4. **Frame timing** - pace emulation to 59.7 fps

### Phase 7: Polish

1. **Audio** (APU)
2. **MBC3/MBC5** for broader game compatibility
3. **Save states** (serialise CPU/MMU/PPU state)
4. **More accurate PPU timing** (if you want to pass test ROMs)

---

## Appendix: Useful References

- **Pan Docs** - The definitive Game Boy technical reference: https://gbdev.io/pandocs/
- **Opcode table** - Complete instruction set with flags and timing: https://gbdev.io/gb-opcodes/optables/
- **Blargg's test ROMs** - CPU instruction tests that catch flag/timing bugs
- **The Ultimate Game Boy Talk** - Excellent overview talk: search for "The Ultimate Game Boy Talk" on YouTube
- **Game Boy CPU Manual** - Detailed register and instruction documentation
- **dmg-acid2** - PPU accuracy test ROM

---

*This analysis was generated by reviewing every source file and test file in the repository.*
