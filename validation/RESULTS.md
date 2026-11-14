# Held-out test of lmreadout 0.5.0: results

## Qwen3.5-0.8B (primary, 12 tasks)

### 15 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.094 (0.001) | 0.484 (0.014) | 0.083 (0.013) | 0.257 (0.043) | 0.484 (0.014) | 20 |
| `law_exam` | 4 | 0.250 | 0.265 (0.001) | 0.296 (0.013) | 0.255 (0.013) | 0.265 (0.014) | 0.278 (0.016) | 4 |
| `legal_support` | 2 | 0.500 | 0.497 (0.000) | 0.483 (0.005) | 0.502 (0.012) | 0.499 (0.023) | 0.491 (0.014) | 0 |
| `german_argument` | 4 | 0.250 | 0.264 (0.000) | 0.239 (0.025) | 0.313 (0.042) | 0.324 (0.033) | 0.239 (0.025) | 20 |
| `acceptability` | 2 | 0.500 | 0.502 (0.000) | 0.528 (0.006) | 0.504 (0.017) | 0.524 (0.024) | 0.519 (0.021) | 1 |
| `nli` | 3 | 0.333 | 0.340 (0.000) | 0.417 (0.009) | 0.337 (0.015) | 0.440 (0.030) | 0.422 (0.033) | 2 |
| `stance` | 2 | 0.500 | 0.479 (0.002) | 0.477 (0.009) | 0.510 (0.017) | 0.533 (0.017) | 0.505 (0.026) | 0 |
| `paraphrase` | 2 | 0.500 | 0.500 (0.000) | 0.525 (0.006) | 0.501 (0.013) | 0.600 (0.042) | 0.559 (0.053) | 0 |
| `word_sense` | 2 | 0.500 | 0.500 (0.000) | 0.483 (0.005) | 0.511 (0.020) | 0.506 (0.024) | 0.497 (0.020) | 0 |
| `request_domain` | 11 | 0.091 | 0.438 (0.001) | 0.803 (0.021) | 0.234 (0.034) | 0.631 (0.066) | 0.803 (0.021) | 20 |
| `citation_intent` | 3 | 0.333 | 0.340 (0.000) | 0.524 (0.015) | 0.416 (0.054) | 0.460 (0.063) | 0.515 (0.042) | 8 |
| `wiki_category` | 14 | 0.071 | 0.192 (0.001) | 0.501 (0.015) | 0.239 (0.037) | 0.441 (0.069) | 0.501 (0.015) | 20 |
| **Mean over tasks with a result** | | | **0.367** | **0.480** | **0.367** | **0.457** | **0.484** | |

- `--auto` against As shipped: above on 9, below on 3, level on 0 of 12 tasks.
- `--auto` against Calibration only: above on 5, below on 3, level on 4 of 12 tasks.
- `--auto` against Word counts: above on 8, below on 4, level on 0 of 12 tasks.
- `--auto` against Fixed edit: above on 5, below on 7, level on 0 of 12 tasks.

### 30 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.094 (0.001) | 0.491 (0.010) | 0.103 (0.017) | 0.315 (0.036) | 0.491 (0.010) | 20 |
| `law_exam` | 4 | 0.250 | 0.265 (0.001) | 0.297 (0.011) | 0.253 (0.012) | 0.278 (0.011) | 0.280 (0.016) | 0 |
| `legal_support` | 2 | 0.500 | 0.497 (0.000) | 0.484 (0.006) | 0.505 (0.016) | 0.498 (0.019) | 0.498 (0.018) | 0 |
| `german_argument` | 4 | 0.250 | 0.264 (0.001) | 0.238 (0.012) | 0.323 (0.053) | 0.343 (0.031) | 0.245 (0.035) | 19 |
| `acceptability` | 2 | 0.500 | 0.502 (0.000) | 0.526 (0.007) | 0.510 (0.012) | 0.528 (0.023) | 0.522 (0.022) | 0 |
| `nli` | 3 | 0.333 | 0.340 (0.000) | 0.419 (0.008) | 0.343 (0.014) | 0.478 (0.029) | 0.452 (0.037) | 0 |
| `stance` | 2 | 0.500 | 0.480 (0.002) | 0.478 (0.006) | 0.511 (0.016) | 0.564 (0.033) | 0.535 (0.047) | 0 |
| `paraphrase` | 2 | 0.500 | 0.500 (0.000) | 0.524 (0.004) | 0.508 (0.014) | 0.633 (0.036) | 0.611 (0.049) | 0 |
| `word_sense` | 2 | 0.500 | 0.500 (0.000) | 0.482 (0.009) | 0.508 (0.029) | 0.511 (0.023) | 0.496 (0.018) | 0 |
| `request_domain` | 11 | 0.091 | 0.437 (0.002) | 0.814 (0.015) | 0.364 (0.047) | 0.774 (0.053) | 0.814 (0.015) | 20 |
| `citation_intent` | 3 | 0.333 | 0.339 (0.001) | 0.537 (0.011) | 0.468 (0.030) | 0.496 (0.048) | 0.527 (0.040) | 1 |
| `wiki_category` | 14 | 0.071 | 0.193 (0.002) | 0.515 (0.011) | 0.382 (0.047) | 0.575 (0.067) | 0.515 (0.011) | 20 |
| **Mean over tasks with a result** | | | **0.368** | **0.484** | **0.398** | **0.499** | **0.499** | |

- `--auto` against As shipped: above on 10, below on 2, level on 0 of 12 tasks.
- `--auto` against Calibration only: above on 6, below on 3, level on 3 of 12 tasks.
- `--auto` against Word counts: above on 9, below on 3, level on 0 of 12 tasks.
- `--auto` against Fixed edit: above on 4, below on 8, level on 0 of 12 tasks.

### 60 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.093 (0.002) | 0.491 (0.006) | 0.139 (0.017) | 0.384 (0.031) | 0.491 (0.006) | 20 |
| `law_exam` | 4 | 0.250 | 0.265 (0.003) | 0.294 (0.008) | 0.255 (0.013) | 0.279 (0.015) | 0.287 (0.017) | 0 |
| `legal_support` | 2 | 0.500 | 0.497 (0.000) | 0.485 (0.005) | 0.500 (0.015) | 0.503 (0.019) | 0.499 (0.016) | 0 |
| `german_argument` | 4 | 0.250 | 0.264 (0.001) | 0.240 (0.010) | 0.341 (0.038) | 0.378 (0.026) | 0.317 (0.073) | 8 |
| `acceptability` | 2 | 0.500 | 0.502 (0.000) | 0.526 (0.007) | 0.512 (0.015) | 0.537 (0.021) | 0.535 (0.023) | 0 |
| `nli` | 3 | 0.333 | 0.340 (0.001) | 0.421 (0.007) | 0.351 (0.019) | 0.512 (0.018) | 0.508 (0.015) | 0 |
| `stance` | 2 | 0.500 | 0.478 (0.004) | 0.474 (0.006) | 0.532 (0.021) | 0.617 (0.027) | 0.605 (0.032) | 0 |
| `paraphrase` | 2 | 0.500 | 0.500 (0.000) | 0.524 (0.009) | 0.505 (0.013) | 0.685 (0.022) | 0.679 (0.027) | 0 |
| `word_sense` | 2 | 0.500 | 0.500 (0.000) | 0.477 (0.008) | 0.523 (0.016) | 0.518 (0.025) | 0.508 (0.025) | 0 |
| `request_domain` | 11 | 0.091 | 0.437 (0.003) | 0.815 (0.010) | 0.569 (0.056) | 0.854 (0.030) | 0.851 (0.032) | 8 |
| `citation_intent` | 3 | 0.333 | 0.340 (0.001) | 0.541 (0.009) | 0.512 (0.046) | 0.554 (0.036) | 0.563 (0.025) | 0 |
| `wiki_category` | 14 | 0.071 | 0.192 (0.002) | 0.517 (0.010) | 0.552 (0.033) | 0.708 (0.032) | 0.596 (0.096) | 11 |
| **Mean over tasks with a result** | | | **0.367** | **0.484** | **0.441** | **0.544** | **0.537** | |

- `--auto` against As shipped: above on 12, below on 0, level on 0 of 12 tasks.
- `--auto` against Calibration only: above on 10, below on 1, level on 1 of 12 tasks.
- `--auto` against Word counts: above on 9, below on 3, level on 0 of 12 tasks.
- `--auto` against Fixed edit: above on 3, below on 9, level on 0 of 12 tasks.

### 120 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.094 (0.003) | 0.494 (0.008) | 0.192 (0.021) | 0.430 (0.023) | 0.494 (0.008) | 16 |
| `law_exam` | 4 | 0.250 | 0.265 (0.004) | 0.293 (0.008) | 0.253 (0.012) | 0.285 (0.012) | 0.285 (0.016) | 0 |
| `legal_support` | 2 | 0.500 | 0.497 (0.001) | 0.484 (0.005) | 0.505 (0.013) | 0.525 (0.020) | 0.511 (0.016) | 0 |
| `german_argument` | 4 | 0.250 | 0.264 (0.001) | 0.244 (0.008) | 0.376 (0.056) | 0.411 (0.031) | 0.396 (0.079) | 3 |
| `acceptability` | 2 | 0.500 | 0.502 (0.001) | 0.526 (0.011) | 0.515 (0.012) | 0.556 (0.020) | 0.543 (0.027) | 0 |
| `nli` | 3 | 0.333 | 0.340 (0.001) | 0.419 (0.006) | 0.342 (0.014) | 0.549 (0.023) | 0.541 (0.024) | 0 |
| `stance` | 2 | 0.500 | 0.479 (0.005) | 0.478 (0.008) | 0.569 (0.019) | 0.691 (0.023) | 0.687 (0.031) | 0 |
| `paraphrase` | 2 | 0.500 | 0.500 (0.000) | 0.522 (0.007) | 0.508 (0.016) | 0.723 (0.018) | 0.720 (0.022) | 0 |
| `word_sense` | 2 | 0.500 | 0.500 (0.000) | 0.481 (0.014) | 0.535 (0.023) | 0.532 (0.016) | 0.518 (0.027) | 0 |
| `request_domain` | 11 | 0.091 | 0.439 (0.004) | 0.817 (0.010) | 0.697 (0.030) | 0.898 (0.021) | 0.897 (0.023) | 1 |
| `citation_intent` | 3 | 0.333 | 0.340 (0.001) | 0.540 (0.007) | 0.550 (0.038) | 0.597 (0.030) | 0.602 (0.026) | 0 |
| `wiki_category` | 14 | 0.071 | 0.193 (0.002) | 0.516 (0.008) | 0.689 (0.030) | 0.808 (0.027) | 0.806 (0.025) | 0 |
| **Mean over tasks with a result** | | | **0.368** | **0.484** | **0.477** | **0.584** | **0.583** | |

- `--auto` against As shipped: above on 12, below on 0, level on 0 of 12 tasks.
- `--auto` against Calibration only: above on 10, below on 1, level on 1 of 12 tasks.
- `--auto` against Word counts: above on 11, below on 1, level on 0 of 12 tasks.
- `--auto` against Fixed edit: above on 2, below on 10, level on 0 of 12 tasks.

### Settings `--auto` chose (count over the 20 draws)

- `law_topic`, 15: fallback (lean only): 20
- `law_topic`, 30: fallback (lean only): 20
- `law_topic`, 60: fallback (lean only): 20
- `law_topic`, 120: fallback (lean only): 16; lean 1, no read-out: 4
- `law_exam`, 15: unchanged: 4; fallback (lean only): 4; lean 1, no read-out: 4; lean 0.5, no read-out: 3; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 1n: 1
- `law_exam`, 30: lean 1, no read-out: 4; lean 0 strength 1 ridge 1n: 3; lean 1 strength 0.5 ridge 1n: 3; lean 0 strength 2 ridge 1n: 3; lean 0 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 0.5, no read-out: 2; lean 0 strength 4 ridge 1n: 1
- `law_exam`, 60: lean 1, no read-out: 5; lean 1 strength 1 ridge 4n: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1
- `law_exam`, 120: lean 1, no read-out: 4; lean 0.5 strength 1 ridge 4n: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1
- `legal_support`, 15: lean 1, no read-out: 5; unchanged: 3; lean 1 strength 2 ridge 1n: 3; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1
- `legal_support`, 30: lean 1 strength 2 ridge 1n: 3; lean 0.5, no read-out: 3; lean 0 strength 4 ridge 1n: 2; lean 1, no read-out: 2; lean 1 strength 1 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; unchanged: 1
- `legal_support`, 60: lean 1, no read-out: 4; lean 0.5, no read-out: 3; unchanged: 2; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1
- `legal_support`, 120: lean 1 strength 1 ridge 0.25n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; unchanged: 1; lean 1 strength 2 ridge 0.25n: 1
- `german_argument`, 15: fallback (lean only): 20
- `german_argument`, 30: fallback (lean only): 19; lean 0 strength 2 ridge 4n: 1
- `german_argument`, 60: fallback (lean only): 8; lean 0 strength 2 ridge 4n: 2; lean 0 strength 1 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1, no read-out: 1; lean 1 strength 1 ridge 1n: 1
- `german_argument`, 120: lean 0 strength 2 ridge 4n: 4; fallback (lean only): 3; lean 0 strength 4 ridge 4n: 2; lean 0 strength 1 ridge 1n: 2; lean 0 strength 1 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `acceptability`, 15: unchanged: 6; lean 1 strength 0.5 ridge 1n: 4; lean 1 strength 4 ridge 1n: 3; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; fallback (lean only): 1; lean 0.5 strength 2 ridge 1n: 1; lean 1, no read-out: 1
- `acceptability`, 30: lean 1, no read-out: 10; unchanged: 3; lean 1 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1
- `acceptability`, 60: lean 1 strength 1 ridge 0.25n: 5; lean 1, no read-out: 3; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 2 ridge 4n: 2; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `acceptability`, 120: lean 1 strength 1 ridge 0.25n: 2; lean 1, no read-out: 2; lean 1 strength 4 ridge 4n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 0 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; unchanged: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1
- `nli`, 15: lean 1, no read-out: 5; lean 1 strength 2 ridge 1n: 4; fallback (lean only): 2; lean 1 strength 0.5 ridge 1n: 2; lean 0 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 0.25n: 1; unchanged: 1
- `nli`, 30: lean 1, no read-out: 4; lean 0.5 strength 4 ridge 1n: 3; lean 0.5 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 2; lean 0.5, no read-out: 2; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1
- `nli`, 60: lean 0.5 strength 4 ridge 1n: 6; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 1 ridge 4n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1
- `nli`, 120: lean 1 strength 1 ridge 0.25n: 3; lean 0 strength 4 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1
- `stance`, 15: lean 1 strength 1 ridge 1n: 3; unchanged: 3; lean 0.5 strength 0.5 ridge 1n: 2; lean 0.5, no read-out: 2; lean 0 strength 0.5 ridge 1n: 2; lean 1, no read-out: 2; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1
- `stance`, 30: lean 1 strength 2 ridge 1n: 3; lean 1 strength 4 ridge 1n: 3; unchanged: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1, no read-out: 2; lean 0 strength 1 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1
- `stance`, 60: lean 1 strength 2 ridge 0.25n: 4; lean 0 strength 2 ridge 4n: 3; lean 0.5 strength 4 ridge 0.25n: 2; lean 1 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1
- `stance`, 120: lean 1 strength 4 ridge 0.25n: 5; lean 0 strength 2 ridge 1n: 3; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1
- `paraphrase`, 15: unchanged: 4; lean 1, no read-out: 4; lean 1 strength 4 ridge 1n: 4; lean 1 strength 0.5 ridge 1n: 3; lean 1 strength 2 ridge 1n: 3; lean 1 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1
- `paraphrase`, 30: lean 1 strength 0.5 ridge 1n: 4; lean 1 strength 4 ridge 1n: 4; lean 1 strength 2 ridge 1n: 4; lean 1 strength 0.5 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 1 ridge 1n: 1; lean 1, no read-out: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `paraphrase`, 60: lean 1 strength 2 ridge 1n: 7; lean 1 strength 4 ridge 4n: 3; lean 1 strength 1 ridge 4n: 3; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1
- `paraphrase`, 120: lean 1 strength 2 ridge 4n: 6; lean 1 strength 4 ridge 4n: 5; lean 1 strength 1 ridge 1n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1
- `word_sense`, 15: unchanged: 4; lean 1 strength 0.5 ridge 1n: 4; lean 1, no read-out: 3; lean 1 strength 2 ridge 1n: 3; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 4n: 2; lean 1 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1
- `word_sense`, 30: lean 1, no read-out: 5; unchanged: 3; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1
- `word_sense`, 60: lean 1 strength 1 ridge 1n: 2; lean 1, no read-out: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; unchanged: 1; lean 0 strength 4 ridge 4n: 1
- `word_sense`, 120: lean 0.5 strength 4 ridge 4n: 3; lean 1 strength 1 ridge 4n: 3; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1
- `request_domain`, 15: fallback (lean only): 20
- `request_domain`, 30: fallback (lean only): 20
- `request_domain`, 60: fallback (lean only): 8; lean 1 strength 0.5 ridge 1n: 4; lean 1 strength 1 ridge 4n: 2; lean 0.5 strength 1 ridge 1n: 2; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1
- `request_domain`, 120: lean 1 strength 1 ridge 1n: 4; lean 1 strength 1 ridge 4n: 3; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; fallback (lean only): 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1
- `citation_intent`, 15: fallback (lean only): 8; lean 1, no read-out: 4; lean 1 strength 1 ridge 1n: 4; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1
- `citation_intent`, 30: lean 1, no read-out: 6; lean 1 strength 1 ridge 1n: 5; lean 1 strength 0.5 ridge 1n: 4; lean 1 strength 2 ridge 1n: 1; fallback (lean only): 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1
- `citation_intent`, 60: lean 1, no read-out: 4; lean 1 strength 0.5 ridge 1n: 4; lean 1 strength 1 ridge 1n: 3; lean 1 strength 2 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1
- `citation_intent`, 120: lean 1 strength 0.5 ridge 1n: 3; lean 1 strength 2 ridge 0.25n: 3; lean 1 strength 0.5 ridge 0.25n: 3; lean 1 strength 0.5 ridge 4n: 3; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1
- `wiki_category`, 15: fallback (lean only): 20
- `wiki_category`, 30: fallback (lean only): 20
- `wiki_category`, 60: fallback (lean only): 11; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 1 ridge 1n: 1; lean 1, no read-out: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1
- `wiki_category`, 120: lean 1 strength 1 ridge 0.25n: 4; lean 1 strength 1 ridge 4n: 4; lean 1 strength 2 ridge 1n: 3; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1

### The three rules

**Rule 1 (no real harm at 15): FAIL.** `--auto` minus as shipped, per task:
- `law_topic`: +0.391
- `law_exam`: +0.014
- `legal_support`: -0.006
- `german_argument`: -0.025  <- more than 0.02 below
- `acceptability`: +0.017
- `nli`: +0.083
- `stance`: +0.026
- `paraphrase`: +0.059
- `word_sense`: -0.003
- `request_domain`: +0.365
- `citation_intent`: +0.175
- `wiki_category`: +0.309

**Rule 2 (matches the fixed edit at 120): FAIL.** `--auto` minus fixed edit, per task:
- `law_topic`: +0.064
- `law_exam`: -0.000
- `legal_support`: -0.015  <- more than 0.005 below
- `german_argument`: -0.015  <- more than 0.005 below
- `acceptability`: -0.013  <- more than 0.005 below
- `nli`: -0.008  <- more than 0.005 below
- `stance`: -0.003
- `paraphrase`: -0.003
- `word_sense`: -0.014  <- more than 0.005 below
- `request_domain`: -0.000
- `citation_intent`: +0.005
- `wiki_category`: -0.002

**Rule 3 (level with the better safe choice at 15): PASS.** Mean over 12 tasks of `--auto` minus the better of as shipped and calibration only: -0.0004. Per task:
- `law_topic`: +0.000
- `law_exam`: -0.018
- `legal_support`: -0.006
- `german_argument`: -0.025
- `acceptability`: -0.009
- `nli`: +0.005
- `stance`: +0.026
- `paraphrase`: +0.034
- `word_sense`: -0.003
- `request_domain`: +0.000
- `citation_intent`: -0.009
- `wiki_category`: +0.000

### Extra view, not a rule: without the tasks where `--auto` fell back in at least 10 of 20 draws of 15 (`law_topic`, `german_argument`, `request_domain`, `wiki_category`)

- Rule 1 quantity, worst task: -0.006 (`legal_support`).
- Rule 3 quantity, mean over 8 tasks: +0.0025.
- Fallback tasks only, Rule 3 quantity, mean over 4 tasks: -0.0062.


## Phi-4-mini (secondary, 4 tasks)

### 15 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.475 (0.002) | 0.518 (0.010) | 0.083 (0.013) | 0.281 (0.045) | 0.518 (0.010) | 20 |
| `legal_support` | 2 | 0.500 | 0.503 (0.001) | 0.561 (0.009) | 0.502 (0.012) | 0.535 (0.020) | 0.542 (0.021) | 0 |
| `acceptability` | 2 | 0.500 | 0.770 (0.002) | 0.763 (0.019) | 0.504 (0.017) | 0.699 (0.059) | 0.749 (0.037) | 1 |
| `request_domain` | 11 | 0.091 | 0.889 (0.001) | 0.883 (0.029) | 0.234 (0.034) | 0.678 (0.070) | 0.883 (0.029) | 20 |
| **Mean over tasks with a result** | | | **0.659** | **0.681** | **0.331** | **0.548** | **0.673** | |

- `--auto` against As shipped: above on 2, below on 2, level on 0 of 4 tasks.
- `--auto` against Calibration only: above on 0, below on 2, level on 2 of 4 tasks.
- `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- `--auto` against Fixed edit: above on 4, below on 0, level on 0 of 4 tasks.

### 30 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.476 (0.002) | 0.529 (0.008) | 0.103 (0.017) | 0.354 (0.047) | 0.529 (0.008) | 20 |
| `legal_support` | 2 | 0.500 | 0.502 (0.001) | 0.565 (0.006) | 0.505 (0.016) | 0.541 (0.018) | 0.539 (0.025) | 0 |
| `acceptability` | 2 | 0.500 | 0.770 (0.002) | 0.762 (0.009) | 0.510 (0.012) | 0.725 (0.047) | 0.760 (0.028) | 0 |
| `request_domain` | 11 | 0.091 | 0.889 (0.002) | 0.895 (0.010) | 0.364 (0.047) | 0.851 (0.055) | 0.895 (0.010) | 20 |
| **Mean over tasks with a result** | | | **0.659** | **0.688** | **0.371** | **0.618** | **0.681** | |

- `--auto` against As shipped: above on 3, below on 1, level on 0 of 4 tasks.
- `--auto` against Calibration only: above on 0, below on 2, level on 2 of 4 tasks.
- `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- `--auto` against Fixed edit: above on 3, below on 1, level on 0 of 4 tasks.

### 60 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.475 (0.004) | 0.531 (0.006) | 0.139 (0.017) | 0.439 (0.032) | 0.531 (0.006) | 20 |
| `legal_support` | 2 | 0.500 | 0.502 (0.001) | 0.566 (0.005) | 0.500 (0.015) | 0.537 (0.020) | 0.542 (0.020) | 0 |
| `acceptability` | 2 | 0.500 | 0.770 (0.004) | 0.763 (0.004) | 0.512 (0.015) | 0.741 (0.025) | 0.767 (0.020) | 0 |
| `request_domain` | 11 | 0.091 | 0.890 (0.003) | 0.901 (0.008) | 0.569 (0.056) | 0.916 (0.030) | 0.919 (0.018) | 8 |
| **Mean over tasks with a result** | | | **0.659** | **0.690** | **0.430** | **0.658** | **0.690** | |

- `--auto` against As shipped: above on 3, below on 1, level on 0 of 4 tasks.
- `--auto` against Calibration only: above on 2, below on 1, level on 1 of 4 tasks.
- `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- `--auto` against Fixed edit: above on 4, below on 0, level on 0 of 4 tasks.

### 120 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | `--auto` | Fallback draws of 20 |
|---|---|---|---|---|---|---|---|---|
| `law_topic` | 16 | 0.062 | 0.475 (0.006) | 0.534 (0.008) | 0.192 (0.021) | 0.484 (0.020) | 0.533 (0.007) | 16 |
| `legal_support` | 2 | 0.500 | 0.503 (0.002) | 0.563 (0.008) | 0.505 (0.013) | 0.565 (0.023) | 0.566 (0.021) | 0 |
| `acceptability` | 2 | 0.500 | 0.771 (0.005) | 0.765 (0.006) | 0.515 (0.012) | 0.747 (0.013) | 0.770 (0.014) | 0 |
| `request_domain` | 11 | 0.091 | 0.890 (0.004) | 0.902 (0.009) | 0.697 (0.030) | 0.946 (0.009) | 0.937 (0.022) | 1 |
| **Mean over tasks with a result** | | | **0.660** | **0.691** | **0.477** | **0.685** | **0.701** | |

- `--auto` against As shipped: above on 3, below on 1, level on 0 of 4 tasks.
- `--auto` against Calibration only: above on 3, below on 1, level on 0 of 4 tasks.
- `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- `--auto` against Fixed edit: above on 3, below on 1, level on 0 of 4 tasks.

### Settings `--auto` chose (count over the 20 draws)

- `law_topic`, 15: fallback (lean only): 20
- `law_topic`, 30: fallback (lean only): 20
- `law_topic`, 60: fallback (lean only): 20
- `law_topic`, 120: fallback (lean only): 16; lean 1, no read-out: 3; lean 0.5, no read-out: 1
- `legal_support`, 15: lean 1, no read-out: 7; lean 1 strength 4 ridge 1n: 3; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 0.5 ridge 1n: 2; unchanged: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1
- `legal_support`, 30: lean 0 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1, no read-out: 2; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; unchanged: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1
- `legal_support`, 60: lean 1 strength 4 ridge 4n: 3; lean 1, no read-out: 3; lean 1 strength 1 ridge 1n: 2; lean 0.5, no read-out: 2; lean 0.5 strength 4 ridge 1n: 2; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1
- `legal_support`, 120: lean 0 strength 4 ridge 0.25n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 0 strength 4 ridge 1n: 2; lean 1, no read-out: 2; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1
- `acceptability`, 15: unchanged: 8; lean 1 strength 1 ridge 1n: 4; lean 1, no read-out: 3; lean 0.5, no read-out: 1; fallback (lean only): 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1
- `acceptability`, 30: unchanged: 5; lean 1, no read-out: 4; lean 0.5, no read-out: 3; lean 1 strength 1 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1
- `acceptability`, 60: lean 0.5, no read-out: 6; unchanged: 3; lean 1, no read-out: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1
- `acceptability`, 120: lean 1 strength 0.5 ridge 4n: 5; lean 1 strength 0.5 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 2; lean 0.5, no read-out: 2; lean 0.5 strength 1 ridge 4n: 1; unchanged: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1
- `request_domain`, 15: fallback (lean only): 20
- `request_domain`, 30: fallback (lean only): 20
- `request_domain`, 60: fallback (lean only): 8; lean 1 strength 1 ridge 1n: 3; lean 0.5, no read-out: 2; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1, no read-out: 1
- `request_domain`, 120: lean 1 strength 1 ridge 1n: 4; lean 0.5 strength 0.5 ridge 4n: 2; unchanged: 2; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; fallback (lean only): 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1, no read-out: 1; lean 0.5, no read-out: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1

### The three rules

**Rule 1 (no real harm at 15): FAIL.** `--auto` minus as shipped, per task:
- `law_topic`: +0.044
- `legal_support`: +0.039
- `acceptability`: -0.022  <- more than 0.02 below
- `request_domain`: -0.006

**Rule 2 (matches the fixed edit at 120): FAIL.** `--auto` minus fixed edit, per task:
- `law_topic`: +0.049
- `legal_support`: +0.002
- `acceptability`: +0.023
- `request_domain`: -0.010  <- more than 0.005 below

**Rule 3 (level with the better safe choice at 15): FAIL.** Mean over 4 tasks of `--auto` minus the better of as shipped and calibration only: -0.0119. Per task:
- `law_topic`: +0.000
- `legal_support`: -0.019
- `acceptability`: -0.022
- `request_domain`: -0.006

### Extra view, not a rule: without the tasks where `--auto` fell back in at least 10 of 20 draws of 15 (`law_topic`, `request_domain`)

- Rule 1 quantity, worst task: -0.022 (`acceptability`).
- Rule 3 quantity, mean over 2 tasks: -0.0205.
- Fallback tasks only, Rule 3 quantity, mean over 2 tasks: -0.0032.

