import matplotlib
from matplotlib.pyplot import subplot, plot, show
from numpy import linspace, sin, pi, random
import seismo

matplotlib.style.use('ggplot')

x = linspace(0, 0.05, 500)
y = 0.6*sin(2*pi*240*x) + 0.2*random.randn(x.size)

f, a = seismo.deeming(x, y)
fmax, amax = seismo.find_peak(f, a)

signal = seismo.signal()
comp1 = seismo.sinewave(amax, fmax, 0)

signal.add_component(comp1)

signal.fit(x, y)

plot(x, y, '.')
plot(x, signal.evaluate(x), lw=2)
show()
