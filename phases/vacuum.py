import numpy as np

from utils.recipe import VACUUM_H, VACUUM_HPA_MAX


def vacuum(measurements, bench, ui, log):
    """Six hours under vacuum, open-circuit. A cell with a weak seal or a
    gassing electrolyte vents, and the post characterisation sees it."""
    cap = bench.vacuum_exposure(VACUUM_H)
    ui.vacuum_progress = 100
    t = np.array(cap["time_h"]); p = np.array(cap["pressure_hpa"])
    under = t[p <= VACUUM_HPA_MAX]
    hours_under = float(under[-1] - under[0]) if under.size > 1 else 0.0
    measurements.exposure.x_axis = cap["time_h"]
    measurements.exposure.y_axis.pressure = cap["pressure_hpa"]
    measurements.exposure.y_axis.pressure.aggregations.min_hpa = float(p.min())
    measurements.exposure.y_axis.pressure.aggregations.hours_under_h = hours_under
    log.info(f"Vacuum {t[-1]:.1f} h, {p.min():.1e} hPa at best, {hours_under:.1f} h under {VACUUM_HPA_MAX:.0e} hPa")
