from setuptools import setup, find_packages
from os import path

current_dir = path.abspath(path.dirname(__file__))

long_description = ""
with open(path.join(current_dir, path.join(current_dir, 'README.md')), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='littlebrain',
  packages=find_packages(),
  package_data={'':['*.aiml']},
  include_package_data=True,
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='kathleen french',
  keywords=['chatbot', 'terminal', 'cli', 'aiml', 'assistant', 'python']
)