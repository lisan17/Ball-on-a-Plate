import numpy as np
from scipy.integrate import odeint

g = 9.8
Kc = -8
tauI = 1000.0
tauD = 8

# The following function gives the ordinary differential
# equation that our plant follows. Do not meddle with this.
def f(x, t, theta):
    return (x[1], (-5 * g / 7) * np.radians(theta))


# Write your function here.

def solve(x, SP, theta, x_vel, I_pre, t, e_pre):

    print("This point was reached with x value ", x)
    x_new = 0.0
    dx = 0.0
    e = SP - x
    print("error is ", e)
    dt = 0.04
    P = Kc * e
    I = I_pre + (Kc / tauI) * e * dt
    D = Kc * tauD * (e - e_pre) / dt
    print("The value of P, I, D terms are ", P, " ", I, " ", D)
    dtheta = P + I + D - theta
    print("The value of theta is ", theta)

    if dtheta > 1.0:
        dtheta = 1.0
    elif dtheta < -1.0:
        dtheta = -1.0

    new_theta = theta + dtheta
    if new_theta > 15.0:
        new_theta = 15.0
    elif new_theta < -15.0:
        new_theta = -15.0


    arr = [x, x_vel]
    print("The value of velocity of x ball is ", x_vel)
    print("The time is ", t)
    tf = [t, t + dt]

    y = odeint(f, arr, tf, args=(new_theta,))

    x_new = y[1][0]

    dx = x_new - x
    new_t = t + dt

    if (abs(x_vel-2)<0):
        new_t = 0.0
    sol = [dx, new_theta, new_t, I, y[1][1], e]
    return sol
