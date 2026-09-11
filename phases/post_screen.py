from phases.characterise import characterise


def post_screen(measurements, bench, log):
    """Characterisation after the vacuum exposure, and the four deltas
    against the reference: the numbers the cell is accepted on."""
    post = characterise(measurements, bench, log, "post", measurements.discharge_post)
    ref = bench.recall("pre")
    measurements.ocv_delta_pct = float(100.0 * abs(post["ocv"] - ref["ocv"]) / ref["ocv"])
    measurements.capacity_delta_pct = float(100.0 * abs(post["capacity"] - ref["capacity"]) / ref["capacity"])
    measurements.mass_delta_pct = float(100.0 * abs(post["mass"] - ref["mass"]) / ref["mass"])
    measurements.acir_delta_pct = float(100.0 * abs(post["acir"] - ref["acir"]) / ref["acir"])
    log.info(f"Deltas: OCV {100.0 * abs(post['ocv'] - ref['ocv']) / ref['ocv']:.3f} %, capacity {100.0 * abs(post['capacity'] - ref['capacity']) / ref['capacity']:.2f} %, mass {100.0 * abs(post['mass'] - ref['mass']) / ref['mass']:.4f} %, ACIR {100.0 * abs(post['acir'] - ref['acir']) / ref['acir']:.1f} %")
