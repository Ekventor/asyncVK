from setuptools import setup, find_packages


requirements = ["asyncio>=3", "aiohttp>=3"]


setup(
    name="async_VKsher",
    version="1.1.1",
    author="Kulenov Islam",
    author_email="kit.werr34@gmail.com",
    description="asyncVK is asynchronous library for creating a bot in VK",
    url="https://github.com/Ekventor/asyncVK",
    packages=find_packages(),
    install_requirement=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
