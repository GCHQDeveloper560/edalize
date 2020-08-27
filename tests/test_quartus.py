import os
from edalize_common import make_edalize_test

qsys_file = """<?xml version="1.0" encoding="UTF-8"?>
<system name="test">
 <component
   name="test"
   displayName="test"
   version="1.0"
   description=""
   tags=""
   categories="System"
   {}
   />
</system>
"""

qsys_fill = {"Standard": "",
             "Pro"     : "tool=\"QsysPro\""}

test_sets = {"Standard": {"Quartus": ['ip-generate.cmd', 'quartus_asm.cmd', 'quartus_fit.cmd', 'quartus_map.cmd', 'quartus_sh.cmd', 'quartus_sta.cmd'],
                          "DSE"    : ['ip-generate.cmd', 'quartus_map.cmd', 'quartus_sh.cmd', 'quartus_dse.cmd']},
             "Pro"     : {"Quartus": ['qsys-generate.cmd', 'quartus_asm.cmd', 'quartus_fit.cmd', 'quartus_syn.cmd', 'quartus_sh.cmd', 'quartus_sta.cmd'],
                          "DSE"    : ['qsys-generate.cmd', 'quartus_syn.cmd', 'quartus_sh.cmd', 'quartus_dse.cmd']}}

for edition in ["Standard", "Pro"]:
    test_sets[edition]["Netlist"] = test_sets[edition]["Quartus"] + ["quartus_eda.cmd"]
    test_sets[edition]["Power"] = test_sets[edition]["Netlist"] + ["quartus_pow.cmd"]


def test_quartus(make_edalize_test):
    tool_options = {
        'family'          : 'Cyclone V',
        'device'          : '5CSXFC6D6F31C8ES',
        'quartus_options' : ['some', 'quartus_options'],
        'dse_options'     : ['some', 'dse_options'],
        'pow_options'     : ['vcd_filter_glitches=on', 'something_else=off'],
    }

    # Test each edition of Quartus
    for edition in ["Standard", "Pro"]:
        for pnr in ["Quartus", "DSE", "Netlist", "Power"]:
            # Each edition and P&R tool has its own set of representative files
            _tool_options = tool_options.copy()

            if pnr != "Quartus":
                _tool_options["pnr"] = pnr.lower()

            # Ensure we test the edition we intend to, even if quartus_sh is
            # present
            os.environ["FUSESOC_QUARTUS_EDITION"] = edition

            tf = make_edalize_test('quartus',
                                   param_types=['vlogdefine', 'vlogparam'],
                                   tool_options=_tool_options,
                                   ref_dir=edition)

            # Each edition performs checks on the QSYS files present, so
            # provide a minimal example
            with open(os.path.join(tf.work_root, "qsys_file"), 'w') as f:
                f.write(qsys_file.format(qsys_fill[edition]))

            tf.backend.configure()
            tf.compare_files(['Makefile', tf.test_name + '.tcl'])

            tf.backend.build()
            tf.compare_files(test_sets[edition][pnr])
