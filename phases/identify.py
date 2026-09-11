def identify(measurements, bench, unit, log):
    """Setup: visual inspection result and vendor code on the record;
    a dented, scratched or leaking cell goes no further."""
    ident = bench.identify()
    measurements.visual_ok = ident["visual_ok"]
    unit.metadata["vendor_code"] = ident["vendor_code"]
    log.info(f"Cell {unit.serial_number}: {ident['vendor_code']}, visual {'ok' if ident['visual_ok'] else 'REJECT'}")
