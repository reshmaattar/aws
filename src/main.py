from src.classes import utility
from src.classes.build_template import EnvironmentTemplate

""" The purpose of this to take input of environment from config.ini file and create cloud formation template .
    Finally it compares with the template defined in template file."""
Env = [{"Env": "Development", "Template": "template_development"},
       {"Env": "Experimental", "Template": "template_experimental"},
       {"Env": "Production", "Template": "template_production"}]
for e in Env:
    template = EnvironmentTemplate(Env=e['Env'])
    template.create_vpc()
    template.create_gateway()
    template.create_network()
    template.write_to_file("output/%s.json" % e['Env'])
    t = utility.CompareFile("template/%s.json" % e['Template'], "output/%s.json" % e['Env'])
    t.difference()
