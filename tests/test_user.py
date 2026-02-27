
# by PiaPsyker918

import numpy as np
import pytest

from core.user import User, Alert, Severity, Reaction


def make_alert(severity=Severity.MEDIUM):
    return Alert(severity=severity, type="security", timestamp=0.0)

def test_attention_bounds():
    # Attention always in [0, 1]
    user = User()

    for _ in range(500):
        user.react_to_alert(make_alert(Severity.HIGH))

    assert 0 <= user.get_attention() <= 1


def test_fatigue_decreases_attention():
    # Alerts reduce attention
    user = User(initial_attention=1.0)

    before = user.get_attention()
    user.react_to_alert(make_alert(Severity.HIGH))
    after = user.get_attention()

    assert after < before


def test_recovery_increases_attention():
    # Recovery increases attention
    user = User(initial_attention=0.3)

    before = user.get_attention()
    user.step(dt=5.0)
    after = user.get_attention()

    assert after > before


def test_low_attention_more_errors():
    # If low attention -> more errors
    user = User(initial_attention=0.1)

    errors = 0

    for _ in range(1000):
        action, _ = user.react_to_alert(make_alert(Severity.HIGH))
        if action == Reaction.ERROR:
            errors += 1

    assert errors > 0.15 * 1000  # at least 15%


def test_high_severity_more_reads():
    # High severity reads more then low
    user1 = User(initial_attention=1.0)
    user2 = User(initial_attention=1.0)

    reads_low = 0
    reads_high = 0

    for _ in range(500):
        if user1.react_to_alert(make_alert(Severity.LOW))[0] == Reaction.READ:
            reads_low += 1

        if user2.react_to_alert(make_alert(Severity.HIGH))[0] == Reaction.READ:
            reads_high += 1

    assert reads_high > reads_low
