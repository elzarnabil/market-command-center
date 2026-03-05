#!/usr/bin/env python3
"""
Market Command Center - Fetcher de Datos Financieros
Fuentes gratuitas: Yahoo Finance (sin API key)
Se ejecuta via GitHub Actions cada 30 min en horario de mercado
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
import os

SYMBOLS = {
    "spx":    "^GSPC",
    "ndx":    "^NDX",
    "ibex":   "^IBEX",
    "btc":    "BTC-USD",
    "vix":    "^VIX",
    "gold":   "GC=F",
    "oil":    "CL=F",
    "eurusd": "EURUSD=X",
    "dxy":    "DX-Y.NYB",
    "ust10":  "^TNX",
    "ust2":   "^IRX",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_ticker(symbol: str) -> dict | None:
    """Obtiene precio y medias móviles de Yahoo Finance (gratuito, sin API key)."""
    encoded = urllib.parse.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?interval=1d&range=1y"

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  ✗ {symbol}: {e}")
        # Retry con query2
        url2 = url.replace("query1", "query2")
        try:
            req2 = urllib.request.Request(url2, headers=HEADERS)
            with urllib.request.urlopen(req2, timeout=12) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e2:
            print(f"  ✗✗ {symbol} (query2): {e2}")
            return None

    try:
        result = data["chart"]["result"][0]
        meta   = result["meta"]
        closes = [c for c in (result.get("indicators", {}).get("quote", [{}])[0].get("close", [])) if c is not None]

        price   = meta.get("regularMarketPrice") or meta.get("previousClose") or (closes[-1] if closes else None)
        prev    = meta.get("previousClose") or (closes[-2] if len(closes) >= 2 else None)

        if price is None:
            return None

        chg_abs = (price - prev) if prev else 0
        chg_pct = (chg_abs / prev * 100) if prev else 0

        ma50  = (sum(closes[-50:])  / 50)  if len(closes) >= 50  else None
        ma200 = (sum(closes[-200:]) / 200) if len(closes) >= 200 else None

        return {
            "price":   round(price,   4),
            "chgAbs":  round(chg_abs, 4),
            "chgPct":  round(chg_pct, 4),
            "ma50":    round(ma50,    2) if ma50  else None,
            "ma200":   round(ma200,   2) if ma200 else None,
        }
    except (KeyError, IndexError, TypeError) as e:
        print(f"  ✗ parse {symbol}: {e}")
        return None


def main():
    print(f"\n{'='*50}")
    print(f"Market Command Center — Fetch Data")
    print(f"Hora UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    output = {}
    ok = 0

    for key, symbol in SYMBOLS.items():
        print(f"  → {key} ({symbol})")
        result = fetch_ticker(symbol)
        if result:
            output[key] = result
            ok += 1
            print(f"    ✓ precio={result['price']}  chg={result['chgPct']:+.2f}%")
        else:
            output[key] = None
        time.sleep(0.4)   # evitar rate-limit

    output["_meta"] = {
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "ok": ok,
        "total": len(SYMBOLS),
        "source": "Yahoo Finance (free, no API key)"
    }

    os.makedirs("data", exist_ok=True)
    out_path = "data/market.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Guardado: {out_path}  ({ok}/{len(SYMBOLS)} activos OK)\n")


if __name__ == "__main__":
    main()
