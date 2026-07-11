library(readxl)
library(DescTools)
library(coin)

# Anchor paths to this script's location so the project runs regardless of
# where it's downloaded (requires running via RStudio's Source button)
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

sapriv <- read_excel("../raw/sapriv.xlsx")

#data subsets
#-- by experience
WithExpSP <- sapriv %>% filter(ScenarioExp == TRUE)
WithoutExpSP <- sapriv %>% filter(ScenarioExp == FALSE)