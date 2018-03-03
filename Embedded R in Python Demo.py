import rpy2.robjects as r
import numpy as  np



r.require("splines")

r.reval("x = rnorm(5)")
r.reval("x = bs( x, df = 5)")
np.array( list(r.r.x))

m = r.bs( x, df = 5)



r.reval('m1 <- c(1:10)')
r.reval("m2 <- matrix(as.complex(m1), nrow=5)")
np.array(list(r.r.m2)).reshape(r.r.m2.dim)
