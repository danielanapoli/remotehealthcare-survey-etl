class Scenario:
    def __init__(self, name, number):
        self.name = name
        self.number = number

Invalid_Scenario = Scenario("Invalid_Scenario", -1)
Chronic = Scenario("Chronic", 1)
Emergency = Scenario("Emergency", 2)
Rehab = Scenario("Rehab", 3)
Symptoms = Scenario("Symptoms", 4)