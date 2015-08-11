data {
    int<lower=0> N;
    real x1[N];   // CALL num
    real x2[N];   // RAISE num
    real x3[N];   // POT amount
    real x4[N];   // stack amount
    int<lower=0> y[N];  // 1:fold, 0:other action
}
transformed data {
    real<lower=0> x1_mean;
    real<lower=0> x2_mean;
    real<lower=0> x3_mean;
    real<lower=0> x4_mean;
    x1_mean <- mean(x1);
    x2_mean <- mean(x2);
    x3_mean <- mean(x3);
    x4_mean <- mean(x4);
}
parameters {
     real b0;     // intercept parameter
     real b1;     // parameter for CALL num
     real b2;     // parameter for RAISE num
     real b3;     // parameter for POT amount
     real b4;     // parameter for stack amount
}
transformed parameters {
    real q[N];
    for (i in 1:N) {
        q[i] <- inv_logit(b0 + b1*(x1[i]-x1_mean) + b2*(x2[i]-x2_mean) + b3*(x3[i]-x3_mean) + b4*(x4[i]-x4_mean));
    }
}
model {
    for (i in 1:N) {
        y[i] ~ bernoulli(q[i]);
    }
}
