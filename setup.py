from setuptools import setup, find_packages
import setuptools_scm

setup(
    name="souperscraper",
    use_scm_version=True,
    setup_requires=["setuptools_scm>=8"],
    description="A simple web scraper base combining Beautiful Soup and Selenium",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucas Faudman",
    author_email="lucasfaudman@gmail.com",
    url="https://github.com/LucasFaudman/souper-scraper.git",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "selenium",
        "beautifulsoup4",
        "requests",
    ],
    python_requires=">=3.8",
    license="LICENSE",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    keywords="web-scraping scraping easy beautifulsoup4 beautifulsoup bs4 selenium selenium-webdriver",
    project_urls={
        "Homepage": "https://github.com/LucasFaudman/souper-scraper.git",
        "Repository": "https://github.com/LucasFaudman/souper-scraper.git",
    },
    entry_points={
        "console_scripts": [
            "getchromedriver=souperscraper.getchromedriver:main",
        ],
    },
)
