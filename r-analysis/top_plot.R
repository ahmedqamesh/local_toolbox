library(ggplot2)
library(palmerpenguins)

data(penguins)
View(penguins)

flipper_length_mm <- penguins$flipper_len
body_mass_g <- penguins$body_mass
## create the plot.
### geom_ function is to display the data
ggplot(data = penguins) + geom_point(mapping = aes(x = flipper_length_mm, y = body_mass_g))

