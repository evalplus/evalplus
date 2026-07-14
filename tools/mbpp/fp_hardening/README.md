# MBPP+ FP-hardening subset

A small selection of existing MBPP+ *plus* tests — 76-123 tests,
~0.2-0.3% of the plus tier's 39,841 total tests — that catches 55-63% of
the pooled verified-wrong programs which pass the MBPP *base* tests
("false positives"). The selection method itself reaches 0.80-0.95
coverage on held-out model families with per-rotation suites of 182-343
tests (~0.5-0.9% of the plus tier; see paper).

Paper (audit methodology, full tables, per-cell validation records):
https://arxiv.org/abs/2607.11022

## Contents

`suite.py` embeds three preregistered per-task budgets and can dump each as
JSON (this repo gitignores `*.json`, so the data lives in the module):

| budget k | tasks | tests | dump command |
|---|---|---|---|
| 1 | 76 | 76 | `python suite.py --dump 1` |
| 2 (suggested default) | 93 | 107 | `python suite.py --dump 2` |
| 4 | 99 | 123 | `python suite.py --dump 4` |

Each suite maps `task_id -> [indices into that task's plus_input]` for
**MBPP+ v0.2.0** (the version pinned by `MBPP_PLUS_VERSION` in
`evalplus/data/mbpp.py`). The indices are positions in the deserialized
`plus_input` list as returned by `get_mbpp_plus()`. Any future dataset
version that reorders or edits `plus_input` invalidates these indices.

## What the numbers mean

- Selection: greedy weighted set cover (same family of technique as this
  repo's `tools/_experimental/set_cover.py`) over a 5,702 x 12,412 kill
  matrix of verified-wrong false-positive programs (base-pass, plus-fail,
  artifact-filtered) from RLVR training runs of three small model families
  (Qwen2.5-Coder-1.5B-Instruct, deepseek-coder-1.3b-instruct,
  Llama-3.2-1B-Instruct), always selecting on two families and scoring on
  the held-out third.
- Held-out coverage of the unseen family's FP signatures: 0.80-0.95,
  measured on the per-rotation suites (182-343 tests each;
  leave-one-family-out, all three rotations and all three budgets reported
  with task-clustered bootstrap CIs; see the paper for the full table). The
  shipped suites are the cross-family intersection of those rotations and
  carry no held-out measurement of their own; re-executed against the full
  pooled FP set they cover 0.55-0.63 (per-family 0.52-0.67) — the only
  measured coverage of the shipped files themselves.
- Three budgets (k=1/2/4) were preregistered and are all shipped; no budget
  was selected post hoc on results. k=2 is suggested purely as a
  size/coverage knee (k=2 -> k=4 adds 16 tests to the shipped
  intersection; the 1.0-1.8pt held-out gain is measured on the
  per-rotation suites, where k=2 -> k=4 adds 32-45 tests).
- Every (program, selected-test) cell was re-executed against live
  evalplus 0.3.1 on Linux: 5,867 cells, 1 disagreement (0.017%, a
  PYTHONHASHSEED-order flake on Mbpp/602), and zero cases of the stored
  matrix under-counting kills (the single disagreement is one over-credited
  kill, in the direction that slightly overstates the suite).

## Scope and limitations

- This is a *hardening* subset for base-test-only scoring loops (e.g. cheap
  RL reward signals). It is **not** a verdict-preserving reduction of MBPP+
  and does not replace the full suite for evaluation or leaderboards.
- Coverage is measured against false positives produced by small instruction
  models under RLVR-style sampling; coverage against other model classes is
  not claimed.
- Construction and validation ran on Linux. evalplus 0.3.1's default-config
  `import resource` path makes Windows return ('timeout', []) for every
  program, so re-validation must be done on Linux (reported separately as an
  environment issue).

## Provenance

The dumps reproduce the paper's frozen audit artifacts exactly up to
newline normalization: `--dump` emits LF bytes deterministically (raw
stdout, or written verbatim via `--output PATH`). The hashes below can be
reproduced with a POSIX shell pipe, or by hashing an `--output` file on
any platform. Note that Windows PowerShell pipes and `>` redirection
re-encode the stream (LF -> CRLF, plus BOM/UTF-16 depending on console
settings) and will not match — use `--output` there. The frozen
artifacts' own sha256 are recorded in the paper repo.

```
$ python suite.py --dump 1 | sha256sum
3001c8f0e09542ddb7eb52c9bed793fee0694a651f79768875b4cf8391c6a54e
$ python suite.py --dump 2 | sha256sum
26abe911a10d0c3a98d8deb3895dd4c7dfd45cee1d1f68f9169e9de6345e4404
$ python suite.py --dump 4 | sha256sum
ed772c967d01ddc4955b7e9932de0ad3b01f1a406588fc291684e98f74d40a2d
```

On Windows (PowerShell):

```
> python suite.py --dump 2 --output suite_k2.json
> Get-FileHash suite_k2.json -Algorithm SHA256   # same values as above
```
