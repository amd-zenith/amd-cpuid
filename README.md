# AMD CPUID

[![Build](https://github.com/amd-zenith/amd-cpuid/actions/workflows/build.yml/badge.svg)](https://github.com/amd-zenith/amd-cpuid/actions/workflows/build.yml)
[![CodeQL](https://github.com/amd-zenith/amd-cpuid/actions/workflows/codeql.yml/badge.svg)](https://github.com/amd-zenith/amd-cpuid/actions/workflows/codeql.yml)
[![PyPI version](https://img.shields.io/pypi/v/amd-cpuid.svg)](https://pypi.org/project/amd-cpuid/)
[![Python versions](https://img.shields.io/pypi/pyversions/amd-cpuid.svg)](https://pypi.org/project/amd-cpuid/)
[![Snyk package health](https://img.shields.io/badge/Snyk-package%20health-4C4A73?logo=snyk&logoColor=white)](https://snyk.io/advisor/python/amd-cpuid)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/amd-zenith/amd-cpuid/badge)](https://scorecard.dev/viewer/?uri=github.com/amd-zenith/amd-cpuid)


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
