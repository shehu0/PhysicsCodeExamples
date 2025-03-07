# Adapted from
# https://docs.scipy.org/doc/scipy/tutorial/stats/sampling.html
# for
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon
from scipy.stats.sampling import TransformedDensityRejection
from math import exp


class BoltmannDistribution:
    def pdf(self, p):
        # temperature is T = 100
        return exp(-p / 100)  # take scipy.constants.Boltzmann  = 1

    def dpdf(self, p):
        # temperature is T = 100
        return -1 / 100.0 * exp(-p / 100)


dist = BoltmannDistribution()
urng = np.random.default_rng()
rng = TransformedDensityRejection(dist, domain=(10, 1000), random_state=urng)
rvs = rng.rvs(size=1000)

x = np.linspace(10, 1000, num=1000)
fx = expon.pdf(x, 0, 100)
fx2 = expon.pdf(x, 0, 50)  # illustration with temperature T = 50
#
# The probability density function for `expon` is:
# .. math::
#     f(x) = \exp(-x)
# for :math:`x \ge 0`.
# ``expon.pdf(x, loc, scale)`` is identically
# equivalent to ``expon.pdf(y) / scale`` with
# ``y = (x - loc) / scale``.

plt.plot(x, fx, "r-", lw=2, label="true Boltzmann distribution")
plt.plot(x, fx2, "y-", lw=2, label="true lower temperature Boltzmann distribution")
plt.hist(
    rvs, bins=30, density=True, alpha=0.8, label="sample from Boltzmann distribution"
)
plt.xlabel("p")
plt.ylabel("PDF(p)")
plt.title("Sampling from Boltzmann distribution")
plt.legend()
plt.show()
# plt.savefig('eg_sampling.png')
