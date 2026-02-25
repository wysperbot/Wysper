# Risk Policy (Draft)

Wysper is built to endure. These constraints are non-negotiable.

## Hard rules
- **One wallet execution**
- **Max risk per trade** (configured)
- **Daily loss cap** (configured)
- **Max concurrent exposure** (configured)
- **Circuit breaker / kill switch**
- **No emotional overrides**
- **No revenge logic**

## Kill switch triggers (examples)
- Daily loss cap hit
- Repeated order failures
- Abnormal slippage beyond threshold
- Data feed becomes unreliable

## Change control
Any change to risk rules must be documented in:
- `CHANGELOG.md`
- this file (with rationale)
