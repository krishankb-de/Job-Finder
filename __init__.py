"""
__init__.py - Package initialization for Job Finder
"""

__version__ = "1.0.0"
__author__ = "Job Finder Team"
__description__ = "A comprehensive job finder for German companies"

from config import (
    JOB_KEYWORDS,
    JOB_LEVEL_KEYWORDS,
    TECHNICAL_KEYWORDS,
    GERMAN_COMPANIES,
    CONFIG
)

from scrapers import (
    LinkedInScraper,
    StepstoneScraper,
    XingScraper,
    IndeedScraper,
    CompanyWebsiteScraper,
    GoogleJobsScraper
)

from utils import (
    JobFilter,
    DataProcessor,
    ExcelExporter,
    CSVExporter
)

__all__ = [
    'JOB_KEYWORDS',
    'JOB_LEVEL_KEYWORDS',
    'TECHNICAL_KEYWORDS',
    'GERMAN_COMPANIES',
    'CONFIG',
    'LinkedInScraper',
    'StepstoneScraper',
    'XingScraper',
    'IndeedScraper',
    'CompanyWebsiteScraper',
    'GoogleJobsScraper',
    'JobFilter',
    'DataProcessor',
    'ExcelExporter',
    'CSVExporter',
]
