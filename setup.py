from setuptools import setup, find_packages

setup(name='babybrowser',
      version='0.1',
      description='A small browser implementation in Python',
      url='https://github.com/lauryndbrown/BabyBrowser',
      author='Lauryn Brown',
      author_email='lauryndbrown@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'PyQt5',
        'requests'
      ],
      entry_points={
        'console_scripts':[
            'babybrowser = baby_browser.baby_browser:start'
        ]
      }, 
      zip_safe=False)
