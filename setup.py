import os
import re
from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.realpath(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(HERE, 'bcx', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


def readme():
    with open(os.path.join(HERE, 'README.md')) as f:
        return f.read()


def extras_requires():
    extra_requirements = {
        'tests': [
            'pytest>=5.0.0',
            'pytest-cov>=2.7.1'
        ],
        'docs': [
            'sphinx>=2.1.2',
            'guzzle_sphinx_theme==0.7.11',
            'numpydoc==0.9.1',
            'sphinx-gallery==0.5.0',
        ]
    }

    dev_requires = []
    for section, required_packages in extra_requirements.items():
        if section in ['docs', 'tests']:
            dev_requires += required_packages

    all_requires = []
    for required_packages in extra_requirements.values():
        all_requires += required_packages

    extra_requirements['dev'] = dev_requires
    extra_requirements['all'] = all_requires

    return extra_requirements


def do_setup():
    config = dict(
        name='bcx',
        version=get_version(),
        packages=find_packages(exclude=['docs']),
        url='https://github.com/ilya-bc/blockchain-exchange-api',
        license='MIT',
        author='Blockchain.com',
        author_email='support@blockchain.zendesk.com',
        description='Blockchain.com Exchange API',
        long_description=readme(),
        long_description_content_type="text/markdown",
        classifiers=[
            'Development Status :: 3 - Alpha',
            "Intended Audience :: Developers",
            "Intended Audience :: Financial and Insurance Industry",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Office/Business :: Financial",
            "License :: OSI Approved :: MIT License",
        ],
        keywords=[
            'blockchain.info',
            'blockchain',
            'exchange',
            'trading',
            'market feed',
            'market data',
            'cryptocurrency',
            'bitcoin',
            'btc',
            'eth',
            'websocket',
            'api',
        ],
        python_requires='>=3.6',
        install_requires=[
            "websocket_client>=0.57.0",
        ],
        extras_require=extras_requires(),
    )

    setup(**config)


if __name__ == "__main__":
    do_setup()
