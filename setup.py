from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vehicle-market-x23311428',
    version='1.0.0',
    author='Dhruv Jani',
    author_email='dhruvjanicloud07@gmail.com',
    description='Motor marketplace utilities library for automotive applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://pypi.org/project/vehicle-marketplace-utils-x23311428/',
    py_modules=['vehicle_utils'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    keywords='vehicle, automotive, marketplace, price-estimation, validation, car, bike'
)