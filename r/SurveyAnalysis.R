#########################################################################
# All statistical tests return non-significant differences              #
# unless p-value is stated.                                             #
#                                                                       #
# Data set last updated:  March 3, 2023                                 #
#########################################################################

library(readxl)
library(DescTools)
library(tidyverse)
library(fifer)

# Anchor paths to this script's location so the project runs regardless of
# where it's downloaded (requires running via RStudio's Source button)
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

df <- read_excel("../python/data_cleaned_raw.xlsx")

#------Data subsets------#
#subsets dedicated to ageBucket
Ages18to34 <- df %>% filter(AgeBucket == "18-34")
Ages35to49 <- df %>% filter(AgeBucket == "35-49")
Ages50to64 <- df %>% filter(AgeBucket == "50-64")
Ages65plus <- df %>% filter(AgeBucket == "65+") 

#subsets dedicated to scenarios
Chronic <- df %>% filter(Scenario == "Chronic")
Emergency <- df %>% filter(Scenario == "Emergency")
Rehab <- df %>% filter(Scenario == "Rehab")
Symptoms <- df %>% filter(Scenario == "Symptoms")

#------Participant summary------# 
Desc(AgeBucket ~ Gender, df)
Desc(AdultBucket  ~ Gender, df)
Desc(df$RaceEthn)
Desc(df$Province)
Desc(df$Education)
Desc(df$Language)
Desc(df$TechUse)
Desc(df$LiveWhere)
Desc(df$LiveWith)
Desc(df$CareTake)
Desc(AgeBucket ~ HealthcareImpact, df)

#------SA-6 + Privacy------#
Desc(AgeBucket ~ SA61, df) 
Desc(AgeBucket ~ SA62, df) #p-value = 0.02
Desc(AgeBucket ~ SA63, df) #p-value = 0.01
Desc(AgeBucket ~ SA64, df)
Desc(AgeBucket ~ SA65, df) 
Desc(AgeBucket ~ SA66, df)
Desc(AgeBucket ~ Priv1, df)
Desc(AgeBucket ~ Priv2, df)

Desc(AdultBucket ~ SA61, df) 
Desc(AdultBucket ~ SA62, df) 
Desc(AdultBucket ~ SA63, df) #p-value = 0.009 
Desc(AdultBucket ~ SA64, df)
Desc(AdultBucket ~ SA65, df)
Desc(AdultBucket ~ SA66, df)
Desc(AdultBucket ~ Priv1, df)
Desc(AdultBucket ~ Priv2, df)

Desc(Scenario ~ SA61, df) 
Desc(Scenario ~ SA62, df) 
Desc(Scenario ~ SA63, df)  
Desc(Scenario ~ SA64, df)
Desc(Scenario ~ SA65, df) 
Desc(Scenario ~ SA66, df)
Desc(Scenario ~ Priv1, df)
Desc(Scenario ~ Priv2, df)

#------Healthcare Experiences------#
Desc(AgeBucket ~ ExpChangeSinceCovid, df)
Desc(AgeBucket ~ BeforeCov_Telephone, df)
Desc(AgeBucket ~ BeforeCov_Video, df)
Desc(AgeBucket ~ BeforeCov_Email, df)
Desc(AgeBucket ~ BeforeCov_InstantMsg, df)
Desc(AgeBucket ~ BeforeCov_SMS, df)

Desc(AdultBucket ~ BeforeCov_Inperson, df) 
Desc(AdultBucket ~ BeforeCov_Telephone, df) 
Desc(AdultBucket ~ BeforeCov_Video, df) 
Desc(AdultBucket ~ BeforeCov_Email, df) 
Desc(AdultBucket ~ BeforeCov_InstantMsg, df) 
Desc(AdultBucket ~ BeforeCov_SMS, df) 
# For all options, there are significant differences between 
# how olderAdults and youngerAdults accessed healthcare before COVID.
# However, due no differences in the median score, this difference
# is not practical for our analysis purposes.

Desc(AgeBucket ~ AfterCov_Inperson, df)
Desc(AgeBucket ~ AfterCov_Telephone, df)
Desc(AgeBucket ~ AfterCov_Video, df)
Desc(AgeBucket ~ AfterCov_Email, df)
Desc(AgeBucket ~ AfterCov_InstantMsg, df)
Desc(AgeBucket ~ AfterCov_SMS, df)

Desc(AdultBucket ~ AfterCov_Inperson, df) 
Desc(AdultBucket ~ AfterCov_Telephone, df)
Desc(AdultBucket ~ AfterCov_Video, df)
Desc(AdultBucket ~ AfterCov_Email, df)
Desc(AdultBucket ~ AfterCov_InstantMsg, df) #p-value: 0.00...
Desc(AdultBucket ~ AfterCov_SMS, df) #p-value: 0.04
# Significant differences are not practical (i.e., median rank
# response are not different)

#------Scenario------#
Desc(AgeBucket ~ Scenario, df)

Desc(AgeBucket ~ TechUseLikelihood, df) #p-value = 0.04
Desc(AdultBucket ~ TechUseLikelihood, df)

Desc(Scenario ~ TechUseLikelihood, df)

Desc(Scenario ~ VideoIDComfort, df)
Desc(Scenario ~ VideoANONComfort, df)
Desc(Scenario ~ AudioComfort, df) #p-value = 0.002
  pairwise.t.test(Chronic$AudioComfort, Emergency$AudioComfort, p.adj = 'bonferroni')
Desc(Scenario ~ WellnessComfort, df)
Desc(Scenario ~ VitalsComfort, df)

Desc(AgeBucket ~ VideoIDComfort, df)
Desc(AgeBucket ~ VideoANONComfort, df)
Desc(AgeBucket ~ AudioComfort, df)
Desc(AgeBucket ~ WellnessComfort, df)
Desc(AgeBucket ~ VitalsComfort, df)

Desc(AdultBucket ~ VideoIDComfort, df)
Desc(AdultBucket ~ VideoANONComfort, df)
Desc(AdultBucket ~ AudioComfort, df)
Desc(AdultBucket ~ WellnessComfort, df)
Desc(AdultBucket ~ VitalsComfort, df)

# ConcernsList
#'I do not know why this information would need to be collected for this scenario'
#'I do not want people to know this information'
#'I worry this information may be misused'
#'I worry this information may not be sufficiently protected when stored'

#Reference: https://evoldyn.gitlab.io/evomics-2018/ref-sheets/R_strings.pdf
str_count(df$VideoIDConcerns, 'I do not know why this information would need to be collected for this scenario')
str_count(df$VideoIDConcerns, 'I do not want people to know this information')


