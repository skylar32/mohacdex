import setuptools

requires = [
    'SQLAlchemy==1.3.20'
]

entry_points = {
    'console_scripts': "mohacdex = mohacdex.db.main:main"
}

setuptools.setup(
    name='mohacdex',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points = entry_points
)
