core support differences
```{r}

data <- left_join(county_Data$voting_Data, county_Data$county_Info, by='fips' )

data[,'Population' ] <- log(data[,'Population' ]+0.5 )
data[,'Population density' ] <- log(data[,'Population density' ]+0.5 ) 
predictors <- colnames(county_Data$county_Info )[4:length(county_Data$county_Info)]

coreDem <- list( data = data[ data$per_point_diff_2016 >= 0.0, ] )
coreDem[['diff']] <- coreDem$data$per_point_diff_2016
coreDem[['X']] <- coreDem$data[, predictors] 
coreDem[['n']] <- nrow(coreDem$data)
coreDem[['means']] <- colMeans( coreDem$X )
coreDem[['var']] <-  diag( var( coreDem$X ) )


coreRep <- list(data = data[ data$per_point_diff_2016 < -0.0,  ])
coreRep[['diff']] <- coreRep$data$per_point_diff_2016
coreRep[['X']] <- coreRep$data[, predictors ]
coreRep[['n']] <- nrow(coreRep$data)
coreRep[['means']] <- colMeans( coreRep$X )
coreRep[['var']] <-  diag( var( coreRep$X ) )


diff <- list( mean = coreDem$means - coreRep$means )
diff[['se']] <- numeric( length = length(colnames(coreDem$X)))
names(diff$se) <- colnames(coreDem$X)
diff[['p-value']] <- numeric( length = length(colnames(coreDem$X)))
names(diff$`p-value`) <- colnames(coreDem$X)

local( 
  for( name in colnames(coreDem$X) )
  {
    if( grepl('%', name))
    {
      p.dem <- coreDem$means[name]; q.dem = 1 - p.dem
      p.rep <- coreRep$means[name]; q.rep = 1 - p.rep
      se <- ( p.dem*q.dem / coreDem$n + p.rep*q.rep / coreRep$n )**0.5 
    } else
    {
      se <- ( coreDem$var[name] / coreDem$n + coreRep$var[name] / coreRep$n )**0.5
    }
    diff$se[name] <<- se
    diff$`p-value`[name] <<- 2* (1-pnorm(abs(diff$mean[name]) / se) )
  }
)


signDiff <- names( sort( diff$`p-value`[ diff$`p-value` < .05/length(colnames(coreDem$X)) ]))
print(signDiff)

sort( abs(as.data.frame (round( cor(y, x[,signDiff]), 2)) ))
round( cor(y, x[,signDiff]), 2)  

round( cor( rbind( coreDem$X[, signDiff], coreRep$X[, signDiff] ) ), 2)

```





From this we see that we should further 

```{r}

coreRep$data <- coreRep$data[sample(nrow(coreRep$data),500),]
sideBySidePlot <- function(x_name, xAxis.low, xAxis.high, yAxis.rouding, yAxis.name )
{
  
  g1 <- ggplot() +
    geom_histogram( aes(x = coreDem$data[,x_name], y=..count../sum(..count..)),  alpha = 0.5, color='blue', fill='blue', bins=30 ) +
    coord_cartesian( xlim=c(xAxis.low,xAxis.high)) +
    scale_y_continuous(labels=function(x){ sprintf( paste("%.",yAxis.rouding,"f"),x)}) +
    theme(axis.title=element_blank(),
          axis.text.x=element_blank())
  
  g2 <- ggplot() +
    geom_histogram( aes(x = coreRep$data[,x_name], y=..count../sum(..count..)),  alpha = 0.5, color='red', fill='red' ) +
    coord_cartesian( xlim=c(xAxis.low,xAxis.high)) +
    scale_y_continuous(labels=function(x){ sprintf( paste("%.",yAxis.rouding,"f"),x)}) +
    theme(axis.title=element_blank())
  
  grid.arrange(g1,g2, nrow=2, left=yAxis.name)
  
}

sideBySidePlot( "Race: Black (%)", 0, 1, 2, "Relative Frequency (%)" )
sideBySidePlot( "Income: household income", min(coreDem$data$`Income: household income`),  max(coreRep$data$`Income: household income`), 0, "Relative Frequency (%)" )

sideBySidePlot( "Population density", 
                min( c(coreDem$data$`Population density`, coreRep$data$`Population density`)),  
                5000, 2, "Relative Frequency (%)" )


ggplot( df, aes( x=`Bachelors (%)`, x =`Population density` ) ) + geom_point( aes(color = dem)) +
  scale_colour_gradient(low="red", high="black") 


ggplot() +
  geom_histogram( aes(x = county_Data$`Bachelors (%)`, y=..count../sum(..count..)),  alpha = 0.5, color='blue', fill='blue', bins=30 )

```






```{r}
-------
  predictors <- colnames(county_Data$county_Info )[4:length(county_Data$county_Info)]
repData <- left_join(repData, county_Data$county_Info, by='fips' )

y <- repData$per_point_diff_2016
x <- repData[, predictors]


sideBySidePlot <- function(x_name, xAxis.low, xAxis.high, yAxis.rouding, yAxis.name )
{
  
  g1 <- ggplot() +
    geom_histogram( aes(x = coreDem$data[,x_name], y=..count../sum(..count..)),  alpha = 0.5, color='blue', fill='blue', bins=30 ) +
    coord_cartesian( xlim=c(xAxis.low,xAxis.high)) +
    scale_y_continuous(labels=function(x){ sprintf( paste("%.",yAxis.rouding,"f"),x)}) +
    theme(axis.title=element_blank(),
          axis.text.x=element_blank())
  
  g2 <- ggplot() +
    geom_histogram( aes(x = coreRep$data[,x_name], y=..count../sum(..count..)),  alpha = 0.5, color='red', fill='red' ) +
    coord_cartesian( xlim=c(xAxis.low,xAxis.high)) +
    scale_y_continuous(labels=function(x){ sprintf( paste("%.",yAxis.rouding,"f"),x)}) +
    theme(axis.title=element_blank())
  
  grid.arrange(g1,g2, nrow=2, left=yAxis.name)
}

for( pred in predictors)
{
  g <- ggplot() + geom_density( mapping = aes(x=repData[,pred] ) ) + xlab(pred)
  print(g)
}

colMeans(x)
