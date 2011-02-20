#!==============================================
#! Examples of physical measurements
#!==============================================

import numpy
from pylab import *

from pacal import *
from pacal.distr import demo_distr


#!
#! coefficient of thermal expansion 
#!
L0 = UniformDistr(9,10)
L1 = UniformDistr(11,12)
dT = NormalDistr(1,2)
k = (L1/L0 - 1)/dT
k.plot(linewidth=3, color = "k")
k.hist(xmin=-1,xmax=1,color="0.75")
k.summary()
print "P(K<0) - NormalDistr(1,2).cdf(0) =", k.cdf(0)[0] - NormalDistr(1,2).cdf(0)[0]
xlim(-1,1)
ylim(ymin=0)
title("Distribution of thermal expansion coefficient")




#!
#! combining two independent measurements
#!

from scipy.optimize.optimize import fminbound


# E1 = UniformDistr(0,2)
# E2 = BetaDistr(2,2) 
# E2 = BetaDistr(0.5,0.5) 
E1 = UniformDistr(-1,1)
E2 = NormalDistr()
E1.summary()
E2.summary()


def E(alpha):
    alpha = numpy.squeeze(alpha)
    return alpha*E1 + (1 - alpha)*E2

print
print "Combining measurements for optimal variance"
alphaOptVar = fminbound(lambda alpha: E(alpha).var(), 0, 1, xtol = 1e-16)
print "alphaOptVar = ", alphaOptVar 
dopt = E(alphaOptVar)
dopt.summary()

print
print "Combining measurements for optimal Median Absolute Deviance"
alphaOptMad = fminbound(lambda alpha: E(alpha).medianad(), 0, 1, xtol = 1e-16)
print "alphaOptMAD = ", alphaOptMad 
dopt = E(alphaOptMad)
dopt.summary()

print
print "Combining measurements for optimal 95% confidence interval"
alphaOptIQrange = fminbound(lambda alpha: E(alpha).iqrange(0.025), 0, 1, xtol = 1e-16)
print "alphaOptIQrange = ", alphaOptIQrange 
dopt = E(alphaOptIQrange)
dopt.summary()

print "-----------------------"
figure()
E1.plot(color='k')
E2.plot(color='k')
E(alphaOptVar).plot(color='r')
E(alphaOptMad).plot(color='g')
E(alphaOptIQrange).plot(color='b')
figure()
E(alphaOptVar).get_piecewise_cdf().plot(color='r')
E(alphaOptMad).get_piecewise_cdf().plot(color='g')
E(alphaOptIQrange).get_piecewise_cdf().plot(color='b')
show()
