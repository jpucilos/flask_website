import math
import numpy
import matplotlib.pyplot as plt


def rayleigh_fade(f0, v, n, fs):
    #if inproper input
    #if f0 or v or n or fs == 0:
    #    f0 = 800
    #    v = 25
    #    n = 9
    #    fs = 20

    v = v/2.23694
    wavelength = 300.0 / float(f0)
    t = []
    r= []
    for k in range(1, int(100*fs / wavelength / v)):
        t.append(k * wavelength / fs * v)
        x = 0
        y = 0
        for i in range(1, 10):
            ri = numpy.random.normal(0,1,1)
            si = numpy.random.normal(0,1,1)
            phi = 2 * math.pi * i / n
            x += ri * math.cos(k*2*math.pi / fs * math.cos(phi)) - si * math.sin(k*2*math.pi / fs * math.cos(phi))
            y += si * math.cos(k*2*math.pi / fs * math.cos(phi)) - ri * math.sin(k*2*math.pi / fs * math.cos(phi))

        r.append(math.sqrt(x*x + y*y))
        plt.plot(t, r)

    plt.title("Rayleigh Fading Signal")
    plt.xlabel("Time (ms)")
    plt.ylabel("Signal Strength (dB)")
    plt.yscale('log')
    plt.grid(True)
    plt.savefig('/home/jpucilos/flask_website/static/rayleigh_fading.PNG')
    plt.gcf().clear()
    return