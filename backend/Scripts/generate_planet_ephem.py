"""
Generate heliocentric planet positions for a list of ISO timestamps using Skyfield.

This module provides a function `generate_planet_ephem` that the FastAPI app
can call to return JSON-serializable planet position data. It intentionally
does NOT change existing ephemeris/vector calculation code in the repo.

Notes:
- Skyfield will download a binary ephemeris (e.g., DE440s) on first run if
  not already available and requires internet access the first time.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import traceback

try:
    from skyfield.api import load
except Exception as e:
    # Defer import-time error to runtime; callers should catch and return helpful message
    load = None


EPHEMERIS_KEYS = {
    "mercury": "mercury",
    "venus": "venus",
    "earth": "earth",
    "mars": "mars barycenter",
    "jupiter": "jupiter barycenter",
    "saturn": "saturn barycenter",
    "uranus": "uranus barycenter",
    "neptune": "neptune barycenter",
    "sun": "sun",
}


def _parse_iso(s: str) -> datetime:
    # support strict ISO formats; will raise ValueError if invalid
    dt = datetime.fromisoformat(s)
    # skyfield expects timezone-aware datetimes; default naive datetimes to UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _make_datetimes(start_dt: datetime, end_dt: Optional[datetime], step_minutes: int) -> List[datetime]:
    if end_dt is None:
        return [start_dt]
    if end_dt < start_dt:
        raise ValueError("end must be >= start")
    times = []
    cur = start_dt
    while cur <= end_dt:
        times.append(cur)
        cur = cur + timedelta(minutes=step_minutes)
    return times


def generate_planet_ephem(start: str, end: Optional[str] = None, step_minutes: int = 60,
                          bodies: Optional[List[str]] = None) -> Dict[str, Any]:
    """Return planet positions for ISO time range.

    Args:
        start: ISO datetime string (required)
        end: ISO datetime string (optional). If omitted, a single epoch is returned.
        step_minutes: sampling cadence in minutes when end is provided.
        bodies: list of body names (short names like 'earth','mars',...)

    Returns a dict with keys:
        times: list of ISO times
        bodies: dict mapping body -> list of position dicts {iso,x,y,z,r_au}

    Raises helpful exceptions on missing dependencies or bad input.
    """
    if load is None:
        raise RuntimeError("skyfield is not available. Install 'skyfield' and 'jplephem' in the environment.")

    if bodies is None:
        bodies = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]

    try:
        start_dt = _parse_iso(start)
        end_dt = _parse_iso(end) if end else None
        dts = _make_datetimes(start_dt, end_dt, int(step_minutes))

        # Load timescale and ephemeris (will download if necessary)
        ts = load.timescale()
        eph = load("de440s.bsp")

        t = ts.utc(dts)
        sun = eph[EPHEMERIS_KEYS["sun"]]

        result = {"times": [dt.isoformat() for dt in dts], "bodies": {}}

        for b in bodies:
            key = EPHEMERIS_KEYS.get(b.lower())
            if not key:
                raise ValueError(f"Unknown body: {b}")
            body_obj = eph[key]
            # position relative to solar-system barycenter, subtract sun -> heliocentric
            pos = body_obj.at(t).position.au - sun.at(t).position.au  # shape (3, N)
            # materialize per-epoch dicts
            arr = []
            # pos is a numpy-like array with shape (3, N)
            N = pos.shape[1]
            for i in range(N):
                x = float(pos[0, i])
                y = float(pos[1, i])
                z = float(pos[2, i])
                r = (x * x + y * y + z * z) ** 0.5
                arr.append({"iso": result["times"][i], "x": x, "y": y, "z": z, "r_au": r})
            result["bodies"][b.lower()] = arr

        return result

    except Exception:
        # include traceback for debug convenience (FastAPI will surface message)
        raise


__all__ = ["generate_planet_ephem"]
