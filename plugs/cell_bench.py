"""Cell screening bench (mock): a battery cycler channel with a
four-wire cell holder, an AC impedance meter at 1 kHz, an analytical
balance, and a small vacuum chamber with a gauge.

Maps to a Neware, Arbin or Chroma cycler channel over its API, a
Hioki BT3562 battery tester for OCV and ACIR, a Sartorius or Mettler
balance over RS-232, and a bell-jar chamber with a Pirani gauge. The
mock synthesizes a healthy cell: 3.42 Ah at C/2, 3.652 V OCV, 23 mohm,
48.15 g, and after six hours under vacuum an OCV 0.4 mV lower, a
capacity 0.6 % lower, 4 mg lighter and 0.3 mohm higher. Swap for
classes speaking the cycler's API and SCPI; the phases stay unchanged.
"""

import numpy as np

from utils.recipe import CELL_CAPACITY_AH_NOM, DISCHARGE_C_RATE, DISCHARGE_CUTOFF_V, VACUUM_H


class CellBench:
    def __init__(self):
        self._rng = np.random.default_rng(1011)
        self._cap_ah = 3.42 + self._rng.normal(0.0, 0.02)
        self._ocv = 3.652 + self._rng.normal(0.0, 0.002)
        self._acir = 23.1 + self._rng.normal(0.0, 0.3)
        self._mass = 48.15 + self._rng.normal(0.0, 0.05)
        self._store = {}
        # self.cycler = ...; self.bt = pyvisa...; self.balance = serial...; self.chamber = ...
        print("Cell bench ready, holder open, chamber at ambient")

    def identify(self):
        return {"visual_ok": True, "vendor_code": "INR18650-35E"}

    def mass_g(self):
        return round(self._mass + self._rng.normal(0.0, 0.0005), 4)

    def ocv_v(self):
        return round(self._ocv + self._rng.normal(0.0, 0.0001), 4)

    def acir_mohm(self):
        return round(self._acir + self._rng.normal(0.0, 0.05), 2)

    def charge_full(self):
        pass

    def discharge(self):
        """CC discharge at C/2 to the cutoff, voltage logged per 0.02 Ah.
        Time-scaled; returns the whole curve."""
        q = np.arange(0.0, self._cap_ah + 0.02, 0.02)
        soc = 1.0 - q / self._cap_ah
        # NMC-shaped curve: plateau around 3.6 V, knee at the end.
        v = 3.35 + 0.25 * soc + 0.55 * soc ** 3 + 0.06 * np.log(np.clip(soc, 1e-3, 1.0))
        v = v - DISCHARGE_C_RATE * self._acir * 1e-3 * CELL_CAPACITY_AH_NOM  # IR drop at C/2
        v = np.clip(v, DISCHARGE_CUTOFF_V, 4.2)
        cut = np.flatnonzero(v <= DISCHARGE_CUTOFF_V)
        end = int(cut[0]) + 1 if cut.size else q.size
        return {"capacity_ah": q[:end].round(3).tolist(), "voltage_v": (v[:end] + self._rng.normal(0.0, 0.001, end)).round(4).tolist()}

    def vacuum_exposure(self, hours):
        """Chamber pumped and held; pressure logged every 5 min. The cell
        rests open-circuit inside. Time-scaled."""
        t = np.arange(0.0, hours + 1.0 / 12, 1.0 / 12)
        p = 1013.0 * np.exp(-t * 40.0) + 4e-4 * (1.0 + 0.2 * np.exp(-t))
        # What the exposure does to a healthy cell: almost nothing.
        self._ocv -= 0.0004
        self._cap_ah *= 0.994
        self._mass -= 0.004
        self._acir += 0.3
        return {"time_h": t.round(3).tolist(), "pressure_hpa": [float(f"{x:.3g}") for x in p]}

    def store(self, key, value):
        self._store[key] = value

    def recall(self, key):
        return self._store[key]

    def __del__(self):
        print("Holder open, chamber at ambient")
