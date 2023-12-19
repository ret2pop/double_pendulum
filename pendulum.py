#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import random


class PendulumSystem:
    def __init__(
        self, r1=5, r2=1, m1=3, m2=2, phi=1.57, phi_dot=0.5, theta=3, theta_dot=1
    ):
        self.g = 9.8
        self.r2 = r2
        self.r1 = r1
        self.m1 = m1
        self.m2 = m2
        self.delta_t = 0.01
        self.phi = phi
        self.phi_dot = phi_dot
        self.theta = theta
        self.theta_dot = theta_dot

        self.Phi = [phi]
        self.Theta = [theta]
        self.ThetaDot = [theta_dot]
        self.PhiDot = [phi_dot]

        self.old_vars = [r1, r2, m1, m2, phi, phi_dot, theta, theta_dot]
        self.epoch = 0

        self.deltaphi_dot = 0
        self.delta_phi = 0
        self.deltatheta_dot = 0
        self.delta_theta = 0
        self.entropy = 0.2

    def populate(self, r):
        for i in range(r):
            self.update()

    def perturb(self):
        for i in range(len(self.old_vars)):
            self.old_vars[i] += random.random() * self.entropy * 2 - self.entropy

    def reset(self):
        self.r1 = self.old_vars[0]
        self.r2 = self.old_vars[1]
        self.m1 = self.old_vars[2]
        self.m2 = self.old_vars[3]
        self.phi = self.old_vars[4]
        self.phi_dot = self.old_vars[5]
        self.theta = self.old_vars[6]
        self.theta_dot = self.old_vars[7]
        self.Phi = [self.phi]
        self.Theta = [self.theta]
        self.ThetaDot = [self.theta_dot]
        self.PhiDot = [self.phi_dot]

        self.deltaphi_dot = 0
        self.delta_phi = 0
        self.deltatheta_dot = 0
        self.delta_theta = 0

        self.epoch += 1

    def update(self):
        self.deltaphi_dot = -(self.g * math.sin(self.phi) * self.delta_t) / self.r2
        self.phi_dot += self.deltaphi_dot
        self.PhiDot.append(self.phi_dot)
        self.delta_phi = self.phi_dot * self.delta_t
        self.deltatheta_dot = (
            self.m2 * self.g * math.cos(self.phi) * math.sin(self.phi - self.theta)
            - self.m1 * self.g * math.sin(self.theta)
        ) / (self.m1 * self.r1)

        self.theta_dot += self.deltatheta_dot
        self.ThetaDot.append(self.theta_dot)
        self.delta_theta = self.theta_dot * self.delta_t

        self.phi += self.delta_phi
        self.theta += self.delta_theta

        self.Phi.append(self.phi)
        self.Theta.append(self.theta)

    def graph(self):
        plt.plot(
            [i for i in range(len(self.Theta))],
            self.Theta,
            color=(
                "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            ),
            label=f"theta, epoch {self.epoch}",
        )
        # plt.plot(
        #     [i for i in range(len(self.Phi))],
        #     self.Phi,
        #     color=(
        #         "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        #     ),
        #     label=f"phi, epoch {self.epoch}",
        # )

    def phase_space(self):
        plt.plot(
            self.ThetaDot,
            self.Theta,
            color=(
                "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            ),
            label=f"Theta, epoch {self.epoch}",
        )
        plt.plot(
            self.PhiDot,
            self.Phi,
            color=(
                "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            ),
            label=f"Phi, epoch {self.epoch}",
        )


p = PendulumSystem(r1=5, r2=1, m1=3, m2=2, phi=1.57, phi_dot=1, theta=3, theta_dot=1)
steps = 500
epochs = 5

# original
p.populate(steps)
p.phase_space()

# pertubations
for i in range(epochs):
    p.perturb()
    p.reset()
    p.populate(steps)
    p.phase_space()

plt.xlabel("time derivatives")
plt.ylabel("phi, theta (radians)")
plt.legend()
plt.show()
