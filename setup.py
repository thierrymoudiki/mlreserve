# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages
from os import listdir

with open('requirements.txt', 'r') as f:
    dependencies = f.read().splitlines()

descr = "mlreserve Package - Claims Reserving package "
name = 'mlreserve'
url = 'https://github.com/thierrymoudiki/mlreserve'
version='0.1.0' # Put this in __init__.py

data_path = ''
setup(
    name=name,
    version=version,
    maintainer='T. Moudiki',
    maintainer_email='thierry.moudiki@gmail.com',
    packages=find_packages(include=["mlreserve", "mlreserve.*"]),
    scripts=[],
    url=url,
    download_url='{}/archive/v{}.tar.gz'.format(url, version),
    license='MPL-2.0',
    include_package_data=True,
    package_data={
        'data': [data_path + item
                 for item in listdir('mlreserve{}'.format(data_path))]},
    description=descr,
    long_description="Machine Learning Reserving",
    install_requires=dependencies,
)
