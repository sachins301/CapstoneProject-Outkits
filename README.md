# CapstoneProject-Outkits
This repo holds the code to generate the executable for outkits project.

## Point of failures
xlsxwriter module not found error in executable - Install xlsxwriter on the python environment that pyinstaller is using and add xlsxwriter to the hidden-import flag in the pyinstaller (or auto-py-to-exe)
