# Introduction

This repository contains a testing script for [nmigen-boards](https://github.com/nmigen/nmigen-boards) that tries to build blinky for all the platforms provided by [nmigen-boards](https://github.com/nmigen/nmigen-boards).
Since each FPGA requires a specific toolchain, the script tries to append the path to the toolchain to the `PATH` environment variable before building blinky.
These toolchain paths are read from `toolchains.txt`, for which an example can be found at `toolchains.txt.example`.
For each platform that successfully builds the script appends an entry to `boards.txt` containing the path, the name of the class, the checksum of the file defining the platform and the toolchain that was used to build blinky.
Upon every invocation of the test script, the `boards.txt` file is read to skip building blinky for the boards for which the file defining them has not been modified since the last successful build.
