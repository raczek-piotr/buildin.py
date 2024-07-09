from setuptools import setup
import re, os

#on_rtd = os.getenv('READTHEDOCS') == 'True'

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

#if on_rtd:
#  requirements.append('')

version = ''
with open('buildin/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

with open('ECVI/__init__.py') as f:
    version += "+ECVI-" + re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = {}

setup(name='buildin.py',
      author='PR',
      url='https://github.com/raczek-piotr/buildin.py/',
      version=version,
      packages=['buildin', 'ECVI'],
      license='none',
      description="For automaticaly update my rpi's softwere (not for comercial use)",
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      extras_require=extras_require,
      classifiers=[
        'Development Status :: 0',
        'Natural Language :: Polish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.12',
      ]
)
