# AUTOGENERATED! DO NOT EDIT! File to edit: 00_models.ipynb (unless otherwise specified).

__all__ = ['SIR']

# Cell
import attr
import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp
import seaborn as sns
sns.set(style="ticks")

@attr.s
class SIR(object):
    N = attr.ib(converter=int)
    I = attr.ib(converter=float)
    beta = attr.ib(converter=float)
    gamma = attr.ib(converter=float)
    days = attr.ib(converter=int, default=200)

    S = attr.ib(init=False, converter=float)

    R = attr.ib(init=False, converter=float, default=0.0)


    def __attrs_post_init__(self):
        self.S = self.N - self.I - self.R


    @staticmethod
    def ode(t, y, beta, gamma, N):
        S, I, R = y

        new_cases = beta*S*I/N
        removed_cases = gamma*I
        S = -new_cases
        I = new_cases - removed_cases
        R = removed_cases

        y = (S,I,R)

        return y

    def solve_days(self):
        y = (self.S, self.I, self.R)
        return solve_ivp(SIR.ode, [0,self.days], y,t_eval=np.arange(0,self.days), args=(self.beta, self.gamma, self.N))


    def plot(self):
        sol = self.solve_days()
        df_sol = pd.DataFrame(sol.y.T, index=sol.t, columns=["S","I","R"])
        sns.lineplot(data=df_sol)
