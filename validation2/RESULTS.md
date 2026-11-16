# Second held-out test: lmreadout 0.6.0 beside 0.5.0, results

## Qwen3.5-0.8B (primary, 12 tasks)

Check: the largest difference between the two runs in any column that does not depend on `--auto` (as shipped, calibration only, word counts, fixed edit) is 0.0000.

### 15 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.504 (0.000) | 0.549 (0.010) | 0.549 (0.030) | 0.612 (0.061) | 0.616 (0.049) | 0.607 (0.044) | -0.009 | 0 |
| `housing_law` | 2 | 0.500 | 0.500 (0.000) | 0.453 (0.012) | 0.536 (0.035) | 0.518 (0.026) | 0.508 (0.025) | 0.491 (0.028) | -0.017 | 0 |
| `contract_type` | 15 | 0.067 | 0.183 (0.001) | 0.459 (0.012) | 0.214 (0.042) | 0.276 (0.056) | 0.459 (0.012) | 0.450 (0.066) | -0.008 | 20 |
| `language_id` | 20 | 0.050 | 0.205 (0.001) | 0.679 (0.019) | 0.115 (0.030) | 0.470 (0.050) | 0.679 (0.019) | 0.733 (0.049) | +0.054 | 20 |
| `patent_section` | 9 | 0.111 | 0.111 (0.000) | 0.227 (0.011) | 0.133 (0.016) | 0.271 (0.039) | 0.227 (0.011) | 0.246 (0.026) | +0.019 | 20 |
| `abstract_role` | 5 | 0.200 | 0.200 (0.000) | 0.285 (0.006) | 0.252 (0.032) | 0.304 (0.045) | 0.280 (0.019) | 0.300 (0.023) | +0.020 | 19 |
| `fed_stance` | 3 | 0.333 | 0.333 (0.000) | 0.404 (0.010) | 0.346 (0.018) | 0.379 (0.025) | 0.380 (0.030) | 0.395 (0.024) | +0.014 | 4 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.000) | 0.298 (0.007) | 0.258 (0.015) | 0.273 (0.016) | 0.291 (0.017) | 0.284 (0.023) | -0.007 | 13 |
| `hate_speech` | 2 | 0.500 | 0.534 (0.001) | 0.535 (0.005) | 0.518 (0.020) | 0.560 (0.040) | 0.554 (0.029) | 0.557 (0.022) | +0.003 | 0 |
| `counterfactual` | 2 | 0.500 | 0.501 (0.000) | 0.517 (0.009) | 0.536 (0.040) | 0.525 (0.037) | 0.513 (0.025) | 0.523 (0.025) | +0.010 | 6 |
| `appeal_outcome` | 2 | 0.500 | 0.519 (0.002) | 0.508 (0.007) | 0.515 (0.020) | 0.521 (0.021) | 0.526 (0.018) | 0.517 (0.017) | -0.009 | 0 |
| `fair_reason` | 2 | 0.500 | 0.500 (0.000) | 0.537 (0.004) | 0.495 (0.012) | 0.514 (0.010) | 0.516 (0.013) | 0.530 (0.012) | +0.014 | 0 |
| **Mean over tasks with a result** | | | **0.362** | **0.454** | **0.372** | **0.435** | **0.462** | **0.469** | **+0.0069** | |

- 0.6.0 `--auto` against As shipped: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 8, below on 4, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 5, below on 7, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### 30 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.504 (0.000) | 0.545 (0.008) | 0.583 (0.037) | 0.656 (0.037) | 0.653 (0.050) | 0.647 (0.044) | -0.006 | 0 |
| `housing_law` | 2 | 0.500 | 0.500 (0.000) | 0.461 (0.005) | 0.559 (0.032) | 0.527 (0.021) | 0.507 (0.029) | 0.502 (0.019) | -0.005 | 0 |
| `contract_type` | 15 | 0.067 | 0.183 (0.002) | 0.455 (0.011) | 0.256 (0.035) | 0.348 (0.045) | 0.455 (0.011) | 0.485 (0.035) | +0.031 | 20 |
| `language_id` | 20 | 0.050 | 0.205 (0.002) | 0.693 (0.017) | 0.236 (0.036) | 0.673 (0.056) | 0.693 (0.017) | 0.783 (0.046) | +0.090 | 20 |
| `patent_section` | 9 | 0.111 | 0.111 (0.000) | 0.235 (0.007) | 0.156 (0.017) | 0.315 (0.026) | 0.235 (0.007) | 0.305 (0.027) | +0.070 | 20 |
| `abstract_role` | 5 | 0.200 | 0.200 (0.000) | 0.285 (0.007) | 0.302 (0.035) | 0.355 (0.028) | 0.304 (0.034) | 0.351 (0.016) | +0.048 | 13 |
| `fed_stance` | 3 | 0.333 | 0.333 (0.000) | 0.402 (0.011) | 0.349 (0.016) | 0.390 (0.025) | 0.382 (0.031) | 0.410 (0.024) | +0.028 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.000) | 0.301 (0.011) | 0.259 (0.014) | 0.279 (0.020) | 0.295 (0.016) | 0.290 (0.018) | -0.005 | 7 |
| `hate_speech` | 2 | 0.500 | 0.534 (0.002) | 0.534 (0.005) | 0.530 (0.021) | 0.619 (0.037) | 0.607 (0.044) | 0.612 (0.032) | +0.005 | 0 |
| `counterfactual` | 2 | 0.500 | 0.501 (0.000) | 0.518 (0.008) | 0.520 (0.037) | 0.517 (0.028) | 0.542 (0.035) | 0.535 (0.035) | -0.006 | 5 |
| `appeal_outcome` | 2 | 0.500 | 0.519 (0.002) | 0.509 (0.005) | 0.528 (0.024) | 0.533 (0.021) | 0.531 (0.017) | 0.526 (0.015) | -0.005 | 0 |
| `fair_reason` | 2 | 0.500 | 0.500 (0.000) | 0.535 (0.007) | 0.495 (0.012) | 0.514 (0.015) | 0.522 (0.015) | 0.525 (0.013) | +0.003 | 0 |
| **Mean over tasks with a result** | | | **0.362** | **0.456** | **0.398** | **0.477** | **0.477** | **0.498** | **+0.0205** | |

- 0.6.0 `--auto` against As shipped: above on 12, below on 0, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 6, below on 6, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### 60 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.504 (0.000) | 0.546 (0.007) | 0.611 (0.043) | 0.687 (0.046) | 0.706 (0.039) | 0.701 (0.046) | -0.004 | 0 |
| `housing_law` | 2 | 0.500 | 0.500 (0.000) | 0.461 (0.008) | 0.619 (0.034) | 0.570 (0.024) | 0.570 (0.027) | 0.566 (0.026) | -0.005 | 0 |
| `contract_type` | 15 | 0.067 | 0.183 (0.003) | 0.456 (0.012) | 0.343 (0.033) | 0.441 (0.041) | 0.456 (0.012) | 0.510 (0.041) | +0.054 | 20 |
| `language_id` | 20 | 0.050 | 0.206 (0.003) | 0.698 (0.010) | 0.437 (0.044) | 0.832 (0.046) | 0.698 (0.010) | 0.857 (0.033) | +0.159 | 20 |
| `patent_section` | 9 | 0.111 | 0.111 (0.000) | 0.231 (0.007) | 0.177 (0.023) | 0.353 (0.023) | 0.241 (0.034) | 0.347 (0.031) | +0.106 | 18 |
| `abstract_role` | 5 | 0.200 | 0.200 (0.000) | 0.284 (0.005) | 0.354 (0.033) | 0.396 (0.027) | 0.383 (0.042) | 0.398 (0.021) | +0.015 | 2 |
| `fed_stance` | 3 | 0.333 | 0.333 (0.000) | 0.405 (0.011) | 0.385 (0.023) | 0.410 (0.030) | 0.400 (0.026) | 0.410 (0.029) | +0.010 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.000) | 0.301 (0.006) | 0.271 (0.014) | 0.289 (0.014) | 0.283 (0.020) | 0.294 (0.017) | +0.011 | 1 |
| `hate_speech` | 2 | 0.500 | 0.535 (0.003) | 0.533 (0.005) | 0.551 (0.019) | 0.687 (0.039) | 0.690 (0.037) | 0.693 (0.036) | +0.003 | 0 |
| `counterfactual` | 2 | 0.500 | 0.501 (0.000) | 0.517 (0.013) | 0.526 (0.037) | 0.523 (0.024) | 0.573 (0.048) | 0.546 (0.038) | -0.027 | 1 |
| `appeal_outcome` | 2 | 0.500 | 0.519 (0.004) | 0.504 (0.005) | 0.546 (0.024) | 0.531 (0.023) | 0.531 (0.023) | 0.531 (0.023) | +0.001 | 0 |
| `fair_reason` | 2 | 0.500 | 0.500 (0.000) | 0.539 (0.004) | 0.495 (0.013) | 0.508 (0.015) | 0.515 (0.018) | 0.520 (0.017) | +0.005 | 0 |
| **Mean over tasks with a result** | | | **0.362** | **0.456** | **0.443** | **0.519** | **0.504** | **0.531** | **+0.0273** | |

- 0.6.0 `--auto` against As shipped: above on 12, below on 0, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 9, below on 3, level on 0 of 12 tasks.

### 120 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.504 (0.000) | 0.544 (0.008) | 0.653 (0.029) | 0.722 (0.023) | 0.748 (0.018) | 0.739 (0.022) | -0.008 | 0 |
| `housing_law` | 2 | 0.500 | 0.500 (0.000) | 0.460 (0.009) | 0.652 (0.025) | 0.613 (0.025) | 0.609 (0.048) | 0.616 (0.028) | +0.007 | 0 |
| `contract_type` | 15 | 0.067 | 0.184 (0.004) | 0.455 (0.013) | 0.419 (0.041) | 0.538 (0.043) | 0.502 (0.073) | 0.585 (0.034) | +0.083 | 14 |
| `language_id` | 20 | 0.050 | 0.206 (0.003) | 0.702 (0.007) | 0.623 (0.041) | 0.948 (0.020) | 0.900 (0.102) | 0.948 (0.020) | +0.047 | 4 |
| `patent_section` | 9 | 0.111 | 0.111 (0.000) | 0.233 (0.008) | 0.216 (0.018) | 0.385 (0.019) | 0.308 (0.084) | 0.391 (0.021) | +0.083 | 11 |
| `abstract_role` | 5 | 0.200 | 0.200 (0.000) | 0.281 (0.008) | 0.387 (0.021) | 0.440 (0.030) | 0.436 (0.030) | 0.437 (0.030) | +0.001 | 0 |
| `fed_stance` | 3 | 0.333 | 0.333 (0.000) | 0.406 (0.014) | 0.402 (0.019) | 0.435 (0.024) | 0.420 (0.025) | 0.434 (0.022) | +0.013 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.000) | 0.303 (0.006) | 0.277 (0.015) | 0.298 (0.019) | 0.300 (0.016) | 0.299 (0.017) | -0.001 | 0 |
| `hate_speech` | 2 | 0.500 | 0.534 (0.006) | 0.531 (0.007) | 0.587 (0.022) | 0.785 (0.029) | 0.784 (0.029) | 0.786 (0.029) | +0.002 | 0 |
| `counterfactual` | 2 | 0.500 | 0.501 (0.000) | 0.525 (0.017) | 0.534 (0.032) | 0.531 (0.021) | 0.587 (0.042) | 0.566 (0.052) | -0.021 | 0 |
| `appeal_outcome` | 2 | 0.500 | 0.518 (0.004) | 0.501 (0.005) | 0.563 (0.014) | 0.550 (0.017) | 0.543 (0.016) | 0.540 (0.019) | -0.003 | 0 |
| `fair_reason` | 2 | 0.500 | 0.500 (0.000) | 0.540 (0.004) | 0.489 (0.014) | 0.493 (0.016) | 0.505 (0.018) | 0.504 (0.020) | -0.001 | 0 |
| **Mean over tasks with a result** | | | **0.362** | **0.457** | **0.484** | **0.562** | **0.553** | **0.570** | **+0.0168** | |

- 0.6.0 `--auto` against As shipped: above on 12, below on 0, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 10, below on 2, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 8, below on 4, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### Settings 0.6.0 `--auto` chose (count over the 20 draws)

- `unfair_clause`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 1 strength 2 ridge 0.25n: 2; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `unfair_clause`, 30: lean 1 strength 0.5 ridge 1n: 9; lean 1 strength 4 ridge 0.25n: 3; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 0.25 ridge 0.25n: 1
- `unfair_clause`, 60: lean 1 strength 1 ridge 1n: 6; lean 0.5 strength 4 ridge 4n: 3; lean 0.5 strength 1 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `unfair_clause`, 120: lean 1 strength 2 ridge 1n: 6; lean 0 strength 4 ridge 4n: 4; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 1 strength 2 ridge 4n: 2; lean 0 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1
- `housing_law`, 15: lean 1 strength 0.25 ridge 1n: 11; lean 0.5 strength 4 ridge 0.25n: 3; lean 1 strength 1 ridge 0.25n: 2; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1
- `housing_law`, 30: lean 1 strength 0.5 ridge 1n: 12; lean 0.5 strength 1 ridge 4n: 2; lean 0.5, no read-out: 2; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1
- `housing_law`, 60: lean 1 strength 1 ridge 1n: 9; lean 1 strength 4 ridge 0.25n: 4; lean 0 strength 4 ridge 0.25n: 2; lean 0.5 strength 4 ridge 0.25n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1
- `housing_law`, 120: lean 1 strength 2 ridge 1n: 9; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 4n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1
- `contract_type`, 15: lean 1 strength 0.25 ridge 1n: 12; lean 1 strength 1 ridge 0.25n: 3; lean 1 strength 0.5 ridge 4n: 2; lean 1, no read-out: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `contract_type`, 30: lean 1 strength 0.5 ridge 1n: 16; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 0.25 ridge 0.25n: 1; lean 1, no read-out: 1
- `contract_type`, 60: lean 1 strength 1 ridge 1n: 7; lean 1 strength 0.25 ridge 4n: 4; lean 1, no read-out: 3; lean 1 strength 0.25 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 0.25 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1
- `contract_type`, 120: lean 1 strength 0.5 ridge 1n: 5; lean 1 strength 0.25 ridge 0.25n: 4; lean 1 strength 0.25 ridge 4n: 4; lean 1 strength 0.5 ridge 0.25n: 3; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 0.25 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1
- `language_id`, 15: lean 1 strength 0.25 ridge 1n: 18; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `language_id`, 30: lean 1 strength 0.5 ridge 1n: 14; lean 1 strength 0.25 ridge 4n: 2; lean 1 strength 0.25 ridge 0.25n: 2; lean 1, no read-out: 2
- `language_id`, 60: lean 1 strength 1 ridge 1n: 9; lean 1 strength 0.25 ridge 0.25n: 4; lean 1 strength 0.5 ridge 0.25n: 3; lean 0.5 strength 0.5 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.25 ridge 4n: 1
- `language_id`, 120: lean 1 strength 2 ridge 1n: 10; lean 1 strength 1 ridge 0.25n: 4; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `patent_section`, 15: lean 1 strength 0.25 ridge 1n: 13; lean 1, no read-out: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `patent_section`, 30: lean 1 strength 0.5 ridge 1n: 9; lean 1 strength 2 ridge 0.25n: 3; lean 0.5 strength 4 ridge 0.25n: 2; lean 1 strength 0.25 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `patent_section`, 60: lean 1 strength 1 ridge 1n: 11; lean 1 strength 0.5 ridge 4n: 3; lean 1 strength 0.25 ridge 4n: 2; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1
- `patent_section`, 120: lean 1 strength 2 ridge 1n: 6; lean 1 strength 4 ridge 4n: 4; lean 1 strength 1 ridge 4n: 4; lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1
- `abstract_role`, 15: lean 1 strength 0.25 ridge 1n: 15; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `abstract_role`, 30: lean 1 strength 0.5 ridge 1n: 13; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1
- `abstract_role`, 60: lean 1 strength 1 ridge 1n: 13; lean 0.5 strength 4 ridge 4n: 3; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `abstract_role`, 120: lean 1 strength 2 ridge 1n: 6; lean 1 strength 1 ridge 4n: 3; lean 0.5 strength 2 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `fed_stance`, 15: lean 1 strength 0.25 ridge 1n: 15; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1
- `fed_stance`, 30: lean 1 strength 0.5 ridge 1n: 13; lean 1 strength 0.25 ridge 0.25n: 3; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1
- `fed_stance`, 60: lean 1 strength 1 ridge 1n: 11; lean 1, no read-out: 3; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1
- `fed_stance`, 120: lean 1 strength 2 ridge 1n: 11; lean 1 strength 2 ridge 4n: 3; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 0.25 ridge 0.25n: 1
- `climate_claim`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 1 strength 0.5 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1
- `climate_claim`, 30: lean 1 strength 0.5 ridge 1n: 11; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1
- `climate_claim`, 60: lean 1 strength 1 ridge 1n: 10; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 0.25 ridge 1n: 1; lean 1 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1, no read-out: 1; lean 1 strength 0.25 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1
- `climate_claim`, 120: lean 1 strength 2 ridge 1n: 6; lean 1, no read-out: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 1 ridge 4n: 2; lean 1 strength 0.25 ridge 0.25n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1
- `hate_speech`, 15: lean 1 strength 0.25 ridge 1n: 10; unchanged: 3; lean 1 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1
- `hate_speech`, 30: lean 1 strength 0.5 ridge 1n: 6; lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 1 ridge 0.25n: 2; lean 0 strength 4 ridge 0.25n: 2; unchanged: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1
- `hate_speech`, 60: lean 1 strength 1 ridge 1n: 6; lean 0 strength 1 ridge 1n: 3; lean 0 strength 2 ridge 1n: 3; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1
- `hate_speech`, 120: lean 1 strength 2 ridge 1n: 8; lean 0.5 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 0.25n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 1 strength 4 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1
- `counterfactual`, 15: lean 1 strength 0.25 ridge 1n: 11; lean 0 strength 4 ridge 4n: 4; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1, no read-out: 1; lean 1 strength 1 ridge 4n: 1
- `counterfactual`, 30: lean 1 strength 0.5 ridge 1n: 15; lean 0 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1
- `counterfactual`, 60: lean 1 strength 1 ridge 1n: 13; lean 0.5 strength 0.25 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1
- `counterfactual`, 120: lean 1 strength 2 ridge 1n: 8; lean 0 strength 1 ridge 4n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 0 strength 1 ridge 1n: 2; lean 1 strength 0.25 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1
- `appeal_outcome`, 15: lean 1 strength 0.25 ridge 1n: 12; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 4n: 1; lean 1, no read-out: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `appeal_outcome`, 30: lean 1 strength 0.5 ridge 1n: 5; unchanged: 4; lean 0.5, no read-out: 2; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 0.25 ridge 4n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1
- `appeal_outcome`, 60: lean 1 strength 1 ridge 1n: 6; lean 0 strength 0.5 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5, no read-out: 1; lean 1 strength 0.25 ridge 4n: 1
- `appeal_outcome`, 120: lean 1 strength 2 ridge 1n: 6; unchanged: 3; lean 1 strength 0.5 ridge 4n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0.5 strength 0.25 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `fair_reason`, 15: lean 1 strength 0.25 ridge 1n: 14; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1
- `fair_reason`, 30: lean 1 strength 0.5 ridge 1n: 8; lean 1, no read-out: 7; lean 1 strength 4 ridge 0.25n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1
- `fair_reason`, 60: lean 1 strength 1 ridge 1n: 8; lean 1, no read-out: 6; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1
- `fair_reason`, 120: lean 1 strength 2 ridge 1n: 7; lean 1, no read-out: 4; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 1 ridge 0.25n: 1

### Settings 0.5.0 `--auto` chose (count over the 20 draws)

- `unfair_clause`, 15: lean 1 strength 2 ridge 1n: 6; lean 1 strength 0.5 ridge 1n: 3; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0.5 strength 1 ridge 1n: 2; lean 0 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `unfair_clause`, 30: lean 1 strength 4 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1, no read-out: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1
- `unfair_clause`, 60: lean 0.5 strength 1 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 3; lean 0.5 strength 2 ridge 4n: 3; lean 1 strength 1 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `unfair_clause`, 120: lean 0 strength 4 ridge 4n: 5; lean 0.5 strength 4 ridge 4n: 3; lean 0.5 strength 2 ridge 4n: 3; lean 0 strength 2 ridge 4n: 3; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1
- `housing_law`, 15: lean 0.5 strength 2 ridge 1n: 3; lean 0.5 strength 4 ridge 1n: 3; lean 1 strength 2 ridge 1n: 3; unchanged: 2; lean 1 strength 1 ridge 1n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 1, no read-out: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1
- `housing_law`, 30: lean 1, no read-out: 3; lean 1 strength 1 ridge 1n: 3; lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 1n: 2; unchanged: 2; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1
- `housing_law`, 60: lean 1 strength 4 ridge 0.25n: 3; lean 0.5 strength 4 ridge 0.25n: 3; lean 1 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 1n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1
- `housing_law`, 120: lean 1 strength 4 ridge 0.25n: 3; lean 0.5 strength 4 ridge 4n: 3; lean 0.5 strength 4 ridge 0.25n: 2; lean 1 strength 1 ridge 4n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 1, no read-out: 1
- `contract_type`, 15: fallback (lean only): 20
- `contract_type`, 30: fallback (lean only): 20
- `contract_type`, 60: fallback (lean only): 20
- `contract_type`, 120: fallback (lean only): 14; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 0.5 ridge 0.25n: 2
- `language_id`, 15: fallback (lean only): 20
- `language_id`, 30: fallback (lean only): 20
- `language_id`, 60: fallback (lean only): 20
- `language_id`, 120: lean 1 strength 1 ridge 1n: 5; fallback (lean only): 4; lean 1 strength 1 ridge 0.25n: 3; lean 1 strength 2 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1
- `patent_section`, 15: fallback (lean only): 20
- `patent_section`, 30: fallback (lean only): 20
- `patent_section`, 60: fallback (lean only): 18; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1
- `patent_section`, 120: fallback (lean only): 11; lean 1 strength 4 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1
- `abstract_role`, 15: fallback (lean only): 19; unchanged: 1
- `abstract_role`, 30: fallback (lean only): 13; lean 1 strength 1 ridge 1n: 3; lean 0.5 strength 4 ridge 1n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1, no read-out: 1
- `abstract_role`, 60: lean 0.5 strength 4 ridge 4n: 4; lean 1 strength 1 ridge 1n: 3; fallback (lean only): 2; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `abstract_role`, 120: lean 1 strength 1 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 3; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `fed_stance`, 15: fallback (lean only): 4; lean 1 strength 0.5 ridge 1n: 3; lean 1 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 4n: 2; lean 1, no read-out: 2; lean 1 strength 1 ridge 1n: 1; unchanged: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1
- `fed_stance`, 30: lean 1, no read-out: 9; lean 0.5, no read-out: 3; lean 0 strength 2 ridge 0.25n: 2; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1
- `fed_stance`, 60: lean 1, no read-out: 6; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1
- `fed_stance`, 120: lean 1, no read-out: 3; lean 1 strength 2 ridge 4n: 3; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1
- `climate_claim`, 15: fallback (lean only): 13; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0.5 strength 2 ridge 4n: 1; unchanged: 1; lean 1 strength 0.5 ridge 1n: 1
- `climate_claim`, 30: fallback (lean only): 7; lean 1 strength 1 ridge 1n: 3; lean 1, no read-out: 3; lean 1 strength 4 ridge 1n: 2; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1
- `climate_claim`, 60: lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1, no read-out: 2; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; unchanged: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; fallback (lean only): 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1
- `climate_claim`, 120: lean 1 strength 1 ridge 4n: 4; lean 1, no read-out: 3; lean 1 strength 0.5 ridge 4n: 3; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1
- `hate_speech`, 15: unchanged: 7; lean 1 strength 1 ridge 1n: 3; lean 0 strength 0.5 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 1, no read-out: 2; lean 0.5, no read-out: 1; lean 0 strength 1 ridge 1n: 1
- `hate_speech`, 30: lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 1 ridge 1n: 2; unchanged: 2; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0 strength 2 ridge 1n: 1
- `hate_speech`, 60: lean 1 strength 4 ridge 0.25n: 4; lean 0.5 strength 2 ridge 0.25n: 2; lean 0 strength 1 ridge 1n: 2; lean 0 strength 2 ridge 1n: 2; lean 0.5 strength 1 ridge 4n: 2; lean 0 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1
- `hate_speech`, 120: lean 0.5 strength 4 ridge 1n: 3; lean 1 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 0.25n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `counterfactual`, 15: fallback (lean only): 6; lean 1, no read-out: 5; unchanged: 4; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1
- `counterfactual`, 30: fallback (lean only): 5; lean 1, no read-out: 2; lean 0 strength 2 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1
- `counterfactual`, 60: lean 0 strength 1 ridge 4n: 3; lean 0 strength 4 ridge 1n: 2; lean 0 strength 2 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 2; lean 0.5 strength 1 ridge 1n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1, no read-out: 1; fallback (lean only): 1
- `counterfactual`, 120: lean 0 strength 1 ridge 1n: 3; lean 0 strength 1 ridge 4n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 0 strength 2 ridge 1n: 2; lean 0 strength 1 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1
- `appeal_outcome`, 15: unchanged: 6; lean 1 strength 2 ridge 1n: 5; lean 0 strength 2 ridge 1n: 3; lean 1 strength 1 ridge 1n: 2; lean 1 strength 4 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1, no read-out: 1
- `appeal_outcome`, 30: lean 1 strength 1 ridge 1n: 4; unchanged: 3; lean 0.5 strength 1 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1
- `appeal_outcome`, 60: lean 1 strength 0.5 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 2; lean 0 strength 2 ridge 4n: 2; lean 0 strength 0.5 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5, no read-out: 1; lean 1, no read-out: 1
- `appeal_outcome`, 120: lean 0.5 strength 2 ridge 1n: 3; lean 0 strength 4 ridge 4n: 2; lean 0.5 strength 1 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1
- `fair_reason`, 15: lean 1, no read-out: 4; lean 1 strength 0.5 ridge 1n: 3; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; unchanged: 2; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 1 ridge 1n: 1
- `fair_reason`, 30: lean 1, no read-out: 8; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1; unchanged: 1
- `fair_reason`, 60: lean 1, no read-out: 7; lean 0.5 strength 0.5 ridge 1n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1
- `fair_reason`, 120: lean 1, no read-out: 4; lean 0.5 strength 1 ridge 0.25n: 2; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5 strength 1 ridge 1n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 4 ridge 4n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1

### The four rules (0.6.0)

**Rule 1 (no real harm at 15), 0.6.0: PASS.** `--auto` minus as shipped, per task:
- `unfair_clause`: +0.103
- `housing_law`: -0.009
- `contract_type`: +0.267
- `language_id`: +0.528
- `patent_section`: +0.135
- `abstract_role`: +0.100
- `fed_stance`: +0.061
- `climate_claim`: +0.035
- `hate_speech`: +0.023
- `counterfactual`: +0.022
- `appeal_outcome`: -0.002
- `fair_reason`: +0.030

**Rule 2 (matches the fixed edit at 120), 0.6.0: FAIL.** `--auto` minus fixed edit, per task:
- `unfair_clause`: +0.018
- `housing_law`: +0.003
- `contract_type`: +0.047
- `language_id`: -0.000
- `patent_section`: +0.006
- `abstract_role`: -0.003
- `fed_stance`: -0.001
- `climate_claim`: +0.001
- `hate_speech`: +0.001
- `counterfactual`: +0.034
- `appeal_outcome`: -0.009  <- more than 0.005 below
- `fair_reason`: +0.010

**Rule 3 (level with the better safe choice at 15), 0.6.0: PASS.** Mean over 12 tasks of `--auto` minus the better of as shipped and calibration only: +0.0103. Per task:
- `unfair_clause`: +0.058
- `housing_law`: -0.009
- `contract_type`: -0.008
- `language_id`: +0.054
- `patent_section`: +0.019
- `abstract_role`: +0.015
- `fed_stance`: -0.009
- `climate_claim`: -0.014
- `hate_speech`: +0.022
- `counterfactual`: +0.006
- `appeal_outcome`: -0.002
- `fair_reason`: -0.007

**Rule 4 (not worse than 0.5.0):** mean over tasks of 0.6.0's `--auto` minus 0.5.0's `--auto`:
- 15 examples: +0.0069 over 12 tasks (0.6.0 above on 7, below on 5)
- 30 examples: +0.0205 over 12 tasks (0.6.0 above on 7, below on 5)
- 60 examples: +0.0273 over 12 tasks (0.6.0 above on 9, below on 3)
- 120 examples: +0.0168 over 12 tasks (0.6.0 above on 7, below on 5)

**Rule 4: PASS.**

### For comparison: Rules 1 to 3 applied to 0.5.0's `--auto` on the same tasks

**Rule 1 (no real harm at 15), 0.5.0: PASS.** `--auto` minus as shipped, per task:
- `unfair_clause`: +0.112
- `housing_law`: +0.008
- `contract_type`: +0.275
- `language_id`: +0.474
- `patent_section`: +0.116
- `abstract_role`: +0.080
- `fed_stance`: +0.047
- `climate_claim`: +0.042
- `hate_speech`: +0.020
- `counterfactual`: +0.012
- `appeal_outcome`: +0.007
- `fair_reason`: +0.016

**Rule 2 (matches the fixed edit at 120), 0.5.0: FAIL.** `--auto` minus fixed edit, per task:
- `unfair_clause`: +0.026
- `housing_law`: -0.004
- `contract_type`: -0.036  <- more than 0.005 below
- `language_id`: -0.047  <- more than 0.005 below
- `patent_section`: -0.077  <- more than 0.005 below
- `abstract_role`: -0.004
- `fed_stance`: -0.015  <- more than 0.005 below
- `climate_claim`: +0.001
- `hate_speech`: -0.001
- `counterfactual`: +0.056
- `appeal_outcome`: -0.007  <- more than 0.005 below
- `fair_reason`: +0.012

**Rule 3 (level with the better safe choice at 15), 0.5.0: PASS.** Mean over 12 tasks of `--auto` minus the better of as shipped and calibration only: +0.0034. Per task:
- `unfair_clause`: +0.067
- `housing_law`: +0.008
- `contract_type`: +0.000
- `language_id`: +0.000
- `patent_section`: +0.000
- `abstract_role`: -0.005
- `fed_stance`: -0.024
- `climate_claim`: -0.007
- `hate_speech`: +0.019
- `counterfactual`: -0.005
- `appeal_outcome`: +0.007
- `fair_reason`: -0.020


## Phi-4-mini (secondary, 4 tasks)

Check: the largest difference between the two runs in any column that does not depend on `--auto` (as shipped, calibration only, word counts, fixed edit) is 0.0000.

### 15 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `housing_law` | 2 | 0.500 | 0.524 (0.001) | 0.536 (0.008) | 0.536 (0.035) | 0.593 (0.035) | 0.588 (0.038) | 0.578 (0.031) | -0.010 | 0 |
| `contract_type` | 15 | 0.067 | 0.205 (0.002) | 0.353 (0.009) | 0.214 (0.042) | 0.252 (0.050) | 0.353 (0.009) | 0.330 (0.096) | -0.023 | 20 |
| `hate_speech` | 2 | 0.500 | 0.827 (0.002) | 0.839 (0.022) | 0.518 (0.020) | 0.824 (0.047) | 0.836 (0.028) | 0.832 (0.011) | -0.004 | 0 |
| `climate_claim` | 4 | 0.250 | 0.368 (0.001) | 0.325 (0.024) | 0.258 (0.015) | 0.317 (0.035) | 0.334 (0.032) | 0.342 (0.031) | +0.009 | 13 |
| **Mean over tasks with a result** | | | **0.481** | **0.513** | **0.382** | **0.496** | **0.528** | **0.520** | **-0.0072** | |

- 0.6.0 `--auto` against As shipped: above on 3, below on 1, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Calibration only: above on 2, below on 2, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 3, below on 1, level on 0 of 4 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 1, below on 3, level on 0 of 4 tasks.

### 30 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `housing_law` | 2 | 0.500 | 0.524 (0.001) | 0.533 (0.007) | 0.559 (0.032) | 0.617 (0.032) | 0.589 (0.046) | 0.580 (0.046) | -0.010 | 0 |
| `contract_type` | 15 | 0.067 | 0.206 (0.003) | 0.354 (0.007) | 0.256 (0.035) | 0.325 (0.048) | 0.354 (0.007) | 0.415 (0.072) | +0.061 | 20 |
| `hate_speech` | 2 | 0.500 | 0.827 (0.003) | 0.852 (0.009) | 0.530 (0.021) | 0.874 (0.036) | 0.863 (0.036) | 0.853 (0.033) | -0.009 | 0 |
| `climate_claim` | 4 | 0.250 | 0.368 (0.002) | 0.322 (0.020) | 0.259 (0.014) | 0.359 (0.026) | 0.354 (0.032) | 0.371 (0.015) | +0.018 | 7 |
| **Mean over tasks with a result** | | | **0.481** | **0.515** | **0.401** | **0.544** | **0.540** | **0.555** | **+0.0149** | |

- 0.6.0 `--auto` against As shipped: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Calibration only: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 2, below on 2, level on 0 of 4 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 2, below on 2, level on 0 of 4 tasks.

### 60 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `housing_law` | 2 | 0.500 | 0.523 (0.001) | 0.537 (0.007) | 0.619 (0.034) | 0.642 (0.035) | 0.631 (0.054) | 0.623 (0.058) | -0.008 | 0 |
| `contract_type` | 15 | 0.067 | 0.205 (0.003) | 0.356 (0.007) | 0.343 (0.033) | 0.439 (0.037) | 0.356 (0.007) | 0.514 (0.033) | +0.158 | 20 |
| `hate_speech` | 2 | 0.500 | 0.829 (0.003) | 0.853 (0.006) | 0.551 (0.019) | 0.891 (0.019) | 0.885 (0.024) | 0.889 (0.021) | +0.003 | 0 |
| `climate_claim` | 4 | 0.250 | 0.368 (0.002) | 0.317 (0.010) | 0.271 (0.014) | 0.355 (0.021) | 0.358 (0.026) | 0.369 (0.016) | +0.011 | 1 |
| **Mean over tasks with a result** | | | **0.481** | **0.516** | **0.446** | **0.582** | **0.558** | **0.599** | **+0.0411** | |

- 0.6.0 `--auto` against As shipped: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Calibration only: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 2, below on 2, level on 0 of 4 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 3, below on 1, level on 0 of 4 tasks.

### 120 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `housing_law` | 2 | 0.500 | 0.523 (0.002) | 0.531 (0.008) | 0.652 (0.025) | 0.690 (0.017) | 0.687 (0.019) | 0.689 (0.018) | +0.002 | 0 |
| `contract_type` | 15 | 0.067 | 0.204 (0.005) | 0.357 (0.006) | 0.419 (0.041) | 0.540 (0.044) | 0.433 (0.116) | 0.572 (0.037) | +0.138 | 14 |
| `hate_speech` | 2 | 0.500 | 0.828 (0.006) | 0.857 (0.008) | 0.587 (0.022) | 0.933 (0.013) | 0.926 (0.022) | 0.927 (0.021) | +0.001 | 0 |
| `climate_claim` | 4 | 0.250 | 0.368 (0.003) | 0.322 (0.011) | 0.277 (0.015) | 0.365 (0.021) | 0.379 (0.023) | 0.383 (0.014) | +0.005 | 0 |
| **Mean over tasks with a result** | | | **0.481** | **0.517** | **0.484** | **0.632** | **0.606** | **0.643** | **+0.0366** | |

- 0.6.0 `--auto` against As shipped: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Calibration only: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Word counts: above on 4, below on 0, level on 0 of 4 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 2, below on 2, level on 0 of 4 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 4, below on 0, level on 0 of 4 tasks.

### Settings 0.6.0 `--auto` chose (count over the 20 draws)

- `housing_law`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 1 strength 1 ridge 0.25n: 3; lean 0 strength 1 ridge 4n: 2; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; unchanged: 1; lean 0.5 strength 0.25 ridge 4n: 1
- `housing_law`, 30: lean 1 strength 0.25 ridge 1n: 8; unchanged: 4; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `housing_law`, 60: lean 1 strength 0.5 ridge 1n: 4; unchanged: 3; lean 0 strength 2 ridge 4n: 3; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1
- `housing_law`, 120: lean 1 strength 1 ridge 1n: 7; lean 1 strength 1 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1
- `contract_type`, 15: lean 1 strength 0.25 ridge 1n: 9; unchanged: 4; lean 0.5 strength 0.5 ridge 0.25n: 2; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 0.25 ridge 4n: 1
- `contract_type`, 30: lean 1 strength 0.25 ridge 1n: 11; lean 1 strength 0.5 ridge 0.25n: 4; lean 1 strength 1 ridge 0.25n: 2; unchanged: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 0 strength 0.25 ridge 0.25n: 1
- `contract_type`, 60: lean 1 strength 0.5 ridge 1n: 17; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 0.25 ridge 1n: 1
- `contract_type`, 120: lean 1 strength 1 ridge 1n: 7; lean 1 strength 0.5 ridge 0.25n: 3; lean 1 strength 0.5 ridge 4n: 3; lean 1 strength 0.25 ridge 0.25n: 2; lean 1 strength 0.25 ridge 4n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 1
- `hate_speech`, 15: unchanged: 16; lean 1 strength 0.25 ridge 1n: 3; lean 0.5, no read-out: 1
- `hate_speech`, 30: unchanged: 11; lean 1 strength 0.25 ridge 1n: 5; lean 1 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 1n: 1
- `hate_speech`, 60: lean 1 strength 0.5 ridge 1n: 9; lean 1 strength 2 ridge 0.25n: 3; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1, no read-out: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.25 ridge 0.25n: 1; unchanged: 1
- `hate_speech`, 120: lean 1 strength 1 ridge 1n: 11; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 0.5, no read-out: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1
- `climate_claim`, 15: lean 1 strength 0.25 ridge 1n: 11; unchanged: 6; lean 0 strength 1 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 0.25 ridge 0.25n: 1
- `climate_claim`, 30: unchanged: 9; lean 1 strength 0.25 ridge 1n: 5; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5, no read-out: 1
- `climate_claim`, 60: unchanged: 12; lean 1 strength 0.5 ridge 1n: 3; lean 1 strength 1 ridge 4n: 2; lean 0 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 0.5 ridge 0.25n: 1
- `climate_claim`, 120: lean 1 strength 1 ridge 1n: 4; lean 0.5 strength 0.25 ridge 4n: 3; lean 0.5, no read-out: 2; unchanged: 2; lean 0 strength 0.5 ridge 1n: 2; lean 1 strength 0.25 ridge 1n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 4 ridge 4n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 0 strength 0.25 ridge 1n: 1

### Settings 0.5.0 `--auto` chose (count over the 20 draws)

- `housing_law`, 15: lean 1 strength 1 ridge 1n: 6; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1
- `housing_law`, 30: lean 1, no read-out: 4; lean 0.5 strength 2 ridge 1n: 3; lean 0 strength 1 ridge 4n: 2; unchanged: 2; lean 0.5 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1
- `housing_law`, 60: lean 0 strength 2 ridge 0.25n: 3; lean 0 strength 2 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1, no read-out: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; unchanged: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1
- `housing_law`, 120: lean 1 strength 1 ridge 4n: 3; lean 0.5 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 0 strength 1 ridge 4n: 2; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1
- `contract_type`, 15: fallback (lean only): 20
- `contract_type`, 30: fallback (lean only): 20
- `contract_type`, 60: fallback (lean only): 20
- `contract_type`, 120: fallback (lean only): 14; lean 1 strength 0.5 ridge 1n: 5; lean 1 strength 0.5 ridge 4n: 1
- `hate_speech`, 15: unchanged: 8; lean 1 strength 1 ridge 1n: 5; lean 1, no read-out: 4; lean 1 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 0.5 ridge 1n: 1
- `hate_speech`, 30: lean 1 strength 1 ridge 1n: 6; unchanged: 4; lean 0.5, no read-out: 2; lean 1 strength 4 ridge 4n: 1; lean 1, no read-out: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1
- `hate_speech`, 60: lean 1, no read-out: 4; lean 0.5 strength 1 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1 strength 1 ridge 4n: 2; lean 0 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1
- `hate_speech`, 120: lean 1 strength 2 ridge 1n: 3; lean 1 strength 1 ridge 1n: 3; lean 1 strength 4 ridge 0.25n: 3; lean 0 strength 1 ridge 0.25n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1
- `climate_claim`, 15: fallback (lean only): 13; lean 0.5, no read-out: 3; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; unchanged: 1
- `climate_claim`, 30: fallback (lean only): 7; lean 0.5, no read-out: 4; unchanged: 2; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1
- `climate_claim`, 60: lean 1, no read-out: 4; unchanged: 4; lean 0.5, no read-out: 3; lean 0 strength 0.5 ridge 0.25n: 2; lean 1 strength 1 ridge 4n: 2; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; fallback (lean only): 1
- `climate_claim`, 120: lean 0 strength 1 ridge 4n: 4; lean 0.5, no read-out: 3; lean 1 strength 0.5 ridge 4n: 3; lean 0 strength 0.5 ridge 4n: 2; lean 0 strength 0.5 ridge 1n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1

### The four rules (0.6.0)

**Rule 1 (no real harm at 15), 0.6.0: FAIL.** `--auto` minus as shipped, per task:
- `housing_law`: +0.054
- `contract_type`: +0.126
- `hate_speech`: +0.005
- `climate_claim`: -0.026  <- more than 0.02 below

**Rule 2 (matches the fixed edit at 120), 0.6.0: FAIL.** `--auto` minus fixed edit, per task:
- `housing_law`: -0.001
- `contract_type`: +0.031
- `hate_speech`: -0.006  <- more than 0.005 below
- `climate_claim`: +0.018

**Rule 3 (level with the better safe choice at 15), 0.6.0: PASS.** Mean over 4 tasks of `--auto` minus the better of as shipped and calibration only: -0.0035. Per task:
- `housing_law`: +0.042
- `contract_type`: -0.023
- `hate_speech`: -0.007
- `climate_claim`: -0.026

**Rule 4 (not worse than 0.5.0):** mean over tasks of 0.6.0's `--auto` minus 0.5.0's `--auto`:
- 15 examples: -0.0072 over 4 tasks (0.6.0 above on 1, below on 3)  <- below 0
- 30 examples: +0.0149 over 4 tasks (0.6.0 above on 2, below on 2)
- 60 examples: +0.0411 over 4 tasks (0.6.0 above on 3, below on 1)
- 120 examples: +0.0366 over 4 tasks (0.6.0 above on 4, below on 0)

**Rule 4: FAIL.**

### For comparison: Rules 1 to 3 applied to 0.5.0's `--auto` on the same tasks

**Rule 1 (no real harm at 15), 0.5.0: FAIL.** `--auto` minus as shipped, per task:
- `housing_law`: +0.064
- `contract_type`: +0.149
- `hate_speech`: +0.009
- `climate_claim`: -0.034  <- more than 0.02 below

**Rule 2 (matches the fixed edit at 120), 0.5.0: FAIL.** `--auto` minus fixed edit, per task:
- `housing_law`: -0.003
- `contract_type`: -0.107  <- more than 0.005 below
- `hate_speech`: -0.007  <- more than 0.005 below
- `climate_claim`: +0.013

**Rule 3 (level with the better safe choice at 15), 0.5.0: PASS.** Mean over 4 tasks of `--auto` minus the better of as shipped and calibration only: +0.0038. Per task:
- `housing_law`: +0.052
- `contract_type`: +0.000
- `hate_speech`: -0.003
- `climate_claim`: -0.034


## LFM2-1.2B (third model, added later on the owner's request, 12 tasks)

Check: the largest difference between the two runs in any column that does not depend on `--auto` (as shipped, calibration only, word counts, fixed edit) is 0.0000.

### 15 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.500 (0.002) | 0.507 (0.011) | 0.549 (0.030) | 0.563 (0.041) | 0.546 (0.037) | 0.539 (0.038) | -0.007 | 0 |
| `housing_law` | 2 | 0.500 | 0.491 (0.000) | 0.436 (0.014) | 0.536 (0.035) | 0.524 (0.028) | 0.498 (0.046) | 0.492 (0.043) | -0.006 | 0 |
| `contract_type` | 15 | 0.067 | 0.176 (0.001) | 0.244 (0.008) | 0.214 (0.042) | 0.227 (0.047) | 0.244 (0.008) | 0.272 (0.045) | +0.028 | 20 |
| `language_id` | 20 | 0.050 | 0.352 (0.002) | 0.468 (0.017) | 0.115 (0.030) | 0.484 (0.048) | 0.468 (0.017) | 0.517 (0.095) | +0.049 | 20 |
| `patent_section` | 9 | 0.111 | 0.105 (0.000) | 0.178 (0.007) | 0.133 (0.016) | 0.182 (0.022) | 0.178 (0.007) | 0.188 (0.009) | +0.010 | 20 |
| `abstract_role` | 5 | 0.200 | 0.240 (0.002) | 0.221 (0.009) | 0.252 (0.032) | 0.267 (0.028) | 0.221 (0.009) | 0.246 (0.027) | +0.026 | 19 |
| `fed_stance` | 3 | 0.333 | 0.328 (0.002) | 0.304 (0.009) | 0.346 (0.018) | 0.330 (0.016) | 0.318 (0.015) | 0.318 (0.012) | -0.000 | 4 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.001) | 0.248 (0.007) | 0.258 (0.015) | 0.263 (0.019) | 0.250 (0.010) | 0.255 (0.011) | +0.005 | 13 |
| `hate_speech` | 2 | 0.500 | 0.540 (0.001) | 0.515 (0.008) | 0.518 (0.020) | 0.544 (0.027) | 0.548 (0.022) | 0.538 (0.023) | -0.009 | 0 |
| `counterfactual` | 2 | 0.500 | 0.471 (0.005) | 0.480 (0.009) | 0.536 (0.040) | 0.501 (0.020) | 0.481 (0.011) | 0.495 (0.016) | +0.015 | 6 |
| `appeal_outcome` | 2 | 0.500 | 0.483 (0.001) | 0.488 (0.009) | 0.515 (0.020) | 0.506 (0.020) | 0.501 (0.018) | 0.495 (0.015) | -0.006 | 0 |
| `fair_reason` | 2 | 0.500 | 0.519 (0.001) | 0.508 (0.005) | 0.495 (0.012) | 0.503 (0.014) | 0.507 (0.012) | 0.511 (0.011) | +0.005 | 0 |
| **Mean over tasks with a result** | | | **0.371** | **0.383** | **0.372** | **0.408** | **0.397** | **0.406** | **+0.0089** | |

- 0.6.0 `--auto` against As shipped: above on 9, below on 3, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 12, below on 0, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 5, below on 7, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 4, below on 8, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### 30 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.499 (0.003) | 0.506 (0.009) | 0.583 (0.037) | 0.599 (0.032) | 0.565 (0.052) | 0.565 (0.041) | +0.001 | 0 |
| `housing_law` | 2 | 0.500 | 0.491 (0.001) | 0.441 (0.016) | 0.559 (0.032) | 0.552 (0.029) | 0.521 (0.039) | 0.521 (0.036) | +0.000 | 0 |
| `contract_type` | 15 | 0.067 | 0.176 (0.002) | 0.248 (0.010) | 0.256 (0.035) | 0.265 (0.041) | 0.248 (0.010) | 0.311 (0.040) | +0.063 | 20 |
| `language_id` | 20 | 0.050 | 0.351 (0.002) | 0.473 (0.012) | 0.236 (0.036) | 0.675 (0.067) | 0.473 (0.012) | 0.644 (0.099) | +0.170 | 20 |
| `patent_section` | 9 | 0.111 | 0.105 (0.001) | 0.182 (0.006) | 0.156 (0.017) | 0.211 (0.020) | 0.182 (0.006) | 0.198 (0.033) | +0.016 | 20 |
| `abstract_role` | 5 | 0.200 | 0.240 (0.002) | 0.220 (0.007) | 0.302 (0.035) | 0.323 (0.038) | 0.257 (0.058) | 0.289 (0.041) | +0.032 | 13 |
| `fed_stance` | 3 | 0.333 | 0.329 (0.002) | 0.302 (0.009) | 0.349 (0.016) | 0.359 (0.020) | 0.332 (0.023) | 0.335 (0.019) | +0.003 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.001) | 0.249 (0.005) | 0.259 (0.014) | 0.282 (0.019) | 0.264 (0.019) | 0.269 (0.016) | +0.005 | 7 |
| `hate_speech` | 2 | 0.500 | 0.540 (0.003) | 0.513 (0.007) | 0.530 (0.021) | 0.592 (0.036) | 0.581 (0.037) | 0.576 (0.032) | -0.005 | 0 |
| `counterfactual` | 2 | 0.500 | 0.471 (0.006) | 0.480 (0.012) | 0.520 (0.037) | 0.505 (0.016) | 0.489 (0.020) | 0.491 (0.021) | +0.002 | 5 |
| `appeal_outcome` | 2 | 0.500 | 0.482 (0.002) | 0.489 (0.009) | 0.528 (0.024) | 0.518 (0.026) | 0.499 (0.023) | 0.498 (0.016) | -0.002 | 0 |
| `fair_reason` | 2 | 0.500 | 0.519 (0.002) | 0.505 (0.005) | 0.495 (0.012) | 0.502 (0.014) | 0.510 (0.009) | 0.511 (0.008) | +0.002 | 0 |
| **Mean over tasks with a result** | | | **0.371** | **0.384** | **0.398** | **0.448** | **0.410** | **0.434** | **+0.0238** | |

- 0.6.0 `--auto` against As shipped: above on 11, below on 1, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 12, below on 0, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 6, below on 6, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 2, below on 10, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 10, below on 2, level on 0 of 12 tasks.

### 60 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.500 (0.005) | 0.500 (0.006) | 0.611 (0.043) | 0.634 (0.042) | 0.626 (0.048) | 0.624 (0.045) | -0.002 | 0 |
| `housing_law` | 2 | 0.500 | 0.491 (0.001) | 0.434 (0.011) | 0.619 (0.034) | 0.597 (0.030) | 0.585 (0.048) | 0.581 (0.048) | -0.004 | 0 |
| `contract_type` | 15 | 0.067 | 0.174 (0.003) | 0.249 (0.008) | 0.343 (0.033) | 0.341 (0.032) | 0.249 (0.008) | 0.320 (0.077) | +0.071 | 20 |
| `language_id` | 20 | 0.050 | 0.350 (0.002) | 0.481 (0.009) | 0.437 (0.044) | 0.805 (0.043) | 0.481 (0.009) | 0.807 (0.035) | +0.326 | 20 |
| `patent_section` | 9 | 0.111 | 0.105 (0.002) | 0.179 (0.008) | 0.177 (0.023) | 0.230 (0.020) | 0.184 (0.017) | 0.230 (0.020) | +0.046 | 18 |
| `abstract_role` | 5 | 0.200 | 0.239 (0.004) | 0.217 (0.009) | 0.354 (0.033) | 0.356 (0.026) | 0.334 (0.050) | 0.326 (0.055) | -0.009 | 2 |
| `fed_stance` | 3 | 0.333 | 0.328 (0.003) | 0.299 (0.009) | 0.385 (0.023) | 0.372 (0.035) | 0.351 (0.032) | 0.354 (0.030) | +0.003 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.002) | 0.248 (0.005) | 0.271 (0.014) | 0.290 (0.021) | 0.290 (0.026) | 0.294 (0.021) | +0.004 | 1 |
| `hate_speech` | 2 | 0.500 | 0.538 (0.004) | 0.509 (0.005) | 0.551 (0.019) | 0.649 (0.040) | 0.634 (0.061) | 0.614 (0.066) | -0.020 | 0 |
| `counterfactual` | 2 | 0.500 | 0.476 (0.008) | 0.486 (0.011) | 0.526 (0.037) | 0.505 (0.015) | 0.491 (0.023) | 0.500 (0.020) | +0.009 | 1 |
| `appeal_outcome` | 2 | 0.500 | 0.482 (0.001) | 0.487 (0.009) | 0.546 (0.024) | 0.536 (0.026) | 0.524 (0.035) | 0.530 (0.031) | +0.006 | 0 |
| `fair_reason` | 2 | 0.500 | 0.520 (0.003) | 0.506 (0.004) | 0.495 (0.013) | 0.491 (0.019) | 0.497 (0.019) | 0.496 (0.018) | -0.001 | 0 |
| **Mean over tasks with a result** | | | **0.371** | **0.383** | **0.443** | **0.484** | **0.437** | **0.473** | **+0.0358** | |

- 0.6.0 `--auto` against As shipped: above on 11, below on 1, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 11, below on 1, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 6, below on 6, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 4, below on 8, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### 120 examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)

| Task | Answers | Guessing | As shipped | Calibration only | Word counts | Fixed edit | 0.5.0 `--auto` | 0.6.0 `--auto` | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |
|---|---|---|---|---|---|---|---|---|---|---|
| `unfair_clause` | 2 | 0.500 | 0.498 (0.006) | 0.504 (0.007) | 0.653 (0.029) | 0.667 (0.031) | 0.666 (0.032) | 0.666 (0.033) | +0.000 | 0 |
| `housing_law` | 2 | 0.500 | 0.491 (0.002) | 0.429 (0.008) | 0.652 (0.025) | 0.638 (0.023) | 0.629 (0.036) | 0.620 (0.045) | -0.008 | 0 |
| `contract_type` | 15 | 0.067 | 0.174 (0.006) | 0.250 (0.011) | 0.419 (0.041) | 0.409 (0.029) | 0.301 (0.085) | 0.414 (0.030) | +0.112 | 14 |
| `language_id` | 20 | 0.050 | 0.351 (0.004) | 0.484 (0.007) | 0.623 (0.041) | 0.903 (0.014) | 0.816 (0.166) | 0.899 (0.014) | +0.083 | 4 |
| `patent_section` | 9 | 0.111 | 0.105 (0.003) | 0.185 (0.007) | 0.216 (0.018) | 0.257 (0.017) | 0.212 (0.038) | 0.257 (0.019) | +0.044 | 11 |
| `abstract_role` | 5 | 0.200 | 0.240 (0.004) | 0.218 (0.007) | 0.387 (0.021) | 0.411 (0.030) | 0.402 (0.049) | 0.407 (0.039) | +0.005 | 0 |
| `fed_stance` | 3 | 0.333 | 0.328 (0.005) | 0.299 (0.013) | 0.402 (0.019) | 0.393 (0.029) | 0.383 (0.027) | 0.382 (0.029) | -0.001 | 0 |
| `climate_claim` | 4 | 0.250 | 0.249 (0.002) | 0.245 (0.007) | 0.277 (0.015) | 0.301 (0.010) | 0.300 (0.013) | 0.300 (0.014) | -0.001 | 0 |
| `hate_speech` | 2 | 0.500 | 0.541 (0.006) | 0.513 (0.008) | 0.587 (0.022) | 0.732 (0.027) | 0.736 (0.036) | 0.723 (0.055) | -0.012 | 0 |
| `counterfactual` | 2 | 0.500 | 0.477 (0.010) | 0.488 (0.018) | 0.534 (0.032) | 0.533 (0.030) | 0.517 (0.039) | 0.530 (0.032) | +0.013 | 0 |
| `appeal_outcome` | 2 | 0.500 | 0.482 (0.005) | 0.492 (0.007) | 0.563 (0.014) | 0.547 (0.021) | 0.537 (0.033) | 0.535 (0.034) | -0.002 | 0 |
| `fair_reason` | 2 | 0.500 | 0.519 (0.004) | 0.506 (0.008) | 0.489 (0.014) | 0.495 (0.018) | 0.502 (0.015) | 0.504 (0.014) | +0.002 | 0 |
| **Mean over tasks with a result** | | | **0.371** | **0.385** | **0.484** | **0.524** | **0.500** | **0.520** | **+0.0196** | |

- 0.6.0 `--auto` against As shipped: above on 11, below on 1, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Calibration only: above on 11, below on 1, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Word counts: above on 7, below on 5, level on 0 of 12 tasks.
- 0.6.0 `--auto` against Fixed edit: above on 2, below on 10, level on 0 of 12 tasks.
- 0.6.0 `--auto` against 0.5.0 `--auto`: above on 7, below on 5, level on 0 of 12 tasks.

### Settings 0.6.0 `--auto` chose (count over the 20 draws)

- `unfair_clause`, 15: lean 1 strength 0.25 ridge 1n: 6; lean 0.5 strength 2 ridge 0.25n: 3; lean 1 strength 4 ridge 0.25n: 2; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1, no read-out: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; unchanged: 1
- `unfair_clause`, 30: lean 1 strength 0.5 ridge 1n: 6; unchanged: 2; lean 0 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1
- `unfair_clause`, 60: lean 1 strength 1 ridge 1n: 7; lean 1 strength 4 ridge 4n: 3; lean 0 strength 2 ridge 4n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 1n: 1; lean 1 strength 0.25 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1
- `unfair_clause`, 120: lean 1 strength 2 ridge 1n: 6; lean 1 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 4n: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1
- `housing_law`, 15: lean 1 strength 0.25 ridge 1n: 8; lean 1, no read-out: 2; lean 1 strength 4 ridge 0.25n: 2; lean 0.5 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1
- `housing_law`, 30: lean 1 strength 0.5 ridge 1n: 9; unchanged: 3; lean 1 strength 4 ridge 1n: 1; lean 0.5, no read-out: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1
- `housing_law`, 60: lean 0.5 strength 4 ridge 4n: 4; lean 1 strength 1 ridge 1n: 3; lean 1 strength 0.5 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1
- `housing_law`, 120: lean 1 strength 2 ridge 1n: 6; lean 1 strength 1 ridge 1n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 4n: 1; unchanged: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `contract_type`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 1 strength 1 ridge 0.25n: 3; lean 1 strength 0.5 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 4n: 1; unchanged: 1; lean 0.5 strength 0.5 ridge 0.25n: 1
- `contract_type`, 30: lean 1 strength 0.5 ridge 1n: 12; lean 1 strength 1 ridge 0.25n: 3; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1
- `contract_type`, 60: lean 1 strength 1 ridge 1n: 5; unchanged: 3; lean 0 strength 1 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 2; lean 0.5 strength 0.25 ridge 4n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1, no read-out: 1; lean 1 strength 0.25 ridge 4n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `contract_type`, 120: lean 1 strength 0.5 ridge 4n: 3; lean 1 strength 2 ridge 1n: 3; lean 1 strength 1 ridge 1n: 2; lean 0 strength 1 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1
- `language_id`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 1 strength 0.5 ridge 0.25n: 4; unchanged: 4; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 0 strength 0.25 ridge 0.25n: 1
- `language_id`, 30: lean 1 strength 0.5 ridge 1n: 14; lean 0.5 strength 1 ridge 0.25n: 2; lean 1, no read-out: 2; lean 0 strength 2 ridge 0.25n: 1; unchanged: 1
- `language_id`, 60: lean 1 strength 1 ridge 1n: 16; lean 0.5 strength 0.5 ridge 0.25n: 2; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `language_id`, 120: lean 1 strength 2 ridge 1n: 13; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1
- `patent_section`, 15: lean 1 strength 0.25 ridge 1n: 16; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1
- `patent_section`, 30: lean 1 strength 0.5 ridge 1n: 14; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; unchanged: 1; lean 1 strength 1 ridge 0.25n: 1
- `patent_section`, 60: lean 1 strength 1 ridge 1n: 10; lean 0.5 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1
- `patent_section`, 120: lean 1 strength 2 ridge 1n: 9; lean 1 strength 1 ridge 4n: 3; lean 1 strength 2 ridge 4n: 3; lean 1 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 1n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1
- `abstract_role`, 15: lean 1 strength 0.25 ridge 1n: 6; lean 1, no read-out: 3; lean 0.5 strength 0.5 ridge 0.25n: 2; lean 0 strength 0.5 ridge 0.25n: 2; lean 0.5 strength 1 ridge 0.25n: 2; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; unchanged: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `abstract_role`, 30: lean 1 strength 0.5 ridge 1n: 8; lean 1 strength 2 ridge 0.25n: 2; unchanged: 2; lean 0 strength 2 ridge 0.25n: 2; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1
- `abstract_role`, 60: lean 1 strength 1 ridge 1n: 8; unchanged: 5; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1
- `abstract_role`, 120: lean 1 strength 2 ridge 1n: 7; lean 0.5 strength 1 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `fed_stance`, 15: lean 1 strength 0.25 ridge 1n: 8; lean 0.5 strength 0.25 ridge 0.25n: 3; lean 0.5, no read-out: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; unchanged: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `fed_stance`, 30: lean 1 strength 0.5 ridge 1n: 7; lean 0.5, no read-out: 2; lean 0 strength 2 ridge 0.25n: 2; unchanged: 2; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.25 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0 strength 0.5 ridge 0.25n: 1
- `fed_stance`, 60: lean 1 strength 1 ridge 1n: 7; lean 0.5, no read-out: 2; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1
- `fed_stance`, 120: lean 1 strength 2 ridge 1n: 8; lean 1 strength 4 ridge 0.25n: 3; lean 0 strength 1 ridge 0.25n: 2; lean 0.5 strength 0.5 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 0.25 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1
- `climate_claim`, 15: lean 1 strength 0.25 ridge 1n: 10; lean 0.5, no read-out: 3; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0 strength 1 ridge 0.25n: 1
- `climate_claim`, 30: lean 1 strength 0.5 ridge 1n: 9; lean 1 strength 1 ridge 0.25n: 2; lean 1 strength 0.25 ridge 4n: 1; unchanged: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `climate_claim`, 60: lean 1 strength 1 ridge 1n: 7; lean 0 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 0.25n: 1
- `climate_claim`, 120: lean 1 strength 2 ridge 1n: 7; lean 0.5 strength 0.5 ridge 4n: 2; lean 0.5 strength 4 ridge 0.25n: 2; lean 1 strength 0.25 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1
- `hate_speech`, 15: lean 0 strength 2 ridge 0.25n: 5; lean 1 strength 0.25 ridge 1n: 5; unchanged: 3; lean 1, no read-out: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1
- `hate_speech`, 30: lean 1 strength 0.5 ridge 1n: 6; unchanged: 3; lean 0 strength 1 ridge 0.25n: 2; lean 0 strength 2 ridge 4n: 2; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1
- `hate_speech`, 60: lean 1 strength 1 ridge 1n: 4; unchanged: 4; lean 0 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1, no read-out: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5, no read-out: 1
- `hate_speech`, 120: lean 0 strength 4 ridge 4n: 3; lean 0 strength 2 ridge 0.25n: 3; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; unchanged: 1; lean 1 strength 1 ridge 0.25n: 1
- `counterfactual`, 15: lean 1 strength 0.25 ridge 1n: 6; lean 1 strength 4 ridge 4n: 6; unchanged: 2; lean 0 strength 0.25 ridge 0.25n: 2; lean 0 strength 1 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1
- `counterfactual`, 30: lean 1 strength 0.5 ridge 1n: 16; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0 strength 0.5 ridge 4n: 1; unchanged: 1
- `counterfactual`, 60: lean 1 strength 1 ridge 1n: 13; lean 0 strength 0.25 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; unchanged: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 1n: 1
- `counterfactual`, 120: lean 1 strength 2 ridge 1n: 14; lean 0 strength 0.5 ridge 4n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 0.25 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `appeal_outcome`, 15: lean 1 strength 0.25 ridge 1n: 12; lean 0 strength 1 ridge 0.25n: 2; unchanged: 2; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1
- `appeal_outcome`, 30: lean 1 strength 0.5 ridge 1n: 11; lean 0 strength 4 ridge 4n: 2; unchanged: 2; lean 1, no read-out: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 0.25 ridge 4n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1
- `appeal_outcome`, 60: lean 1 strength 1 ridge 1n: 9; lean 1 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 4n: 2; lean 1 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; unchanged: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 4n: 1
- `appeal_outcome`, 120: lean 1 strength 2 ridge 1n: 4; lean 0.5 strength 4 ridge 4n: 2; lean 0 strength 4 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 1 strength 4 ridge 1n: 1; lean 0.5, no read-out: 1; lean 1 strength 0.25 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; unchanged: 1; lean 1, no read-out: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1
- `fair_reason`, 15: unchanged: 8; lean 1 strength 0.25 ridge 1n: 5; lean 1 strength 4 ridge 0.25n: 2; lean 0 strength 0.25 ridge 0.25n: 1; lean 0 strength 4 ridge 4n: 1; lean 1, no read-out: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 2 ridge 0.25n: 1
- `fair_reason`, 30: lean 1 strength 0.5 ridge 1n: 6; unchanged: 3; lean 0.5 strength 2 ridge 0.25n: 3; lean 0.5 strength 0.25 ridge 0.25n: 3; lean 0.5, no read-out: 2; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1
- `fair_reason`, 60: lean 1 strength 1 ridge 1n: 6; unchanged: 3; lean 0.5 strength 4 ridge 4n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.25 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 1 strength 0.25 ridge 1n: 1
- `fair_reason`, 120: unchanged: 6; lean 1 strength 2 ridge 1n: 5; lean 1, no read-out: 2; lean 0 strength 0.5 ridge 4n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1

### Settings 0.5.0 `--auto` chose (count over the 20 draws)

- `unfair_clause`, 15: lean 1 strength 2 ridge 1n: 5; lean 1 strength 4 ridge 1n: 4; lean 0 strength 1 ridge 1n: 3; unchanged: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0 strength 1 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1
- `unfair_clause`, 30: unchanged: 4; lean 1 strength 2 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 1, no read-out: 2; lean 0.5 strength 2 ridge 1n: 2; lean 0 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1
- `unfair_clause`, 60: lean 1 strength 4 ridge 4n: 4; lean 1 strength 2 ridge 1n: 3; lean 0 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1
- `unfair_clause`, 120: lean 1 strength 4 ridge 4n: 3; lean 0 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 0 strength 4 ridge 4n: 2; lean 1 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1
- `housing_law`, 15: lean 1, no read-out: 4; lean 1 strength 4 ridge 1n: 3; lean 0.5 strength 1 ridge 1n: 3; lean 0 strength 2 ridge 1n: 2; unchanged: 2; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1
- `housing_law`, 30: unchanged: 6; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 1n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1, no read-out: 1; lean 0.5, no read-out: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1
- `housing_law`, 60: lean 0.5 strength 4 ridge 4n: 3; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 2 ridge 1n: 2; lean 1 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1
- `housing_law`, 120: lean 0.5 strength 4 ridge 4n: 3; lean 1 strength 4 ridge 0.25n: 2; lean 1 strength 1 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 0.5 strength 4 ridge 0.25n: 2; lean 0 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1
- `contract_type`, 15: fallback (lean only): 20
- `contract_type`, 30: fallback (lean only): 20
- `contract_type`, 60: fallback (lean only): 20
- `contract_type`, 120: fallback (lean only): 14; lean 1 strength 0.5 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1
- `language_id`, 15: fallback (lean only): 20
- `language_id`, 30: fallback (lean only): 20
- `language_id`, 60: fallback (lean only): 20
- `language_id`, 120: fallback (lean only): 4; lean 1 strength 2 ridge 1n: 3; lean 0 strength 2 ridge 1n: 2; lean 1 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 4n: 1
- `patent_section`, 15: fallback (lean only): 20
- `patent_section`, 30: fallback (lean only): 20
- `patent_section`, 60: fallback (lean only): 18; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1
- `patent_section`, 120: fallback (lean only): 11; lean 1 strength 1 ridge 4n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 1, no read-out: 2; lean 1 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1
- `abstract_role`, 15: fallback (lean only): 19; lean 1, no read-out: 1
- `abstract_role`, 30: fallback (lean only): 13; lean 0 strength 2 ridge 1n: 2; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1
- `abstract_role`, 60: fallback (lean only): 2; lean 0 strength 1 ridge 4n: 2; lean 0 strength 4 ridge 1n: 2; lean 0 strength 2 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 1 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1
- `abstract_role`, 120: lean 0.5 strength 1 ridge 4n: 2; lean 0 strength 2 ridge 0.25n: 2; lean 1 strength 2 ridge 4n: 2; lean 1 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5, no read-out: 1; lean 0 strength 1 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 1 ridge 4n: 1
- `fed_stance`, 15: fallback (lean only): 4; lean 0.5, no read-out: 3; lean 1, no read-out: 3; unchanged: 3; lean 1 strength 2 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1
- `fed_stance`, 30: unchanged: 4; lean 1, no read-out: 3; lean 0 strength 2 ridge 1n: 2; lean 0.5, no read-out: 2; lean 1 strength 0.5 ridge 4n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 1n: 1; lean 0 strength 0.5 ridge 0.25n: 1
- `fed_stance`, 60: lean 1 strength 0.5 ridge 4n: 2; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 0.5, no read-out: 2; lean 1 strength 1 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1, no read-out: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 0.5 ridge 4n: 1
- `fed_stance`, 120: lean 1 strength 4 ridge 0.25n: 3; lean 0.5 strength 4 ridge 0.25n: 2; lean 0 strength 1 ridge 0.25n: 2; lean 1 strength 2 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 0.5, no read-out: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 0 strength 0.5 ridge 4n: 1
- `climate_claim`, 15: fallback (lean only): 13; unchanged: 3; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1, no read-out: 1; lean 0 strength 2 ridge 1n: 1
- `climate_claim`, 30: fallback (lean only): 7; lean 1 strength 1 ridge 1n: 3; unchanged: 2; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1, no read-out: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 1n: 1
- `climate_claim`, 60: lean 0.5 strength 0.5 ridge 1n: 2; lean 0 strength 4 ridge 1n: 2; lean 0 strength 2 ridge 4n: 2; lean 1 strength 4 ridge 4n: 2; lean 1 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1; lean 1, no read-out: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; fallback (lean only): 1; lean 1 strength 1 ridge 4n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1
- `climate_claim`, 120: lean 1 strength 2 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 2 ridge 1n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 0.5 strength 4 ridge 0.25n: 2; lean 0 strength 2 ridge 4n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0.5 strength 0.5 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 1 strength 4 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1
- `hate_speech`, 15: unchanged: 4; lean 1 strength 2 ridge 1n: 4; lean 0 strength 2 ridge 1n: 3; lean 0 strength 1 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 1; lean 1, no read-out: 1; lean 1 strength 1 ridge 1n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0 strength 0.5 ridge 1n: 1
- `hate_speech`, 30: lean 0 strength 1 ridge 1n: 3; lean 1 strength 4 ridge 1n: 3; lean 1 strength 2 ridge 1n: 3; lean 0 strength 0.5 ridge 1n: 2; unchanged: 2; lean 0.5 strength 1 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1
- `hate_speech`, 60: lean 0 strength 2 ridge 1n: 3; lean 0 strength 2 ridge 4n: 2; lean 0.5 strength 2 ridge 4n: 2; lean 1, no read-out: 2; lean 1 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 1n: 1; lean 0 strength 4 ridge 4n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5 strength 1 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 4 ridge 1n: 1; lean 0 strength 0.5 ridge 1n: 1; lean 0.5, no read-out: 1
- `hate_speech`, 120: lean 0 strength 2 ridge 0.25n: 3; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; lean 0 strength 4 ridge 4n: 2; lean 0 strength 2 ridge 4n: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 1 strength 1 ridge 0.25n: 1
- `counterfactual`, 15: fallback (lean only): 6; lean 0.5, no read-out: 4; lean 1, no read-out: 2; unchanged: 2; lean 1 strength 2 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1
- `counterfactual`, 30: fallback (lean only): 5; lean 1 strength 2 ridge 1n: 3; lean 1, no read-out: 3; lean 1 strength 0.5 ridge 1n: 3; lean 0.5, no read-out: 1; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 0.25n: 1; lean 0 strength 0.5 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 0.5 ridge 0.25n: 1
- `counterfactual`, 60: lean 1 strength 2 ridge 1n: 5; lean 1, no read-out: 4; lean 1 strength 0.5 ridge 1n: 2; lean 1 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 1 strength 2 ridge 4n: 1; unchanged: 1; fallback (lean only): 1; lean 0.5 strength 0.5 ridge 1n: 1
- `counterfactual`, 120: lean 1, no read-out: 5; lean 1 strength 2 ridge 4n: 2; lean 1 strength 2 ridge 0.25n: 2; lean 1 strength 0.5 ridge 0.25n: 2; lean 1 strength 1 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0.5, no read-out: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 1 strength 1 ridge 0.25n: 1
- `appeal_outcome`, 15: lean 0 strength 1 ridge 1n: 4; lean 0.5 strength 2 ridge 1n: 4; unchanged: 3; lean 1 strength 4 ridge 1n: 2; lean 0 strength 2 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 1, no read-out: 1; lean 0.5, no read-out: 1; lean 0.5 strength 4 ridge 1n: 1
- `appeal_outcome`, 30: lean 0.5, no read-out: 3; lean 0 strength 0.5 ridge 1n: 2; lean 1 strength 1 ridge 1n: 2; lean 1, no read-out: 2; lean 0 strength 4 ridge 1n: 2; lean 0.5 strength 1 ridge 1n: 1; lean 0 strength 2 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 0 strength 1 ridge 4n: 1; lean 1 strength 2 ridge 0.25n: 1; lean 1 strength 4 ridge 1n: 1; unchanged: 1
- `appeal_outcome`, 60: lean 1 strength 0.5 ridge 4n: 2; lean 0.5 strength 4 ridge 1n: 2; lean 1 strength 0.5 ridge 1n: 2; unchanged: 2; lean 0.5 strength 4 ridge 0.25n: 1; lean 1 strength 4 ridge 0.25n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1, no read-out: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5 strength 4 ridge 4n: 1; lean 1 strength 2 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1
- `appeal_outcome`, 120: lean 0 strength 4 ridge 4n: 4; lean 1 strength 4 ridge 1n: 2; lean 0.5 strength 4 ridge 4n: 2; lean 0.5, no read-out: 1; lean 0 strength 1 ridge 4n: 1; lean 0 strength 1 ridge 1n: 1; lean 0.5 strength 4 ridge 1n: 1; lean 0.5 strength 4 ridge 0.25n: 1; lean 0 strength 2 ridge 4n: 1; unchanged: 1; lean 1, no read-out: 1; lean 1 strength 0.5 ridge 4n: 1; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 4 ridge 0.25n: 1
- `fair_reason`, 15: lean 1, no read-out: 7; lean 0 strength 2 ridge 1n: 2; lean 0 strength 0.5 ridge 1n: 2; lean 1 strength 4 ridge 1n: 2; unchanged: 2; lean 0.5, no read-out: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 4 ridge 1n: 1; lean 1 strength 2 ridge 1n: 1
- `fair_reason`, 30: unchanged: 4; lean 1, no read-out: 4; lean 0.5 strength 2 ridge 0.25n: 2; lean 0.5, no read-out: 2; lean 1 strength 0.5 ridge 1n: 2; lean 0.5 strength 0.5 ridge 1n: 1; lean 1 strength 1 ridge 1n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 4 ridge 1n: 1; lean 0.5 strength 2 ridge 1n: 1; lean 0 strength 2 ridge 4n: 1
- `fair_reason`, 60: lean 0.5 strength 4 ridge 4n: 3; unchanged: 3; lean 0.5 strength 0.5 ridge 1n: 2; lean 1 strength 4 ridge 0.25n: 2; lean 1 strength 2 ridge 1n: 1; lean 0.5 strength 2 ridge 4n: 1; lean 0.5, no read-out: 1; lean 0.5 strength 2 ridge 1n: 1; lean 1 strength 4 ridge 4n: 1; lean 1 strength 1 ridge 4n: 1; lean 1 strength 0.5 ridge 1n: 1; lean 0 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 1, no read-out: 1
- `fair_reason`, 120: lean 1, no read-out: 5; unchanged: 2; lean 1 strength 0.5 ridge 4n: 2; lean 0 strength 0.5 ridge 4n: 1; lean 0.5 strength 2 ridge 0.25n: 1; lean 0 strength 2 ridge 1n: 1; lean 0 strength 1 ridge 0.25n: 1; lean 0.5 strength 1 ridge 0.25n: 1; lean 0 strength 1 ridge 4n: 1; lean 0.5, no read-out: 1; lean 0 strength 4 ridge 0.25n: 1; lean 0 strength 1 ridge 1n: 1; lean 0 strength 0.5 ridge 0.25n: 1; lean 0.5 strength 1 ridge 1n: 1

### The four rules (0.6.0)

**Rule 1 (no real harm at 15), 0.6.0: PASS.** `--auto` minus as shipped, per task:
- `unfair_clause`: +0.039
- `housing_law`: +0.001
- `contract_type`: +0.096
- `language_id`: +0.165
- `patent_section`: +0.083
- `abstract_role`: +0.007
- `fed_stance`: -0.010
- `climate_claim`: +0.005
- `hate_speech`: -0.002
- `counterfactual`: +0.024
- `appeal_outcome`: +0.012
- `fair_reason`: -0.008

**Rule 2 (matches the fixed edit at 120), 0.6.0: FAIL.** `--auto` minus fixed edit, per task:
- `unfair_clause`: -0.001
- `housing_law`: -0.017  <- more than 0.005 below
- `contract_type`: +0.004
- `language_id`: -0.004
- `patent_section`: -0.000
- `abstract_role`: -0.004
- `fed_stance`: -0.011  <- more than 0.005 below
- `climate_claim`: -0.002
- `hate_speech`: -0.009  <- more than 0.005 below
- `counterfactual`: -0.003
- `appeal_outcome`: -0.012  <- more than 0.005 below
- `fair_reason`: +0.010

**Rule 3 (level with the better safe choice at 15), 0.6.0: PASS.** Mean over 12 tasks of `--auto` minus the better of as shipped and calibration only: +0.0111. Per task:
- `unfair_clause`: +0.032
- `housing_law`: +0.001
- `contract_type`: +0.028
- `language_id`: +0.049
- `patent_section`: +0.010
- `abstract_role`: +0.007
- `fed_stance`: -0.010
- `climate_claim`: +0.005
- `hate_speech`: -0.002
- `counterfactual`: +0.015
- `appeal_outcome`: +0.007
- `fair_reason`: -0.008

**Rule 4 (not worse than 0.5.0):** mean over tasks of 0.6.0's `--auto` minus 0.5.0's `--auto`:
- 15 examples: +0.0089 over 12 tasks (0.6.0 above on 7, below on 5)
- 30 examples: +0.0238 over 12 tasks (0.6.0 above on 10, below on 2)
- 60 examples: +0.0358 over 12 tasks (0.6.0 above on 7, below on 5)
- 120 examples: +0.0196 over 12 tasks (0.6.0 above on 7, below on 5)

**Rule 4: PASS.**

### For comparison: Rules 1 to 3 applied to 0.5.0's `--auto` on the same tasks

**Rule 1 (no real harm at 15), 0.5.0: PASS.** `--auto` minus as shipped, per task:
- `unfair_clause`: +0.047
- `housing_law`: +0.007
- `contract_type`: +0.068
- `language_id`: +0.116
- `patent_section`: +0.073
- `abstract_role`: -0.019
- `fed_stance`: -0.010
- `climate_claim`: +0.001
- `hate_speech`: +0.008
- `counterfactual`: +0.009
- `appeal_outcome`: +0.018
- `fair_reason`: -0.012

**Rule 2 (matches the fixed edit at 120), 0.5.0: FAIL.** `--auto` minus fixed edit, per task:
- `unfair_clause`: -0.001
- `housing_law`: -0.009  <- more than 0.005 below
- `contract_type`: -0.108  <- more than 0.005 below
- `language_id`: -0.087  <- more than 0.005 below
- `patent_section`: -0.045  <- more than 0.005 below
- `abstract_role`: -0.009  <- more than 0.005 below
- `fed_stance`: -0.010  <- more than 0.005 below
- `climate_claim`: -0.001
- `hate_speech`: +0.003
- `counterfactual`: -0.016  <- more than 0.005 below
- `appeal_outcome`: -0.010  <- more than 0.005 below
- `fair_reason`: +0.007

**Rule 3 (level with the better safe choice at 15), 0.5.0: PASS.** Mean over 12 tasks of `--auto` minus the better of as shipped and calibration only: +0.0021. Per task:
- `unfair_clause`: +0.039
- `housing_law`: +0.007
- `contract_type`: +0.000
- `language_id`: +0.000
- `patent_section`: +0.000
- `abstract_role`: -0.019
- `fed_stance`: -0.010
- `climate_claim`: +0.001
- `hate_speech`: +0.008
- `counterfactual`: +0.000
- `appeal_outcome`: +0.013
- `fair_reason`: -0.012

