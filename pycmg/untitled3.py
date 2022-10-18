# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 07:10:49 2022

@author: ga67hah
"""

from generate_mesostructure import Mesostructure
from configuration import Configuration
from visualization import export_data, visualize_sections

my_configuration = Configuration(vf_max_assembly=0.3)
my_configuration.load_inclusions(conf_csv='../examples/AB8_CMG.csv')

my_mesostructure = Mesostructure(mesostructure_size=[200, 200, 200])
my_mesostructure.add_configuration(my_configuration)

# #GENERATE
# my_synthetic_microstructure =my_mesostructure.assemble_sra()
# # VISUALIZE
# visualize_sections(my_synthetic_microstructure, 2)
# #EXPORT
# #export_data(my_synthetic_microstructure, 'vtk', 'mesostructure.vti')