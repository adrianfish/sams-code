import numpy as np
import matplotlib.pyplot as pyplot

# PART (A)

# Here we first define the function to be integrated followed by the function to evaluate the 
# integral for conditions c.
def integrand(x_screen, x_aperture, c):
    return np.exp( c['waveno'] * 1j * (x_screen - x_aperture)**2 / (2*c['screendist']) )

def fresnel_integral(x_screen, c):

    assert c['intervals'] % 2 == 0, "number of intervals must be even."

    x_aperture = np.linspace(c['xapt_lower'], c['xapt_upper'], c['intervals']+1)
    dx_aperture = x_aperture[1] - x_aperture[0]
    sum_vals = np.zeros( len(x_aperture) )

    for i in range( len(x_aperture) ):
        sum_vals[i] = integrand(x_screen[i], x_aperture[i], c)

    return c['multiplier'] * dx_aperture/3 * \
           ( sum_vals[0] + np.sum(sum_vals[len(x_aperture)] + 4*sum_vals[1::2] + 2*sum_vals[2::2]) )

c = {
    'xapt_lower': -1e-5, 
    'xapt_upper': 1e-5,
    'waveno': 2 * np.pi / 1e-6,
    'screendist': 0.02,
    'intervals': 100,
    'E_0': 1
    }

c['multiplier'] = c['waveno'] * c['E_0'] / (2 * np.pi * c['screendist'])

x_screen = np.linspace(-5e-3, 5e-3, c['intervals'])

def plotdata(x_screen, c):
    intensity = np.zeros( len(x_screen) ) 

    for i in range( len(x_screen) ):
        intensity[i] = ( abs(fresnel_integral(x_screen[i], c)) )**2
    
    return intensity
intensitydata = plotdata(x_screen, c)
pyplot.plot(intensitydata, x_screen)
pyplot.xlabel('Screen coordinate (m)')
pyplot.ylabel('Relative intensity')
pyplot.show()
pyplot.savefig('1d_intensity.png')
