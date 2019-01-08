"""Set up find_a_doggo as a package."""


from setuptools import setup

setup(
    name='find_a_doggo',
    packages=['find_a_doggo'],
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
