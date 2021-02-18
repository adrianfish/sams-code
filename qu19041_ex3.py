import numpy as np
import matplotlib.pyplot as pyplot

# PART (A)

def integrand(screen_coord, apt_coord, c):
    return np.exp( c['waveno'] * 1j * (screen_coord - apt_coord) ** 2 / (2 * c['screendist']) )

def fresnel_integral(screen_coord, apt, c):
    assert c['intervals'] % 2 == 0, "number of intervals must be even."

    aperture = np.linspace(apt['apt_lower'], apt['apt_upper'], c['intervals'] + 1)
    d_aperture = aperture[1] - aperture[0]
    sum_vals = np.zeros( len(aperture), dtype=np.complex_ )
    
    for i in range( len(aperture) ):
        sum_vals[i] = integrand(screen_coord, aperture[i], c)

    return c['multiplier'] * d_aperture/3 * \
    ( sum_vals[0] + np.sum(sum_vals[0:-1:2] + 4*sum_vals[1::2] + 2*sum_vals[2::2]))
#   -2*sum_vals[0:-1:2])) which values are getting picked

def plotdata(screenarray, apt, c):
    intensity = np.zeros( len(screenarray) ) 

    for i in range( len(x_screen) ):
        intensity[i] = ( abs(fresnel_integral(x_screen[i], apt, c)) ) ** 2
    return intensity

constants = {
    'waveno': 2 * np.pi / 1e-6,
    'screendist': 0.02,
    'intervals': 150,
    'E_0': 5.0
}

xapt = {
     'apt_lower': -1e-5, 
     'apt_upper': 1e-5,
}

constants['multiplier'] = constants['waveno'] * constants['E_0'] \
/(2 * np.pi * constants['screendist'])

x_screen = np.linspace(-5e-3, 5e-3, constants['intervals'] + 1)

pyplot.plot(x_screen, plotdata(x_screen, xapt, constants ))
pyplot.xlabel('Screen coordinate (m)')
pyplot.ylabel('Relative intensity')
pyplot.show()

# PART (C)

# dictionary for aperture in y direction
yapt = {
    'apt_lower': -1e-5,
    'apt_upper': 1e-5,
}

constants['multiplier'] = constants['waveno'] * constants['E_0'] \
/(2 * np.pi * constants['screendist'])

intensity = np.zeros( (constants['intervals'], constants['intervals']))
    
y_screen = np.linspace(-5e-3, 5e-3, constants['intervals'] + 1)

for i in range(constants['intervals']):
    for j in range(constants['intervals']):
        intensity[i, j] = abs(fresnel_integral(x_screen[i], xapt, constants) *
                          fresnel_integral(y_screen[j], yapt, constants) \
                          / constants['multiplier']) ** 2 

pyplot.set_cmap("pink")
pyplot.imshow(intensity)
pyplot.show()

