from setuptools import find_packages,setup
from typing import List
from pathlib import Path

HYPEN_E_DOT='-e .'
PROJECT_ROOT = Path(__file__).resolve().parent

def get_requirements(file_path:str)->List[str]:
    '''
        this function will return List of requirements
    ''' 
    requirements=[]
    with open(PROJECT_ROOT / file_path, "r") as file_obj:
        requirements = [
            req.strip()
            for req in file_obj.readlines()
            if req.strip() and not req.strip().startswith("#")
        ]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT) 
            
    return requirements
     
setup(
name='Machine Learning Project',
version='0.0.1',
author = 'Aman Pathak',
author_email='apmaths999@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)