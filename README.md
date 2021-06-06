# Introduction

This repository contains a testing script for [nmigen-boards](https://github.com/nmigen/nmigen-boards) that tries to build blinky for all the platforms provided by [nmigen-boards](https://github.com/nmigen/nmigen-boards).
Since each FPGA requires a specific toolchain, the script tries to append the path to the toolchain to the `PATH` environment variable before building blinky.
These toolchain paths are read from `toolchains.txt`, for which an example can be found at `toolchains.txt.example`.
For each platform that successfully builds the script appends an entry to `boards.txt` containing the path, the name of the class, the checksum of the file defining the platform and the toolchain that was used to build blinky.
Upon every invocation of the test script, the `boards.txt` file is read to skip building blinky for the boards for which the file defining them has not been modified since the last successful build.

# Setup

To be able to build blinky for different FPGAs, you will need to have the following toolchains installed:

* [yosys](https://github.com/YosysHQ/yosys) + [nextpnr](https://github.com/YosysHQ/nextpnr) + [icestorm](https://github.com/YosysHQ/icestorm) (Lattice iCE40 FPGAs)
* [yosys](https://github.com/YosysHQ/yosys) + [nextpnr](https://github.com/YosysHQ/nextpnr) + [prjtrellis](https://github.com/YosysHQ/prjtrellis) (Lattice ECP5)
* [Lattice Diamond](http://www.latticesemi.com/latticediamond) (Lattice MachXO2)
* [Intel/Altera Quartus 20.1.1](https://fpgasoftware.intel.com/20.1.1/?edition=lite&platform=linux) (Intel/Altera Cyclone IV, V, 10 LP, MAX II, MAX V, MAX 10, Arria II FPGAs)
* [Intel/Altera Quartus 13.1](https://fpgasoftware.intel.com/13.1/?edition=web&platform=linux) (Intel/Altera Cyclone III)
* [Xilinx ISE 14.7 (WebPACK)](https://www.xilinx.com/downloadNav/vivado-design-tools/archive-ise.html) (Xilinx Spartan 3A, Spartan 6)
* [Xilinx Vivado 2020.1 (WebPACK)](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/2020-1.html) (Xilinx 7-series, UltraScale)

**Note**: it looks like Xilinx ISE is not required, as Xilinx Vivado seems to handle the same subset of FPGAs.

Also make sure you have the following programming tools installed:

* [dfu-util](http://dfu-util.sourceforge.net/)
* [merclpcl](https://github.com/cr1901/mercpcl)
* [openFPGAloader](https://github.com/trabucayre/openFPGALoader)
* [OpenOCD](http://openocd.org/)
* [xc3sprog](http://xc3sprog.sourceforge.net/)

You can specify the paths to the toolchains using `toolchains.txt`, of which an example can be found at `toolchains.txt.example`.

Finally, you will need to install [nmigen](https://github.com/nmigen/nmigen) and [nmigen-boards](https://github.com/nmigen/nmigen-boards):

```
virtualenv env --python=python3
source env/bin/activate
git clone https://github.com/nmigen/nmigen
cd nmigen
pip install --editable .[builtin-yosys]
cd ..
git clone https://github.com/nmigen/nmigen-boards
cd nmigen-boards
pip install --editable .[builtin-yosys]
cd ..
```

Then you should be able to run the test script as follows:

```
python test.py
```
