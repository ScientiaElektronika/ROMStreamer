# Copyright (C) 1991-2013 Altera Corporation
# Your use of Altera Corporation's design tools, logic functions 
# and other software and tools, and its AMPP partner logic 
# functions, and any output files from any of the foregoing 
# (including device programming or simulation files), and any 
# associated documentation or information are expressly subject 
# to the terms and conditions of the Altera Program License 
# Subscription Agreement, Altera MegaCore Function License 
# Agreement, or other applicable license agreement, including, 
# without limitation, that your use is for the sole purpose of 
# programming logic devices manufactured by Altera and sold by 
# Altera or its authorized distributors.  Please refer to the 
# applicable agreement for further details.

# Quartus II: Generate Tcl File for Project
# File: ROMStreamer.tcl
# Generated on: Mon Nov  3 20:31:59 2025

# Load Quartus II Tcl Project package
package require ::quartus::project

set need_to_close_project 0
set make_assignments 1

# Check that the right project is open
if {[is_project_open]} {
	if {[string compare $quartus(project) "ROMStreamer"]} {
		puts "Project ROMStreamer is not open"
		set make_assignments 0
	}
} else {
	# Only open if not already open
	if {[project_exists ROMStreamer]} {
		project_open -revision ROMStreamer ROMStreamer
	} else {
		project_new -revision ROMStreamer ROMStreamer
	}
	set need_to_close_project 1
}

# Make assignments
if {$make_assignments} {
	set_global_assignment -name FAMILY "Cyclone II"
	set_global_assignment -name DEVICE EP2C5T144C8
	set_global_assignment -name ORIGINAL_QUARTUS_VERSION "13.0 SP1"
	set_global_assignment -name PROJECT_CREATION_TIME_DATE "19:55:01  жовтня 19, 2025"
	set_global_assignment -name LAST_QUARTUS_VERSION "13.0 SP1"
	set_global_assignment -name VERILOG_FILE ROMStreamer.v
	set_global_assignment -name VERILOG_FILE image_ROM.v
	set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
	set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
	set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
	set_global_assignment -name ERROR_CHECK_FREQUENCY_DIVISOR 1
	set_global_assignment -name EDA_SIMULATION_TOOL "ModelSim-Altera (Verilog)"
	set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "VERILOG HDL" -section_id eda_simulation
	set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
	set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
	set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top
	set_global_assignment -name STRATIX_DEVICE_IO_STANDARD "3.3-V LVTTL"
	set_location_assignment PIN_144 -to i_rst_n
	set_location_assignment PIN_17 -to i_clk
	set_location_assignment PIN_143 -to o_DAC_Y[0]
	set_location_assignment PIN_63 -to o_DAC_X[8]
	set_location_assignment PIN_59 -to o_DAC_X[7]
	set_location_assignment PIN_57 -to o_DAC_X[6]
	set_location_assignment PIN_53 -to o_DAC_X[5]
	set_location_assignment PIN_51 -to o_DAC_X[4]
	set_location_assignment PIN_47 -to o_DAC_X[3]
	set_location_assignment PIN_44 -to o_DAC_X[2]
	set_location_assignment PIN_42 -to o_DAC_X[1]
	set_location_assignment PIN_40 -to o_DAC_X[0]
	set_location_assignment PIN_119 -to o_DAC_Y[8]
	set_location_assignment PIN_121 -to o_DAC_Y[7]
	set_location_assignment PIN_125 -to o_DAC_Y[6]
	set_location_assignment PIN_129 -to o_DAC_Y[5]
	set_location_assignment PIN_133 -to o_DAC_Y[4]
	set_location_assignment PIN_135 -to o_DAC_Y[3]
	set_location_assignment PIN_137 -to o_DAC_Y[2]
	set_location_assignment PIN_141 -to o_DAC_Y[1]
	set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top

	# Commit assignments
	export_assignments

	# Close project
	if {$need_to_close_project} {
		project_close
	}
}
