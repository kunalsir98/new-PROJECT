from setuptools import find_packages,setup
from typing import List 

'''
this function will help to return the requirements of all the necessary library  
which are present in requirements.txt

'''
HYPEN_E_DOT='-e .'

def get_requirements(file_path)->List[str]:
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('/n','')for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name='housing',
    version='0.0.1',
    author='kunal',
    author_email='kunalchopde98@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()

)

