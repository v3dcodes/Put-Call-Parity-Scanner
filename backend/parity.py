"""Put/call parity scanner.

European parity (dividend-free index):  C - P = S - K * e^{-rT}

For every (expiry, strike) we pair the call and put mids and measure the
residual against parity. A residual larger than the round-trip bid/ask cost is a
*potential* arbitrage / data anomaly worth a look.

    residual = (C_mid - P_mid) - (S - K * e^{-rT})
"""
import numpy as np
import pandas as pd


def scan(df, spot, r=0.045):
    calls = df[df.type == "C"].set_index(["dte", "strike"])
    puts = df[df.type == "P"].set_index(["dte", "strike"])
    rows = []
    for key in calls.index.intersection(puts.index):
        dte, k = key
        c, p = calls.loc[key], puts.loc[key]
        t = dte / 365.0
        theo_diff = spot - k * np.exp(-r * t)            # parity RHS
        residual = (c.mid - p.mid) - theo_diff
        # round-trip cost to actually capture it (cross both spreads)
        cost = (c.ask - c.bid) / 2 + (p.ask - p.bid) / 2
        rows.append(dict(
            expiry=c.expiry, dte=int(dte), strike=float(k),
            call_mid=float(c.mid), put_mid=float(p.mid),
            residual=float(residual), edge=float(abs(residual) - cost),
            signal="rich call" if residual > 0 else "rich put",
        ))
    out = pd.DataFrame(rows).sort_values("strike")
    out["arb"] = out.edge > 0
    return out.reset_index(drop=True)


def payload(df, spot, r=0.045):
    out = scan(df, spot, r)
    flagged = out[out.arb].reindex(out.edge.sort_values(ascending=False).index).head(25)
    return {
        "spot": spot,
        "n_scanned": int(len(out)),
        "n_flagged": int(out.arb.sum()),
        "rows": [
            {**{k: r2[k] for k in ("expiry", "dte", "strike", "call_mid",
                                   "put_mid", "residual", "edge", "signal", "arb")}}
            for r2 in out.to_dict("records")
        ],
        "top": flagged.to_dict("records"),
    }
