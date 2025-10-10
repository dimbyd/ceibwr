from setuptools import setup

setup(
    name='ceibwr',
    version='0.1',
    description='Meddalwedd Gynganeddol',
    url='http://github.com/dimbyd/ceibwr',
    author='dimbyd',
    author_email='evansd8@cf.ac.uk',
    license='GNU',
    packages=['ceibwr'],
    install_requires=['lxml', 'pyaml', 'tabulate', 'python-slugify',],
    entry_points={
        'console_scripts': ['ceibwr=ceibwr:main'],
    },
    include_package_data=True,
    zip_safe=False,
)
