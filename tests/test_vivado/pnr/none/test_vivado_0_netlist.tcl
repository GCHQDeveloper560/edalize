# Write a timing simulation netlist and SDF

open_run [get_runs impl_1]

set top [ get_property top [current_fileset] ]

write_verilog -mode timesim -sdf_anno true -force -file ${top}_timesim.v
write_sdf -mode timesim -process_corner slow -force -file ${top}_timesim.sdf

