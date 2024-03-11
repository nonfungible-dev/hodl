from setuptools import setup, find_packages

setup(
    name='hodl',
    version='0.1.0',
    author='NFP',
    author_email='nfp@pesky-penguins.com',
    description='A CLI for DCAing into and out of crypto via the Coinbase Advanced API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important for rendering markdown READMEs
    url='http://github.com/nonfungible_dev/hodl',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'click',
        'coinbase-advanced-py',
    ],
    entry_points='''
        [console_scripts]
        hodl=hodl:main
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Cryptocurrency :: DCA Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

