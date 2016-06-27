from distutils.core import setup

setup(
    name='chimera_commandersk',
    version='0.0.1',
    packages=['chimera_commandersk', 'chimera_commandersk.instruments', 'chimera_commandersk.instruments.skdrv'],
    install_requires='pymodbus',
    scripts=[],
    url='http://github.com/astroufsc/chimera-commandersk',
    license='GPL v2',
    author='Salvador Agati',
    author_email='wschoenell@gmail.com',
    description='Emerson Control Techniques COMMANDER SK driver for the chimera observatory control system.'
)
