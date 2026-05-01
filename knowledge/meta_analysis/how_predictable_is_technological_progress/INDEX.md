---
document: how_predictable_is_technological_progress
generated: 2026-05-01T19:43:00Z
source_checksum: sha256:35c6af7feb22ffaf18f928c372eb40eedf78b0cab790b7a7b0cb73796a930839
total_lines: 694
depth: 3
section_count: 30
---

# how_predictable_is_technological_progress Index

## J Doyne Farmer[a][,][b][,][c] , Franc¸ ois Lafond[a][,][d][,][e][,][∗]
**Lines:** 29-42

Author affiliations and abstract for a paper by Doyne Farmer and François Lafond formulating Moore's law as a correlated geometric random walk with drift, applied to 53 technologies to derive a closed-form forecast error distribution, with solar PV as a demonstration case.

## 1 Introduction
**Lines:** 43-104

Introduces the paper's goal of deriving distributional (rather than point) forecasts for technology cost trajectories by reformulating Moore's Law as a geometric random walk with drift (extended to an IMA(1,1) process with autocorrelated noise), motivated by contrasting cost histories of coal, nuclear, and solar PV. Outlines the assumption that all technologies share the same stochastic process (with technology-specific drift/volatility), positions the approach against Wright's law and expert-opinion forecasting, and previews the paper's section structure.

## 2 Models
**Lines:** 105-106 | **Subsections:** 2.1, 2.2, 2.3, 2.4

I don't have the content of "Section 2: Models" — could you point me to the file path, or paste the section text? Without seeing the actual content, I can't summarize what concepts or definitions it contains.

### 2.1 Geometric random walk
**Lines:** 107-142

Introduces the geometric random walk with drift as the preferred stochastic formulation of Moore's law (Eq. 2: $y_t = y_{t-1} + \mu + n_t$), contrasting it with the trend-stationary regression model (Eq. 1) and showing that random-walk shocks accumulate over time so forecast errors grow with horizon. Defines core variables ($p_t$ cost, $\mu$ drift, $n_t$ i.i.d. noise, $y_t = \log p_t$) and motivates pooling errors across technologies via a generalized error-distribution formula that accommodates autocorrelation.

### 2.2 Prediction of forecast errors
**Lines:** 143-194

Derives the forecast error formula for the geometric random walk model: decomposes error into a diffusion term (accumulated noise) and an estimation term (mean error), yielding the normalized mean squared error Ξ(τ) = (m-1)/(m-3)·(τ + τ²/m) and showing the standardized error follows a Student t(m-1) distribution independent of technology-specific parameters. Introduces Eqs. (4)-(10), variables μ, K, τ, m, and the pooling property that enables aggregating forecast errors across technologies and horizons.

### 2.3 Generalization for autocorrelation
**Lines:** 195-232

Covers the IMA(1,1) generalization of the random walk forecast model to handle autocorrelated errors, deriving the variance term $K^2 = (1+\theta^2)\sigma^2$, the forecast error distribution coefficient $A^*$ (Eq. 13), the expected mean squared normalized error (Eq. 14), the rescaled error t-distribution (Eq. 15), and the resulting distributional forecast for future log-cost (Eq. 16).

### 2.4 Alternative hypotheses
**Lines:** 233-236

Covers alternative model generalizations beyond autocorrelation — specifically heavy tails (rejected based on forecast error evidence in Appendix C.4) and long-memory (deemed plausible due to nonstationarity but not pursued because the geometric random walk with normal noise and autocorrelation adequately fit the observed time-scaling of forecast errors).

## 3 Data
**Lines:** 237-238 | **Subsections:** 3.1, 3.2, 3.3

I don't have the contents of "Section 3: Data" — no document was attached or referenced in your message. Could you point me to the file (path or URL) you want summarized?

### 3.1 Data collection
**Lines:** 239-334

Section 3.1 describes the data collection methodology for a technological forecasting study, sourcing 66 technology cost time series primarily from the Santa Fe Institute's Performance Curve DataBase across sectors (chemistry, genomics, energy, hardware, consumer durables, food), and includes Table 5 with descriptive statistics and parameter estimates ($\hat{\mu}$, $p$-value, $\hat{K}$, $\hat{\sigma}$) ranked by improvement significance, noting 13 technologies (e.g., Crude.Oil, Nuclear.Electricity) are dropped for lacking statistically significant cost improvement.

### 3.2 Data selection and descriptive statistics
**Lines:** 335-343

Section 3.2 covers data selection criteria for the technology forecasting analysis: applying a one-sided t-test on first-difference log series at 10% confidence to filter out technologies without statistically significant improvement rates, and introduces notation conventions (hat for window estimates, tilde for full-sample estimates) along with Table 1's p-values, drift estimates $\hat{\mu}_j$, and standard deviations $\hat{K}_j$.

### 3.3 Relation between drift and volatility
**Lines:** 344-347

Covers the empirical relationship between volatility ($\hat{K}_j$) and improvement rate ($-\hat{\mu}_j$) across technologies, reporting a linear fit ($\tilde{K} = 0.02 - 0.76\tilde{\mu}_j$, R²=0.87) and a log-log fit ($\tilde{K} = e^{-0.98}(-\tilde{\mu})^{0.73}$, R²=0.73), and proposes risk-return trade-off or fluctuation-scaling interpretations.

## 4 Estimation procedures
**Lines:** 348-349 | **Subsections:** 4.1, 4.2

I don't have the content of Section 4 to summarize — you've given me only the section title. Could you share the document or paste the section text? Likely candidates given the project context: - A specific file in `knowledge/meta_analysis/` (several new untracked dirs there) - A section of an extracted source's `output.md` - A chapter in the KerML/SysML spec If you point me to the path, I'll read it and produce the 1-2 sentence summary.

### 4.1 Statistical validation
**Lines:** 350-377

Covers the hindcasting (backtesting) procedure for statistical validation of the forecast model: rolling-window parameter estimation with $m=5$ recent observations, exhaustive forecast generation across feasible origin years $t_0$ and horizons $\tau$ (capped at $\tau_{\max}=20$), and a surrogate-data Monte Carlo procedure for null-distribution testing to handle approximation error, autocorrelation from overlapping windows, and finite-sample fluctuations.

### 4.2 Parameter estimation
**Lines:** 378-397

Covers parameter estimation for the forecasting model: rolling-window estimators for drift $\hat{\mu}_{t_0}$ (Eq. 17, telescoping sample mean of first differences) and volatility $\hat{K}_{t_0}^2$ (Eq. 18, unbiased estimator), plus two methods for setting a global autocorrelation parameter $\theta$ — error-matched ($\hat{\theta}_m = 0.63$) and weighted-average ($\hat{\theta}_w = 0.25$) — justified via a bias-variance tradeoff given short time series.

## 5 Comparison of models to data
**Lines:** 398-409 | **Subsections:** 5.1, 5.2, 5.3, 5.4

Introduces Section 5 of a forecasting paper, listing five empirical questions used to compare the model to data: scaling law of forecast errors over time (Eqs. 8 and 14), existence and sign of parameter θ under the null hypothesis, agreement of collapsed normalized errors with the Student distribution (Eq. 15), error scaling with trailing sample size m under stationarity, and model specification.

### 5.1 Normalized forecast errors as a function of $\tau$
**Lines:** 410-425

Covers empirical validation of the forecast error model by comparing the mean squared normalized forecast error Ξ(τ) (Eq. 14) against predictions for three autocorrelation values (θ=0, θ_w=0.25, θ_w=0.63), finding that θ_w=0.63 best matches empirical data across τ≤20 and that θ=0 is statistically rejected. Includes Figure 6, the surrogate data significance testing procedure, and justification for using Bessel's correction over the maximum likelihood estimator due to small sample size m.

### 5.2 Distribution of forecast errors
**Lines:** 426-443

Covers empirical validation of forecast error distributions against the predicted Student distribution using rescaled errors (Eq. 15) with autocorrelation parameter θ̂_w = 0.63, presenting Figs. 7-8 and surrogate-data hypothesis tests that accept θ = 0.63 while rejecting θ = 0.25 and θ = 0.

### 5.3 Dependence on sample size m
**Lines:** 444-451

Covers Section 5.3 on choosing the trailing sample size $m$ for forecasts, comparing stationary vs. nonstationary process assumptions and concluding via Fig. 9 experiments that errors decrease with larger $m$ (best choice $m=16$ here, possibly higher with longer time series), benchmarked against the $\theta_m = 0.63$ model.

### 5.4 Is the model well-specified?
**Lines:** 452-461

Section 5.4 examines whether the forecasting model is well-specified given short time series, noting that technology-specific values of the autocorrelation parameter θ cannot be reliably estimated and a global θ_m must be used (≈0.25 from case averaging vs. ≈0.63 needed to match empirical forecast errors). It argues the global-θ model is likely mis-specified due to expected technology-specific variation (analogous to μ_i and K_i), but concludes the simple model still matches observed forecasting errors reasonably well, with Figure 9 showing mean squared normalized forecast error Ξ vs. horizon τ for trailing sample sizes m = 4, 8, 12, 16.

## 6 Application to solar PV modules
**Lines:** 462-465 | **Subsections:** 6.1, 6.2, 6.3

Provides a distributional forecast for solar PV module prices and demonstrates using it to estimate the probability that one technology will be cheaper than a competing technology at a given time horizon.

### 6.1 A distributional forecast for solar energy
**Lines:** 466-487

Covers a distributional forecast for solar PV module costs through 2030 using Eq. (19) (the autocorrelated geometric random walk with parameters μ₃=-0.10, K₃=0.15, θ=0.63, m=33 years) and includes Figures 10-11 showing predicted price distributions and the probability of solar PV undercutting a hypothetical competing technology.

### 6.2 Estimating the probability that one technology will be less expensive than another
**Lines:** 488-505

Covers Section 6.2's derivation of the probability that one technology becomes cheaper than another by treating the log-cost difference $Z = y_C - y_S$ as normally distributed and expressing $Pr(y_S < y_C)$ via the error function (Eq. 20), illustrated with a photovoltaic-vs-hypothetical-competitor example.

### 6.3 Discussion of PV relative to coal-fired electricity and nuclear power
**Lines:** 506-521

Covers a comparative cost discussion of solar PV against coal-fired electricity (citing McNerney et al. 2011 on plant cost trends and fuel-cost floors) and nuclear power (comparing 2013–2014 PV LCOE figures of $0.06–0.16/kWh to Hinkley Point's projected $0.14/kWh), and argues that pooling forecast errors across many technologies enables reliable distributional forecasts and policy-relevant uncertainty bounds beyond Moore's-law-style extrapolation.

## 7 Conclusion
**Lines:** 522-549

Concludes the paper by summarizing the proposed autocorrelated geometric random walk method for distributional technology forecasting, with footnotes comparing solar PV price drops to fossil fuels/minerals, acknowledgements of contributors and funding (EU FP7 GROWTHCOM, US DOE, INET), and Appendix A listing data sources (Santa-Fe Performance Curve Database, photovoltaic price releases, nuclear data from Koomey/Hultman and Cooper, DNA sequencing from Wetterstrand).

### B.1 Random walk with drift
**Lines:** 550-581

Derives the distribution of forecast errors for a random walk with drift model, showing they follow a Gaussian distribution with variance $K^2(\tau + \tau^2/m)$ and, after accounting for estimated variance, a Student t-distribution with $m-1$ degrees of freedom (Eqs. 21-26).

### B.2 Integrated moving average
**Lines:** 582-621

Derives the forecast error distribution for an IMA(1,1) process when forecasts assume a random walk with drift, producing the variance expression σ² (Eq. 13) and extending to estimated-variance results (Eqs. 14–15) under the independence assumption from Appendix B.1.

### C.1 Size of the learning window
**Lines:** 622-625

Covers the robustness check on learning window size $m$ for forecast errors across different horizons, noting the lower bound $m=4$ (since $m=3$ yields infinite variance in the Student distribution with 2 degrees of freedom) and referencing Figs. 9 and 13 which show normalized mean squared forecast error decreasing as $m$ grows.

### C.2 Data selection
**Lines:** 626-629

Demonstrates robustness of normalized mean squared forecast error growth under random data subsampling, using 10,000 trials that each remove half of the technologies, with results shown in Fig. 14.

### C.3 Increasing $\tau_{max}$
**Lines:** 630-633

Section C.3 examines the effect of extending the forecast horizon $\tau_{max}$ from 20 to 73, showing via Fig. 15 that using all forecast errors up to the maximum horizon does not significantly change the empirical error distribution or the estimate of $\theta$ from Appendix B.

### C.4 Heavy tail innovations
**Lines:** 634-694

Covers Appendix C.4 (heavy-tail/Student-distributed noise innovations and their limited effect on long-horizon forecast errors), Appendix D (three methods for selecting the autocorrelation parameter θ, yielding values like θ=0.25 and θ=0.63), Appendix E (statistical comparison of empirical rescaled forecast errors against the predicted Student distribution via surrogate datasets and p-values), Appendix F (a trend extrapolation projecting solar PV reaching 20% of global energy by 2027), and the paper's full References list.
