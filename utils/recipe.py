"""Cell screening recipe for COTS 18650 cells going into a smallsat
battery: every cell characterised, exposed to vacuum, characterised
again, and accepted on how little it changed.

Where the numbers come from. The Nanoracks payload safety screening
for lithium-ion cells (NR-SRD-139) is the reference most CubeSat
programmes follow for COTS cells: 100 % screening with a visual, mass,
open-circuit voltage and capacity before and after a vacuum exposure
(and a vibration, run as its own procedure here), and acceptance on
the change: OCV within 0.1 %, capacity within 5 %, mass within 0.1 %.
The AC impedance at 1 kHz and its change are the programme's own
addition, because a cell whose impedance moved has a seal or an
electrolyte problem the other three may not show yet. The cell data
(3.5 Ah class, NMC, 3.6 V nominal) is the vendor's."""

CELL_CAPACITY_AH_NOM = 3.5
CAPACITY_AH_MIN = 3.30
OCV_V_MIN = 3.55
OCV_V_MAX = 3.75
ACIR_MOHM_MAX = 30.0
MASS_G_MIN = 47.5
MASS_G_MAX = 49.0

DISCHARGE_C_RATE = 0.5
DISCHARGE_CUTOFF_V = 3.0
CHARGE_V = 4.2

VACUUM_HPA_MAX = 1.0e-3
VACUUM_H = 6.0

OCV_DELTA_PCT_MAX = 0.1
CAPACITY_DELTA_PCT_MAX = 5.0
MASS_DELTA_PCT_MAX = 0.1
ACIR_DELTA_PCT_MAX = 20.0
TIME_SCALE = 0.0   # mock returns the discharge and the vacuum exposure in one call each
