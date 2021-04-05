import io
from os import name

from setuptools import find_packages
from setuptools import setup

pkg_name = 'jokes'


setup(
    name=pkg_name,
    package_dir={"": "src"},
    packages=find_packages("src"),
    version="0.0.1",
    author='Ksenia Kargina',
    author_email='kargina.ks@gmail.com',
    install_requires=[
        "pytest~=6.2.3",
        "PyJWT~=2.0.1",
        "Flask~=1.1.2",
        "Werkzeug~=0.16.1",
        "requests~=2.25.1",
        "setuptools~=54.2.0",
        "Flask-JWT-Extended==4.1.0",
        "Flask-SQLAlchemy==2.5.1",
        "flask-restx==0.3.0",
        "PyMySQL==1.0.2"
    ],
    entry_points={
        'console_scripts':
            ['joke-api = jokes.main:run']
    },
)
