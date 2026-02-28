# Linear A Computational Analysis

Computational structural analysis of the Minoan Linear A script (~1850-1450 BCE). This project applies information-theoretic, morphological, and cross-domain methods to extract linguistic structure from the undeciphered corpus without requiring a bilingual text.

## What This Is

Linear A is one of the last major undeciphered writing systems. These scripts analyze the ~1,427 known inscriptions using computational methods to:

- Test proposed grammatical rules against the libation formula corpus (41 variants)
- Measure information-theoretic properties (Shannon entropy, bigram predictability)
- Compare the Minoan sound system against candidate language families
- Apply statistical controls (permutation testing, ablation, perturbation analysis)
- Evaluate cross-domain convergence across linguistic, archaeological, and genetic evidence

## Key Findings

- **6/6 morphological agreement rules confirmed** with zero exceptions across the libation formula corpus
- **Shannon entropy of 4.70 bits/sign** — squarely in the natural language range
- **9/9 administrative structural features** match other Bronze Age accounting systems
- **Vowel distribution** (a=43%, i=21%, u=18%, e=14%, o=4%) matches Beekes' reconstructed pre-Greek three-vowel system
- Hurro-Urartian shows strongest overall fit at 77.7% across 14 dimensions, with a 37-point gap over the next candidate (Semitic at 40.1%)

## Scripts

| Script | Description |
|--------|-------------|
| `LINEAR_A_STRUCTURAL_ANALYSIS.py` | Core analysis: libation formula corpus, morphological rule testing, information theory, sign frequency, co-occurrence networks |
| `LINEAR_A_PHONOLOGICAL_ANALYSIS.py` | Sound system analysis: phonotactics, vowel harmony, consonant clusters, syllable structure, rhythm patterns |
| `LINEAR_A_HURRIAN_COMPARISON.py` | Systematic Hurrian grammar comparison: case system mapping, vocabulary, verbal morphology |
| `LINEAR_A_ENHANCED_COMPARISON.py` | Extended comparison with pre-Greek substrate, Urartian three-way analysis, Van Soesbergen readings |
| `LINEAR_A_STATISTICAL_CONTROLS.py` | Reviewer-proof controls: baseline distributions across 6 language families, ablation, permutation testing, sign-reading perturbation |
| `LINEAR_A_CROSS_DOMAIN_CONVERGENCE.py` | Bayesian convergence across 8 independent evidence domains (linguistic, archaeogenetic, maritime trade, material culture, religious iconography, etc.) |
| `LINEAR_A_TRANSLATION_ATTEMPT.md` | Full writeup: established facts, analysis results, proposed translations, confidence levels, honest assessment of unknowns |

## Running

All scripts use only the Python 3 standard library. No external dependencies.

```bash
python3 LINEAR_A_STRUCTURAL_ANALYSIS.py
python3 LINEAR_A_STATISTICAL_CONTROLS.py
python3 LINEAR_A_CROSS_DOMAIN_CONVERGENCE.py
# etc.
```

## Methodology

**Confidence protocol**: Every claim is tagged `[HIGH]`, `[MEDIUM]`, `[LOW]`, or `[SPECULATIVE]`.

The approach treats Linear A as a systems analysis problem rather than a purely linguistic one:

1. **Structural analysis** — Variant comparison across 41 libation formula inscriptions reveals grammatical agreement rules
2. **Administrative pattern matching** — Cross-cultural comparison with Sumerian, Egyptian, and Linear B accounting systems
3. **Statistical controls** — Every proposed pattern is tested against null hypotheses and competing language families
4. **Cross-domain convergence** — Independent evidence streams (DNA, trade networks, material culture) evaluated via Bayesian updating

## Data Sources

- SigLA Database (Salgarella & Castellan, 2020)
- GORILA Corpus (Godart & Olivier, 1976-1985)
- Younger, J.G. — Linear A Texts in Phonetic Transcription
- Davis, B. (Melbourne) — Statistical/phonotactic analysis
- Corazza, Montecchi, Valerio, Tamburini (Bologna, 2020) — Fraction sign values
- Van Soesbergen, P.G. (2017) — Hurrian hypothesis
- Beekes, R.S.P. (2014) — Pre-Greek substrate reconstruction

## License

MIT
