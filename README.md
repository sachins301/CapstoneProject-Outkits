# CapstoneProject-Outkits
This repo holds the code to generate the executable for outkits project.

## Auto-py-to-exe Configurations
![image](https://github.com/user-attachments/assets/8dcfcae1-5038-4484-be11-0b282585ac5a)
![image](https://github.com/user-attachments/assets/6c7d1893-265d-4685-81bc-4f064c60e025)


## Point of failures
xlsxwriter module not found error in executable - Install xlsxwriter on the python environment that pyinstaller is using and add xlsxwriter to the hidden-import flag in the pyinstaller (or auto-py-to-exe)
