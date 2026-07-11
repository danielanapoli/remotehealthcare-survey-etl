library(readxl)
library(DescTools)
library(dplyr)

# Anchor paths to this script's location so the project runs regardless of
# where it's downloaded (requires running via RStudio's Source button)
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

datashare <- read_excel("../raw/datashare.xlsx")

Desc(Scenario ~ Total, datashare)
Desc(AgeBucket ~ Total, datashare)

#data subsets
#-- by experience
WithExpShare <- datashare %>% filter(ScenarioExp == TRUE)
WithoutExpShare <- datashare %>% filter(ScenarioExp == FALSE)
