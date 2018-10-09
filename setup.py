from setuptools import setup

setup(name='yape',
      description='Yet another pbuttons tool',
      url='https://github.com/murrayo/yape',
      author='Fabian',
      author_email='fab@intersystems.com',
      license='MIT',
      packages=['yape'],
      entry_points = {
        'console_scripts': ['yape=yape.command_line:main','yape-profile=yape.command_line:main_profile'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
      'pytz==2018.5',
      'matplotlib==2.2.3',
      'numpy==1.15.1',
      'pandas==0.23.4',
      'PyYAML==3.13',
      'setuptools_scm==3.1.0'],
      use_scm_version=True,
      version='',
      setup_requires=['setuptools_scm'],
      zip_safe=False)
