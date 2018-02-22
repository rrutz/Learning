#kernal examples

nearestNeighbourKernal <- function( k, x_point, x, y )
{
  l = length(x)
  index <- which.min( abs(x - x_point ))
  
  if( index < k/2 )
  {
    return( mean(y[0:k]) )
  }
  else if( (l-index) < k/2  )
  {
    return( mean(y[(l-k):l]) )
  }
  else
  {
    return( mean( y[ (index - k/2):(index + k/2)] ))
  }
}

normalKernal <- function( x_i, x, y)
{
  weights <- dnorm( x, mean = x_i, sd = var(x)^.5 / 3  )
  weights <- weights / sum(weights)
  return( sum( weights * y) )
}


x <- sort( runif(100) )
y <- sin(4*x) + rnorm(100 ,0, 1/3) 
x_spaced <- c(0:100)/100

nearestNeighbourKernal(k=6, x_point= x_spaced[101]  , x=x, y=y)

ggplot() + geom_point(  mapping = aes(x =x, y=y)) +
   geom_line( mapping = aes( x=x_spaced, y = sin(4*x_spaced), color = "true"), size = 1) + 
  
  geom_line( mapping = aes( x=x_spaced,   
            y = sapply( x_spaced, FUN = function(x_in) nearestNeighbourKernal(k=30,x_point= x_in, x=x, y=y)),
            color = "k-means"), size = 1) +
  
  geom_line( mapping = aes( x=x_spaced, y = sapply(x_spaced, FUN = function(x_i) normalKernal(x_i = x_i, x=x, y=y)  ),
            color = "normal kernal"), size = 1) +
  scale_color_manual(labels = c( "k-means", "normal kernal", "true"),
                     values = c("true"= "black", "k-means"= "blue", "normal kernal" = "green"))

  
