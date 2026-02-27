
# Main file of the user model
# by PiaPsyker918

from dataclasses import dataclass
from enum import Enum
import numpy as np

class Severity(float, Enum):
    LOW = 0.3
    MEDIUM = 0.6
    HIGH = 1.0

class Reaction(str, Enum):
    READ = "read"
    IGNORE = "ignore"
    ERROR = "error"

@dataclass(slots=True)
class Alert:
    severity: float | Severity
    type: str
    timestamp: float

@dataclass(slots=True)
class UserState:
    attention: float = 1.0
    time: float = 0.0

# USER MODEL

class User:

    def __init__(
        self,
        initial_attention: float = 1.0,     # You can change these values to get a different result:
        fatigue_rate: float = 0.15,         # fatigue_rate (float ; 0.15) ↑ → faster burnout | recovery_rate (float ; 0.05) ↑ → faster recovery 
        recovery_rate: float = 0.05,        # error_factor (float ; 0.3) ↑ → more errors | sensitivity (float ; 5.0) ↑ → stronger effect of severity
        sensitivity: float = 5.0,           # Best parametrs: error_sensitivity = 1 or 2 ; temperature = 1.0 - 1.3
        error_factor: float = 0.3,          # bifurcation point - error_sensitivity ≈ 2–3
        ignore_bias = 0.5,                  # 
        error_sensitivity = 4.0,            # 
        temperature: float = 1.0,           # by PiaPsyker918
        rng: np.random.Generator | None = None,
    ):
        self.state = UserState(attention=initial_attention)

        self.fatigue_rate = fatigue_rate
        self.recovery_rate = recovery_rate
        self.sensitivity = sensitivity
        self.error_factor = error_factor
        self.ignore_bias = ignore_bias
        self.error_sensitivity = error_sensitivity
        self.temperature = temperature

        self.rng = rng or np.random.default_rng()

    def step(self, dt: float) -> None:

        self._recover(dt)
        self.state.time += dt


    def react_to_alert(self, alert: Alert) -> tuple[Reaction, float]:
        severity = float(alert.severity)

        self._fatigue(severity)

        probs = self._reaction_probabilities(severity)

        actions = [Reaction.READ, Reaction.IGNORE, Reaction.ERROR]

        r = self.rng.random()
        cum = np.cumsum(probs)
        idx = int(np.searchsorted(cum, r, side="right"))

        idx = max(0, min(idx, len(actions) - 1))
        action = actions[idx]

        self._post_action_update(action)

        return action, self.state.attention
    
    def get_attention(self) -> float:
        return self.state.attention
    
    def _fatigue(self, severty: float) -> None:

        self.state.attention *= np.exp(-self.fatigue_rate * severty)
        self._clamp_attention()

    def _recover(self, dt: float) -> None:

        self.state.attention += self.recovery_rate * dt * (1 - self.state.attention)
        self._clamp_attention()

    def _reaction_probabilities(self, severity: float) -> np.ndarray:
        a = self.state.attention

        u_read = self.sensitivity * severity * a
        u_ignore = self.ignore_bias * (1 - a)
        # default: u_error = self.error_factor * severity * (1 - a)
        # variant 1: u_error = self.error_factor * severity**2 * (1 - a)
        u_error = self.error_sensitivity * severity * (1 - a)

        logits = np.array([u_read, u_ignore, u_error], dtype=float)

        return User.softmax(logits, temperature=self.temperature)

    def _post_action_update(self, action: Reaction) -> None:

        if action == Reaction.READ:
            self.state.attention -= 0.02

        elif action == Reaction.ERROR:
            self.state.attention -= 0.05
        
        self._clamp_attention()

    def _clamp_attention(self) -> None:
        self.state.attention = float(np.clip(self.state.attention, 0.0, 1.0))

    def reset(self):
        self.state = UserState(attention=1.0, time=0.0)

    @staticmethod
    def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        x = x / temperature
        x = x - np.max(x)
        exp_x = np.exp(x)
        return exp_x / (np.sum(exp_x) + 1e-12)
