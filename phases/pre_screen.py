from phases.characterise import characterise


def pre_screen(measurements, bench, log):
    """Characterisation before the vacuum exposure; the reference kept on
    the bench plug because phases cannot read each other's measurements."""
    ref = characterise(measurements, bench, log, "pre", measurements.discharge_pre)
    bench.store("pre", ref)
