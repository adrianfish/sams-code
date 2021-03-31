import numpy as np
import matplotlib.pyplot as pyplot
# fuck all clue what I'm doing so just chucking out these definitions
def f1(vx):
    return vx
def f2(vy):
    return vy
def f3(x, y, c):
    return ((-c['g'] * c['M'] * x) / ((x ** 2 + y ** 2) ** (3 / 2))
def f4(x, y, c):
    return ((-c['g'] * c['M'] * y) / ((x ** 2 + y ** 2) ** (3 / 2))
# BANTERRRR
def simulation(c):
    t = np.linspace(0, c['endtime'])
    h = t[1] - t[0]                

    x = np.zeros(c['points'])   
    y = np.zeros(c['points'])
    vx = np.zeros(c['points'])   
    vy = np.zeros(c['points'])
    x[0], y[0] = c['x_initial'], c['y_initial']
    vx[0], vy[0] = c['vx_initial'], c['vy_initial']

    for i in range(1, c['points']):
        k1_x = f1(vx[i])
        k1_y = f2(vy[i])
        k1_vx = f3(x[i], y[i], c)
        k1_vy = f4(x[i], y[i], c)

        k2_x = f1(vx[i] + h * k1_vx / 2)
        k2_y = f2(vy[i] + h * k1_vy / 2)
        k2_vx = f3(x[i] + h * k1_x / 2, y[i] + h * k1_y / 2, c)
        k2_vy = f4(x[i] + h * k1_x / 2, y[i] + h * k1_y / 2, c)

        k3_x = f1(vx[i] + h * k2_vx / 2)
        k3_y = f2(vy[i] + h * k2_vy / 2)
        k3_vx = f3(x[i] + h * k2_x / 2, y[i] + h * k2_y / 2, c)
        k3_vy = f4(x[i] + h * k2_x / 2, y[i] + h * k2_y / 2, c)

        k4_x = f1(vx[i] + h * k3_vx)
        k4_y = f2(vy[i] + h * k3_vy)
        k4_vx = f3(x[i] + h * k3_x, y[i] + h * k3_y, c)
        k4_vy = f4(x[i] + h * k3_x, y[i] + h * k3_y, c)

        # it begins
        x[i] = x[i-1] + (h / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
        y[i] = y[i-1] + (h / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
        
        vx[i] = vx[i-1] + (h / 6) * (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx)
        vy[i] = vy[i-1] + (h / 6) * (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy)

    return (x, y)

conditions = {
    'g': 9.81,
    'M': 5.972e24,
    'endtime': 10,
    'x_initial': -100,
    'y_initial': 1, 
    'vx_initial': -1, 
    'vy_initial': 100,
    'points': 50,
}
x, y = simulation(conditions)
pyplot.plot(x, y)
pyplot.show()
