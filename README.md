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


## Modules

seismo contains the following modules:

* timeseries - contains some DFT implementations
* fitting - will contain frequency fitting routines

## Tests
Run the tests with:

    py.test tests


## Goals

Kepler datasets can be very long and contain many datapoints. These take a long
time to calculate via a naive O(N^2) algorithm (but needed because I don't have
a better algorithm for unevenly sampled data that I'm happy with). For this
reason I'm trying to create something that can run more or less with only some
user input, so that I can let it run by itself and save each step in the
output.

Each DFT for the particular dataset I'm interested in takes about 50min to run
on my GTX 760, and about 16 hours on my MBP's i5 with 2 threads, and I may need to do 40 - 50 of them to extract all the
frequencies. (Donations for a Nvidia 980 welcome)
