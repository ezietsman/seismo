---
layout: default
---



## Note

<p>The aim is to have a small set of tools that will allow
me to extract frequencies from an unevenly sampled dataset e.g. Kepler
lightcurve. This requires a LOT of processing power, which is why there are
multiple parallel implementations of the O(N^2) Deeming periodogram, including
one that runs on my GPU via <code>opencl</code>. That one is
<strong>FAST</strong>.</p>

<h2>
    <a name="modules" class="anchor" href="#modules"><span class="octicon octicon-link"></span></a>Modules</h2>

<p>seismo contains the following modules:</p>

<ul>
    <li>timeseries - contains some DFT implementations</li>
    <li>fitting - will contain frequency fitting routines</li>
</ul><h2>
    <a name="tests" class="anchor" href="#tests"><span class="octicon octicon-link"></span></a>Tests</h2>

<p>Run the tests with:</p>

<pre><code>py.test tests
</code></pre>

<h2>
    <a name="goals" class="anchor" href="#goals"><span class="octicon octicon-link"></span></a>Goals</h2>

<p>Kepler datasets can be very long and contain many datapoints. These take a long
time to calculate via a naive O(N^2) algorithm (but needed because I don't have
a better algorithm for unevenly sampled data that I'm happy with). For this
reason I'm trying to create something that can run more or less with only some
user input, so that I can let it run by itself and save each step in the
output.</p>

<p>Each DFT for the particular dataset I'm interested in at the moment takes
about 50 minutes to run on my GTX 760, and about 16 hours on my MBP's i5 with 2
threads, and I may need to do 40 - 50 of them to extract all the frequencies.
(Donations for a Nvidia 980 welcome)</p>
