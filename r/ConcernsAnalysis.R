library(readxl)
library(DescTools)
library(coin)
library(dplyr)

# Anchor paths to this script's location so the project runs regardless of
# where it's downloaded (requires running via RStudio's Source button)
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

concerns <- read_excel("../raw/concerns.xlsx")

#data subsets
#-- by experience
WithExp <- concerns %>% filter(ScenarioExp == TRUE)
WithoutExp <- concerns %>% filter(ScenarioExp == FALSE)

#---by age
concerns18to34 <- concerns %>% filter(AgeBucket == "18-34")
concerns35to49 <- concerns %>% filter(AgeBucket == "35-49")
concerns50to64 <- concerns %>% filter(AgeBucket == "50-64")
concerns65plus <- concerns %>% filter(AgeBucket == "65+") 

#Kruskal-Wallis to checks if there are differences
Desc(AgeBucket ~ VideoIDConcernsCount, concerns) #p-value = 0.03
Desc(AgeBucket ~ VideoANONConcernsCount, concerns)
Desc(AgeBucket ~ AudioConcernsCount, concerns)
Desc(AgeBucket ~ WellnessConcernsCount, concerns) #p-value = 0.01
Desc(AgeBucket ~ VitalsConcernsCount, concerns) 

#TODO:
#Post-hoc pairwise tests to see where the differences are between groups