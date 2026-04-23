# Data
target_n <- 95000
control_n <- 5000

target_fuelers <- 13522
control_fuelers <- 641

target_liters <- 411300
control_liters <- 17400

# Parameters
p1 <- target_fuelers / target_n 
p0 <- control_fuelers / control_n
mu1 <- target_liters / target_fuelers
mu0 <- control_liters / control_fuelers

cv <- 1 # try 0.8, 1.0, 1.2
sd1 <- cv * mu1
sd0 <- cv * mu0

# KPI 1: Conversion rate
out_kpi1 <- prop.test(
  x = c(target_fuelers, control_fuelers),
  n = c(target_n, control_n),
  alternative = "greater"
)

out_kpi1 <- c(
  control = p0,
  target  = p1,
  diff    = p1 - p0,
  diffpct = p1 / p0 - 1,
  p       = out_kpi1$p.value
)

# KPI 2: Avg liters per fueler
diff_kpi2 <- mu1 - mu0
se_kpi2   <- sqrt(sd1^2 / target_fuelers + sd0^2 / control_fuelers)
z_kpi2    <- diff_kpi2 / se_kpi2
p_kpi2    <- 2 * pnorm(-abs(z_kpi2))

out_kpi2 <- c(
  control = mu0,
  target  = mu1,
  diff    = diff_kpi2,
  diffpct = mu1 / mu0 - 1,
  p       = p_kpi2
)

# KPI 3: Avg liters per member (incl. non-fuelers)
m1 <- target_liters / target_n
m0 <- control_liters / control_n
diff_kpi3 <- m1 - m0

var1 <- p1 * (sd1^2) + p1 * (1 - p1) * (mu1^2)
var0 <- p0 * (sd0^2) + p0 * (1 - p0) * (mu0^2)

se_kpi3 <- sqrt(var1 / target_n + var0 / control_n)
z_kpi3  <- diff_kpi3 / se_kpi3
p2s_kpi3 <- 2 * pnorm(-abs(z_kpi3))
p1s_kpi3 <- 1 - pnorm(z_kpi3)

out_kpi3 <- c(
  control = m0,
  target  = m1,
  diff    = diff_kpi3,
  diffpct = m1 / m0 - 1,
  p       = p2s_kpi3
)

# Combine into dataframe
results_df <- data.frame(
  KPI     = c("KPI 1 - Conversion rate",
              "KPI 2 - Avg liters per fueler",
              "KPI 3 - Avg liters per member"),
  Control = c(out_kpi1["control"], out_kpi2["control"], out_kpi3["control"]),
  Target  = c(out_kpi1["target"],  out_kpi2["target"],  out_kpi3["target"]),
  Diff    = c(out_kpi1["diff"],    out_kpi2["diff"],    out_kpi3["diff"]),
  DiffPct = c(out_kpi1["diffpct"], out_kpi2["diffpct"], out_kpi3["diffpct"]),
  P_value = c(out_kpi1["p"],       out_kpi2["p"],       out_kpi3["p"])
)

print(results_df, row.names = FALSE)
