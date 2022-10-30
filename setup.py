from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='neozot',
    version='0.0.5',
    author='Vishnu Raj',
    author_email='rajvishnu@duck.com',
    url='https://github.com/v-i-s-h/neozot-py/',
    packages=['neozot'],
    package_data={
        'neozot': [
            'ui/index.html', 
            'ui/style.css'
        ]
    },
    install_requires=['appdirs', 'eel', 'numpy', 'requests', 'scikit_learn'],
    python_requires='>=3.7',
    description='neozot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['zotero', 'arxiv', 'research'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
)
