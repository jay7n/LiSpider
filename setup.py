from setuptools import setup

setup(
    name='lispider',
    version='0.1.dev0',
    url='https://github.com/jay7n/LiSpider',
    author=' Jayson Li',
    author_email='jay7n.li@outlook.com',
    license='MIT',
    py_modules=['lispider'],
    install_requires={
        'beautifulsoup4': ['beautifulsoup4'],
        'html5lib': ['html5lib']
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ]
)
