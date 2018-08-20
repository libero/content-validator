from setuptools import setup, find_packages
import validator


setup(
    name='content-validator',
    version=validator.__version__,
    description='Validate XML against the Libero content model',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['lxml'],
    license='MIT',
    url='https://github.com/libero/content-validator.git',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='tech-team@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
