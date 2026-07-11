library(readxl)
library(DescTools)
library(ggplot2)
library(ggthemes)
library(reshape)

# Anchor paths to this script's location so the project runs regardless of
# where it's downloaded (requires running via RStudio's Source button)
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

df <- read_excel("../python/qualtrics_cleaned_raw.xlsx")
viz <- df["Scenario"]

#stacked bar chart
#SOURCE: https://kleiber.me/blog/2018/04/21/R-stacked-horizontal-barcharts-likert-type-scale/

StronglyAgree <- numeric()
sa = 0

viz <- data.frame(StronglyAgree)

for(row in df$TechUseLikelihood){
  ifelse (df$TechUseLikelihood == "5", (sa = sa+1), (sa=sa))
}
StronglyAgree <- c(sa)

viz["StronglyAgree"] <- viz["StronglyAgree"] / viz["Scenario"] * 100

df_m <- melt(df[1:5], id.vars = "Scenario")

print(
  ggplot(df_m, aes(x = paste(substr(Question, 1, 50), '...') , y = value, fill = variable)) + 
  geom_bar(stat = 'identity') + 
  ggtitle('Title') + 
#  xlab('Statement') + 
#  ylab('Participants') + 
  coord_flip() + 
  theme_minimal()
)
