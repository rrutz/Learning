install.packages("glmnet")
library(glmnet)

heartData <- read.csv("C:/Users/Ruedi/OneDrive/R/Classification/Logistic Regression/SAheart.data")
heartData$row.names <- NULL
heartData$chd <- as.factor(heartData$chd)
heartData$famhist <- as.numeric(heartData$famhist != "Absent")
x = as.matrix(heartData[,1:9])
fit <- glm( heartData$chd ~ 1 + x[, 1:3]+ x[,5] + x[,7:9], family = "binomial" )



