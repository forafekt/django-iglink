"""""
setup module
"""""
from pathlib import Path  # noqa

import setuptools
import os

app = Path(__file__).resolve(strict=True).parent.parent
here = Path(__file__).resolve(strict=True).parent

__all__ = ["__version__"]

with open(os.path.join(here, 'VERSION')) as f:
    __version__ = f.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(here, 'MANIFEST.in')) as f:
    MANIFEST = f.read().strip()

extra_files = [
    os.path.join(here, 'VERSION'),
    os.path.join(here, 'README.md'),
    os.path.join(here, 'MANIFEST.in')
]

setuptools.setup(
    name="django-iglink",
    version=__version__,

    include_package_data=True,
    package_data={"": extra_files},
    project_urls={
        "Bug Tracker": "https://github.com/forafekt/django-iglink/issues",
        "Documentation": "https://github.com/forafekt/django-iglink/tree/master/djangular_serve/docs",
        "Source Code": "https://github.com/forafekt/django-iglink",
    },

    packages=setuptools.find_packages(),

    author="Jonny Doyle",
    author_email="jonathan.d@programmer.net",
    license="MIT",
    description="Django Instagram API. Use your Instagram data anywhere.  "
                "Includes cache feature in the case of Exceptions.",
    keywords="django angular ig instagram http api rest django-rest-framework json cache",
    platform="Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forafekt/django-iglink",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.6',
)
