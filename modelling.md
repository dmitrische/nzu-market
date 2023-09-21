Assuming price dynamics follows [geometric Brownian motion (GBM)](https://en.wikipedia.org/wiki/Geometric_Brownian_motion), it can be simulated using a discrete-time [Markov chain Monte Carlo (MCMC)](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) by repeatedly applying the following recurrence relation, 

$$
p^{(t+1)} = p^{(t)}\exp(d+\xi^{(t)}), 
$$

where $t \in \{0,1,2,\dots\}$ indexes regular timesteps (which could represent days, months, or years), $d$ is a constant drift parameter, and $\xi^{(t)}$ is a normally distributed random variable, i.e. $\xi^{(t)} \sim \mathcal{N}(0,\sigma)$, with the standard deviation $\sigma$ (and variance $\sigma^{2}$) determining price volatility. Note that the underlying assumption here is that geometric returns will change in increments that are lognormally distributed, i.e.

$$
r^{(t+1)} := \ln\left(\frac{p^{(t+1)}}{p^{(t)}}\right) \sim \mathcal{N}(d,\sigma).
$$

The two parameters, $d$ and $\sigma$, can be inferred from data on past prices, i.e. a historical dataset $P_{H} = \{p^{(t)}, p^{(t-1)}, \dots, p^{(t-M)}\}$, from which $R_{H} = \{r^{(t)}, \dots, r^{(t-M+1)}\}$ can be calculated. The latter set of values will have an arithmetic mean $\mu_{r}$ and variance $\sigma_{r}^{2}$, calculated using 

$$
\mu_{r} = \frac{1}{M}\sum_{i=0}^{M-1}r^{(t-i)} \quad \mathrm{and} \quad \sigma_{r}^{2} = \frac{1}{M-1} \sum_{i=0}^{M-1} (r^{(t-i)} - \mu_{r})^{2},
$$

and the drift parameter can then be calculated using the formula

$$
d = \mu_{r} - \frac{\sigma_{r}^{2}}{2}. 
$$

A simulated Markov chain $i$ starting from $p^{(0)}$ at $t=0$ should end up at a value

$$
p_{i}^{(N)} = p^{(0)} \exp\left(Nd + \sum_{t=1}^{N}\xi^{(t)}\right)
$$

at $t=N$. Repeating the simulation starting with the same initial condition will produce another Markov chain $j$ with a different endpoint, i.e. $p_{j}^{(N)} \neq p_{i}^{(N)}$. Repeating the simulation sufficiently many times should reveal that the endpoints will be lognormally distributed with the mean value of $Nd_{r}$ and standard deviation of $\sqrt{N}\sigma_{r}$, i.e.

$$
\ln\left(\frac{p^{(N)}}{p^{(0)}}\right) \sim \mathcal{N}(Nd,\sqrt{N}\sigma_{r}).
$$

This knowledge enables us to make analytic projections into the future and plot probability isocontours, such as the drift line and the envelopes around it. 

Note that the GBM model can be extended to describe stochastic volatility, as in the [Heston model](https://en.wikipedia.org/wiki/Heston_model).
