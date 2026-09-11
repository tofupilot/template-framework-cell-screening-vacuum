def release(measurements, bench, log):
    """Teardown: a last OCV so the cell goes to storage with a known
    voltage on the record."""
    ocv = bench.ocv_v()
    measurements.ocv_storage_v = ocv
    log.info(f"Released at {ocv:.4f} V")
