from src.classes import utility
from src.classes.build_template import EnvironmentTemplate

Env = [{"Env": "Development", "Template": "template_development"},
       {"Env": "Experimental", "Template": "template_experimental"},
       {"Env": "Production", "Template": "template_production"}]
for e in Env:
    a = EnvironmentTemplate(Env=e['Env'])
    a.create_vpc()
    a.create_gateway()
    a.create_network()
    a.write_to_file("output/%s.json" % e['Env'])
    t = utility.CompareFile("template/%s.json" % e['Template'], "output/%s.json" % e['Env'])
    t.difference()
