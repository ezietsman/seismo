seismo
======

Visit the [homepage](http://ezietsman.github.io/seismo)


This started as a place to keep my asteroseismology-related stuff

## Note

I just started this but the aim is to have a small set of tools that will allow
me to extract frequencies from an unevenly sampled dataset e.g. Kepler
lightcurve. This requires a LOT of processing power, which is why there are
multiple parallel implementations of the O(N^2) Deeming periodogram, including
one that runs on my GPU via `opencl`.


# Installation

Make sure you have `pip` installed.

On OSX I use [homebrew](http://brew.sh/). If you have not, install `python` from there first then install pip.

    (optional) brew install python
    brew install pip

On Debian/Ubuntu

    sudo apt-get install python-pip
    
Once pip is installed, install `seismo` with:

    pip install -r requirements.txt
    pip install .

in this folder.

You may need `sudo` for the last command


## Running the unit tests

To see if the installation completed successfully, run:

    py.test tests

This should give some output and all the tests should pass.


## Notes about OpenCL and GPU calculations

To use the [OpenCL](https://www.khronos.org/opencl/) extensions, you need an
OpenCL driver installed for each different device. On OSX this is installed
already, on Linux it is not. For NVIDIA users, one is installed with the CUDA
SDK, I do not know what is needed for AMD cards and CPUs. *NOTE* You do NOT
need the CUDA SDK for the opencl driver.


## Modules

seismo contains the following modules:

* timeseries - contains some DFT implementations
* fitting - will contain frequency fitting and extraction routines


## Goals

Kepler datasets can be very long and contain many datapoints. These take a long
time to calculate via a naive O(N^2) algorithm (but needed because I don't have
a better algorithm for unevenly sampled data that I'm happy with). For this
reason I'm trying to create something that can run more or less with only some
user input, so that I can let it run by itself and save each step in the
output.

Each DFT for the particular dataset I'm interested in takes about 50min to run
on my GTX 760, and about 16 hours on my MBP's i5 with 2 threads, and I may need
to do 40 - 50 of them to extract all the frequencies. (Donations for a Nvidia
980 welcome)


## Changes:

Version 0.1.2:
    * Added `deeming` function that wraps the dft implementations.
    * Updated examples
    * added tests
