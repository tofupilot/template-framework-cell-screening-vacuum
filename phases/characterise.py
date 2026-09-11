import numpy as np


def characterise(measurements, bench, log, prefix, curve_meas):
    """Shared by the pre and post phases: mass, OCV, ACIR at 1 kHz, then
    a full charge and a C/2 discharge to the cutoff with the capacity
    read from the curve."""
    mass = bench.mass_g()
    ocv = bench.ocv_v()
    acir = bench.acir_mohm()
    bench.charge_full()
    cap = bench.discharge()
    q = np.array(cap["capacity_ah"])
    capacity = float(q[-1])

    setattr(measurements, f"mass_{prefix}_g", mass)
    setattr(measurements, f"ocv_{prefix}_v", ocv)
    setattr(measurements, f"acir_{prefix}_mohm", acir)
    curve_meas.x_axis = cap["capacity_ah"]
    curve_meas.y_axis.voltage = cap["voltage_v"]
    curve_meas.y_axis.voltage.aggregations.capacity_ah = capacity
    log.info(f"{prefix}: {mass:.4f} g, OCV {ocv:.4f} V, ACIR {acir:.2f} mohm, {capacity:.3f} Ah at C/2")
    return {"mass": mass, "ocv": ocv, "acir": acir, "capacity": capacity}
