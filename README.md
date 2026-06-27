# AMD CPUID

A very small Python library and CLI for parsing, interpreting and converting between the different ways AMD encodes processor identity (CPUID).

## Representations

AMD exposes the same processor identity using different representations.

| Representation              | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| **CPUID instruction**       | The 32-bit signature returned by the `CPUID` instruction.  |
| **Microcode header**        | The packed `cpuid` field of an AMD microcode patch header. |
| **Family, Model, Stepping** | The human-facing family / model / stepping numbers.        |

For AMD Zen the base family is always `0xF`, so the *display family* is `0xF + extended_family`, and the *model* is `extended_model << 4 | model`.

## Installation

```bash
pip install amd-cpuid
```
