import setuptools

setuptools.setup(
    name='jbotokenizer',
    version='1.0.0',
    license='MIT',
    author='Oleg Parashchenko',
    author_email='olpa@uucode.com',
    description='Lojban tokenizer for machine learning tasks',
    url='https://github.com/olpa/lojban-mt/tree/master/tokenizer/',
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords=['lojban'],
    package_dir={'jbotokenizer': './jbotokenizer'},
    packages=['jbotokenizer'],
    scripts=['./scripts/jboparse.py'],
    python_requires='>=3.6',
)
