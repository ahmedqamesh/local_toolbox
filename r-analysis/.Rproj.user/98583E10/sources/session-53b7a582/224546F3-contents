library(tidyverse)
library(skimr)
library(janitor)
library(ggplot2)
bookings_df <- read_csv("data/hotel_bookings.csv")
View(bookings_df)
#summarize or preview your data
head(bookings_df)
#str(bookings_df)
#glimpse(bookings_df)
# provides a detailed summary of the data
skim_without_charts(bookings_df)

# what columns you have in your data frame
colnames(bookings_df)


## Plot the data as scatterplot
ggplot(data = bookings_df) +
  geom_point(mapping = aes(x = lead_time, y = children, color=arrival_date_year))

# plot the relationship as smooth
ggplot(data = bookings_df) +
  geom_smooth(mapping = aes(x = stays_in_weekend_nights, y = children))
  ggsave("output/bookings_df.png")
# Plot bars


# create new data frame  that focuses on the average daily rate, 
#which is referred to as `adr` in the data frame, and  `adults` 
new_df <- select(bookings_df, `adr`, adults)

# create new variables in your data frame
mutate(new_df, total = `adr` / adults)

#-----------------------------------------------------------------------
#Create a new data frame with just those columns
trimmed_df <- bookings_df %>% 
  select(hotel, is_canceled, lead_time)




# Rename the variable 'hotel' to be named 'hotel_type'
trimmed_df %>% 
  select(hotel, is_canceled, lead_time) %>% 
  rename(hotel_type = hotel)


#combine the arrival month and year into one column using the unite() 

example_df <- bookings_df %>%
  select(arrival_date_year, arrival_date_month) %>% 
  unite(arrival_month_year, c("arrival_date_month", "arrival_date_year"), sep = " ")

# To see the total number of canceled bookings
sum(trimmed_df$is_canceled)


# `arrange()`  automatically orders by ascending order
hotel_bookings_v2 <- arrange(bookings_df, desc(lead_time))

max(bookings_df$lead_time)
mean(bookings_df$lead_time)
