import matplotlib
from matplotlib.pyplot import subplot, plot, show
from numpy import linspace, sin, pi
import seismo

matplotlib.style.use('ggplot')

x = linspace(0, 0.05, 500)
y = 0.6*sin(2*pi*240*x)\
    + 0.15*sin(2*pi*1303*x + 0.4)\
    + 0.1*sin(2*pi*3000*x)

f, a = seismo.deeming(x, y)

subplot(211)
plot(x, y, '.')
subplot(212)
plot(f, a)

show()
