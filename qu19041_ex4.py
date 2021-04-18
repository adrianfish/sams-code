import numpy as np
import matplotlib.pyplot as pyplot

choice = '0'
choice = input('Enter a choice, "a" for Earth orbit, or "b" for orbit of the Earth and the moon: ')

def earch_accel(x_or_y, x, y, c):
    return -(c['G'] * c['m_earth'] * x_or_y) / ((x ** 2 + y ** 2) ** (3 / 2))

if choice == 'a':
    def x_accel(x, y, c):
        #return -(c['G'] * c['m_earth'] * x) / ((x ** 2 + y ** 2) ** (3 / 2))
        return earth_accel(x, x, y, c)
    def y_accel(x, y, c):
        #return -(c['G'] * c['m_earth'] * y) / ((x ** 2 + y ** 2) ** (3 / 2))
        return earth_accel(y, x, y, c)

elif choice == 'b':
    def x_accel(x, y, c):
        #return -(c['G'] * c['m_earth'] * x) / ((x ** 2 + y ** 2) ** (3 / 2))\
        #        - (c['G'] * c['m_moon'] * x) / ((x ** 2 + (y - 3.844e8) ** 2) ** (3 / 2))
        return earch_accel(x, x, y, c)\
                - (c['G'] * c['m_moon'] * x) / ((x ** 2 + (y - 3.844e8) ** 2) ** (3 / 2))

    def y_accel(x, y, c):
        #return -(c['G'] * c['m_earth'] * y) / ((x ** 2 + y ** 2) ** (3 / 2))\
        #        - c['G'] * c['m_moon'] * (y - 3.844e8) / ((x ** 2 + (y - 3.844e8) ** 2) ** (3 / 2))
        return earch_accel(y, x, y, c)\
                - c['G'] * c['m_moon'] * (y - 3.844e8) / ((x ** 2 + (y - 3.844e8) ** 2) ** (3 / 2))
else:
    quit()

def simulate(c):
    t = np.linspace(0.0, c['endtime'], c['points'])
    dt = t[1] - t[0]                
    print(dt)
    x = np.zeros(c['points'])   
    y = np.zeros(c['points'])
    vx = np.zeros(c['points'])   
    vy = np.zeros(c['points'])
    x[0], y[0] = c['x_initial'], c['y_initial']
    vx[0], vy[0] = c['vx_initial'], c['vy_initial']

    for i in range(1, c['points']):
        k1_x = vx[i - 1]
        k1_y = vy[i - 1]
        k1_vx = x_accel(x[i - 1], y[i - 1], c)
        k1_vy = y_accel(x[i - 1], y[i - 1], c)

        k2_x = vx[i - 1] + dt * k1_vx / 2
        k2_y = vy[i - 1] + dt * k1_vy / 2
        k2_vx = x_accel(x[i - 1] + dt * k1_x / 2, y[i - 1] + dt * k1_y / 2, c)
        k2_vy = y_accel(x[i - 1] + dt * k1_x / 2, y[i - 1] + dt * k1_y / 2, c)

        k3_x = vx[i - 1] + dt * k2_vx / 2
        k3_y = vy[i - 1] + dt * k2_vy / 2
        k3_vx = x_accel(x[i - 1] + dt * k2_x / 2, y[i - 1] + dt * k2_y / 2, c)
        k3_vy = y_accel(x[i - 1] + dt * k2_x / 2, y[i - 1] + dt * k2_y / 2, c)

        k4_x = vx[i - 1] + dt * k3_vx
        k4_y = vy[i - 1] + dt * k3_vy
        k4_vx = x_accel(x[i - 1] + dt * k3_x, y[i - 1] + dt * k3_y, c)
        k4_vy = y_accel(x[i - 1] + dt * k3_x, y[i - 1] + dt * k3_y, c)

        # it begins
        x[i] = x[i - 1] + (dt / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
        y[i] = y[i - 1] + (dt / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
        
        vx[i] = vx[i - 1] + (dt / 6) * (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx)
        vy[i] = vy[i - 1] + (dt / 6) * (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy)
        
        # TESTS
        if np.sqrt(x[i] ** 2 + y[i] ** 2) <= 6371e3:
            print('The satellite has crashed into the Earth')
            break
        if choice == 'b':
            if np.sqrt(x[i] ** 2 + (y[i] - 4e8) ** 2) <= 1737.4e3:
                print('The satellite has crashed into the moon') 
                break
    return (x, y)

conditions = {
    'G': 6.67408e-11,
    'm_earth': 5.972e24,
    'm_moon': 7.3476e22,
    'endtime': 1500000,
#    'x_initial': 00,
    'x_initial': 9.7e6,
    'y_initial': 8.7e6,
#    'y_initial': -6.8e6, 
#    'vx_initial': 10722, 
    'vx_initial': 2430,
    'vy_initial': 7305,
#    'vy_initial': 0,
    'points': 150000,
}

x, y = simulate(conditions)

visual = pyplot.figure()
axes = visual.add_subplot(111)

pyplot.text(0, 0, 'Earth')
pyplot.plot([0], [0], 'bo')
if choice == 'b':
    pyplot.text(0, 4e8, 'Moon')
    pyplot.plot([0], [4e8], 'yo')
pyplot.plot(x, y)

axes.set_aspect('equal', adjustable='box')
pyplot.show()

