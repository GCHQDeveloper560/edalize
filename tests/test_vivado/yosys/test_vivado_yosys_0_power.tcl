# Analyse power using a SAIF file from simulation

open_run [get_runs impl_1]

set top [ get_property top [current_fileset] ]

# No switching activity (SAIF) files found. Skipping read_saif

report_power -format text -file ${top}_report_power.txt

