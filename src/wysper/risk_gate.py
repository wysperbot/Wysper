from wysper.constants import (
    ENTRY_ATTEMPT,
    ENTRY_APPROVED,
    ENTRY_BLOCKED,
)

from wysper.event_logger import EventLogger


class RiskGate:
    """
    Enforces hard risk constraints before allowing execution.
    """

    def __init__(self, config):
        self.config = config
        self.logger = EventLogger()
        self.daily_loss = 0.0
        self.open_positions = 0
        self.total_exposure = 0.0

    def evaluate_entry(self, symbol, risk_amount, exposure_amount):
        self.logger.log_event(
            ENTRY_ATTEMPT,
            symbol=symbol,
            risk=risk_amount,
        )

        if risk_amount > self.config.risk.max_risk_per_trade:
            self.logger.log_event(
                ENTRY_BLOCKED,
                reason="risk_per_trade_exceeded",
                symbol=symbol,
            )
            return False

        if self.daily_loss >= self.config.risk.daily_loss_limit:
            self.logger.log_event(
                ENTRY_BLOCKED,
                reason="daily_loss_limit_reached",
                symbol=symbol,
            )
            return False

        if self.open_positions >= self.config.risk.max_open_positions:
            self.logger.log_event(
                ENTRY_BLOCKED,
                reason="max_open_positions_reached",
                symbol=symbol,
            )
            return False

        if self.total_exposure + exposure_amount > self.config.risk.max_total_exposure:
            self.logger.log_event(
                ENTRY_BLOCKED,
                reason="exposure_limit_exceeded",
                symbol=symbol,
            )
            return False

        self.logger.log_event(
            ENTRY_APPROVED,
            symbol=symbol,
        )

        return True
