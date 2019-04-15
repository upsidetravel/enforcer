"""
Tell Python how to install and manage this library. Used implicitly by `pip`,
so don't remove!
"""
try:
    from setuptools import setup, PEP420PackageFinder  # or find_packages
except ImportError:
    raise AssertionError('Cannot build library without setuptools!')
# Support custom commands, like writing out our requirements into
# a form that Snyk knows how to parse.
# TODO: if we adopt Pipenv, replace this with a line of bash:
# `pipenv lock -r > requirements.txt`
import shutil
from distutils.cmd import Command


class SnykSync(Command):
    description = "Sync setup.py to requirements.txt to enable Snyk to run."
    user_options = [
        ('output', 'o', 'Output file name (default: requirements.txt)'),
        ('backup', 'b', 'Backup file name (default: requirements_orig.txt)'),
    ]

    def initialize_options(self):
        self.output = 'requirements.txt'
        self.backup = 'requirements_orig.txt'

    def finalize_options(self):
        pass

    def run(self):
        shutil.copyfile(self.output, self.backup)
        with open(self.output, 'w', encoding='utf8') as reqs:
            reqs.write('\n'.join(INSTALL_REQUIRES))


INSTALL_REQUIRES = [
    'python-dotenv~=0.7.1',
    'boto3==1.9.66',
    'pyperclip==1.7.0',
    'click==7.0',
    'colorama==0.4.1',
]

TEST_REQUIRES = [
    'flake8~=3.5.0',
    'mock~=2.0.0',
    'moto==1.3.1',
    'pytest~=3.4.0',
    'pytest-cov~=2.5.1',
    'tox~=2.9.1',
    'yapf~=0.21.0',
    'bandit==1.5.1',
]

try:
    import pypandoc

    DESCRIPTION = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    DESCRIPTION = "AWS SSM Parameter Store Management CLI"

DEPENDENCY_LINKS = []

setup(
    name='enforcer',
    version="1.0.1",
    url='https://github.com/PotomacInnovation/enforcer',
    license='Upside',
    author="@PotomacInnovation/owners-sre",
    description='AWS SSM Parameter Store Management CLI',
    long_description=DESCRIPTION,
    packages=PEP420PackageFinder.find(),  # or find_packages()
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    test_requires=TEST_REQUIRES,
    extras_require={'dev': TEST_REQUIRES},
    dependency_links=DEPENDENCY_LINKS,
    classifiers=[],
    scripts=['bin/enforcer'],
    cmdclass={'snyksync': SnykSync})
