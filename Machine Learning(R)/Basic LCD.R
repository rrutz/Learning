#Basic LCD  

install.packages("ggplot2")
library("ggplot2")
install.packages("mvtnorm")
library("mvtnorm")
library(plyr)

# read in data
data <- read.csv("C:/Users/Ruedi/OneDrive/R/vowel.train")
data$row.names <- NULL
data$y <- as.factor(data$y)
y <- as.factor(data$y)
x <- data[, 3:12 ]

# descriptive statistics

N = nrow(x)
priors <- summary(y) / sum( summary(y) )
means <- ddply( data,  .(y), numcolwise(mean) )
data.sigma <- cov(x) / ( length(y) - ncol(x))

# classifies training data
prob <- data.frame( matrix(nrow = nrow(x), ncol = 0))
for( i in c(1:11) )
{
  w <- dmvnorm( x, mean = as.numeric(means[i, 2:11]), sigma = data.sigma )
  prob <- cbind( prob, data.frame( w ))
}
colnames(prob ) <- c(1,2,3,4,5,6,7,8,9,10,11)
classificaitons <- as.factor( unname( apply(prob, 1, FUN = which.max) ) )

# plot classifications ( only showing two coordinates )
ggplot() + geom_point( data = data, mapping = aes( x = x.1, y = x.2, colour = classificaitons) ) +
  geom_point(data = means, mapping = aes( x = x.1, y = x.2, colour =levels(classificaitons) ), size = 8 )

# error on trainin data
1 - sum(classificaitons == y) / N

# error on validation data
data_valid <- read.csv("C:/Users/Ruedi/OneDrive/R/vowel_valid.test")
x_v <- data_valid[, 3:12 ]
y_v <- as.factor(data_valid$y)

prob <- data.frame( matrix(nrow = nrow(x_v), ncol = 0))
for( i in c(1:11) )
{
  w <- dmvnorm( x_v, as.numeric(means[i, 2:11]), data.sigma )
  prob <- cbind(prob, w)
}
colnames(prob ) <- c(1,2,3,4,5,6,7,8,9,10,11)
classificaitons_v <- as.factor( unname( apply(prob, 1, FUN = which.max) ) )
1 - sum(classificaitons_v == y_v) / nrow(x_v)
