from numpy import sin, cos, pi, sqrt, tan, arctan, arccos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

m = 1.0
a = 0.0
v0 = 10.0
B = 0.0
h = 20.0

dt = 0.004 #długość kroku czasowego

g = 9.8 #przysp. ziemskie
m = float(input("Proszę podać masę [kg]: "))
h = float(input("Proszę podać wysokość [m]: "))
B = float(input("Proszę podać współczynnik oporu aerodynamicznego: "))
v0 = float(input("Proszę podać prędkość początkową [m/s]: "))
a = float(input("Proszę podać kąt między prędkością, a osią X [rad]: "))
x = []
y = []
x.append(0.0)
y.append(h)

vx = v0*cos(a)
vy = v0*sin(a)

maxx = 0.0
minx = 0.0
maxy = 0.0

j = 0
while(y[j] > 0): #wykonuje krok w czasie
    dvx = (-1)*(B*sqrt(abs(vx**2 + vy**2))*vx*dt)/m
    dvy = (-1)*(B*sqrt(abs(vx**2 + vy**2))*vy*dt)/m - g*dt
    
    dx = vx*dt
    dy = vy*dt
    x.append(x[j] + dx)
    y.append(y[j] + dy)
    maxx = max(maxx, x[j])
    maxy = max(maxy, y[j])
    minx = min(minx, x[j])
    vx = vx + dvx
    vy = vy + dvy
    j += 1

fig = plt.figure(figsize = (5, 5))
ax = fig.add_subplot(111, autoscale_on=True, xlim=(minx - 1, maxx + 1), ylim=(-0.3, maxy+1))
ax.grid()
ax.set_ylabel('Wysokość nad ziemią [m]')
ax.set_title('Odległość pozioma [m]')

line, = ax.plot([], [], 'o-', lw=6)
trace, = ax.plot([], [], ',-', lw=1)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=10000), deque(maxlen=10000)

def init():
    line.set_data([], [])
    trace.set_data([], [])
    time_text.set_text('')
    return line, trace, time_text

def animate(i):
    thisx = [x[i]]
    thisy = [y[i]]
    line.set_data(thisx, thisy)

    if i == 1:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(thisx[0])
    history_y.appendleft(thisy[0])

    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))

    return line, trace, time_text
if v0 == 0:
    v0 = 1
ani = animation.FuncAnimation(fig, animate, np.arange(1, j), interval=dt*300/(0.1*v0), blit=True, init_func=init)
plt.show()

