from dataclasses import dataclass
from pathlib import Path
import json
import os


@dataclass
class RiskConfig:
    max_risk_per_trade: float = 0.01
    daily_loss_limit: float = 0.03
    max_open_positions: int = 3
    max_total_exposure: float = 0.30


@dataclass
class WysperConfig:
    dry_run: bool = True
    risk: RiskConfig = RiskConfig()


def load_config(path: str = "config.json") -> WysperConfig:
    """
    Loads config from a JSON file. If not found, returns defaults.
    Environment variables can override selected fields.
    """
    cfg = WysperConfig()

    p = Path(path)
    if p.exists():
        data = json.loads(p.read_text())

        if "dry_run" in data:
            cfg.dry_run = bool(data["dry_run"])

        risk = data.get("risk", {})
        if "max_risk_per_trade" in risk:
            cfg.risk.max_risk_per_trade = float(risk["max_risk_per_trade"])
        if "daily_loss_limit" in risk:
            cfg.risk.daily_loss_limit = float(risk["daily_loss_limit"])
        if "max_open_positions" in risk:
            cfg.risk.max_open_positions = int(risk["max_open_positions"])
        if "max_total_exposure" in risk:
            cfg.risk.max_total_exposure = float(risk["max_total_exposure"])

    # Optional overrides
    if os.getenv("WYSPER_DRY_RUN") is not None:
        cfg.dry_run = os.getenv("WYSPER_DRY_RUN") == "1"

    return cfg

Add config schema + loader
