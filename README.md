# Security-Warnings-Fatigue-Analyzer-SWFA
## Overview

Security Warnings Fatigue Analyzer (SWFA) is a stochastic simulation framework that models user attention decay, recovery dynamics, and probabilistic reactions to repeated security alerts.
The project explores how repeated exposure to warnings affects decision quality, error probability, and long-term cognitive stability.

`This is beta version of README. I will rewrite it in the future.`

## Motivation

Modern systems frequently display security warnings.
Over time, users may experience alert fatigue, leading to:

- Increased ignore rate

- Higher error probability

- Decreased effective attention

- Potential bifurcation into unstable behavior regimes

SWFA provides a computational model to simulate and analyze these dynamics.

## Model Description

The model represents a user as a dynamic system with:

- Attention state ```A(t)∈[0,1]```

- Fatigue decay after alerts

- Exponential recovery over time

- Softmax-based probabilistic action selection

Possible reactions to alerts:

- READ

- IGNORE

- ERROR

Attention evolves according to:

Fatigue:
```A ← A · exp(-fatigue_rate · severity)```

Recovery:
```dA/dt = recovery_rate · (1 - A)```

Decision probabilities are computed via temperature-controlled softmax over utility logits.

## Key Parameters

Parameter - Meaning

```fatigue_rate``` - Speed of attention decay

```recovery_rate```	- Speed of recovery

```sensitivity```	- How strongly severity influences reading

```error_sensitivity```	- How strongly low attention increases errors

```temperature```	- Rationality vs randomness

```ignore_bias```	- Baseline ignore tendency

## Example Usage

```python
user = User()
alert = Alert(severity=Severity.HIGH, type="malware", timestamp=0.0)

reaction, attention = user.react_to_alert(alert)
```

## Research Potential

The model allows exploration of:

- Phase transitions in error rates

- Stability vs instability regimes

- Critical error_sensitivity thresholds

- Long-term behavioral equilibria

## Future Work

 - Memory-dependent fatigue

 - Habituation effects

 - Multi-agent modeling

 - UI adaptation strategies

 - Empirical parameter fitting

## Licence

GNU GPL v3.0
