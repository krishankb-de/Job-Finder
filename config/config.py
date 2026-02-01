"""
Configuration file for Job Finder application
"""

import os
from datetime import datetime

# Job Keywords - Entry Level, Junior, and related positions
JOB_KEYWORDS = [
    "Junior AI Engineer",
    "AI Engineer Entry Level",
    "Data Scientist Junior",
    "Data Scientist Entry Level",
    "ML Engineer Junior",
    "ML Engineer Entry Level",
    "Software Developer Junior",
    "Software Developer Trainee",
    "SDE Junior",
    "Grad Software Engineer",
    "Graduate Trainee",
    "Starting Career",
    "Einstieg",
    "Anfänger",
    "Junior Developer",
    "Trainee Software",
    "Einstiegsposition",
]

# German Job Board URLs and search parameters
JOB_BOARDS = {
    "linkedin": {
        "base_url": "https://www.linkedin.com/jobs/search/",
        "country": "DE",
        "keywords": ["AI Engineer", "Data Scientist", "ML Engineer", "Software Developer"]
    },
    "stepstone": {
        "base_url": "https://www.stepstone.de/jobs/",
        "keywords": ["AI Engineer", "Data Scientist", "ML Engineer", "Softwareentwickler"]
    },
    "xing": {
        "base_url": "https://www.xing.com/jobs/",
        "keywords": ["AI Engineer", "Data Scientist", "ML Engineer", "Softwareentwickler"]
    },
    "indeed": {
        "base_url": "https://de.indeed.com/jobs",
        "keywords": ["AI Engineer", "Data Scientist", "ML Engineer", "Softwareentwickler"]
    },
    "google_jobs": {
        "base_url": "https://www.google.com/search",
        "keywords": ["jobs", "AI Engineer", "Data Scientist"]
    }
}

# German Companies - Add top German tech companies and startups
GERMAN_COMPANIES = {
    # Large Tech MNCs
    "SAP": {"url": "https://www.sap.com/careers", "careers_page": "https://careers.sap.com/"},
    "Siemens": {"url": "https://www.siemens.com/jobs", "careers_page": "https://jobs.siemens.com/"},
    "Deutsche Telekom": {"url": "https://www.telekom.com/en/career", "careers_page": "https://career.telekom.com/"},
    "BMW": {"url": "https://www.bmw-careeers.com", "careers_page": "https://www.bmw-group.com/en/careers.html"},
    "Daimler": {"url": "https://www.daimler.com/careers", "careers_page": "https://careers.daimler.com/"},
    "Volkswagen": {"url": "https://www.volkswagen-career.de", "careers_page": "https://www.volkswagen.com/careers"},
    "Deutsche Börse": {"url": "https://careers.deutsche-boerse.com", "careers_page": "https://careers.deutsche-boerse.com"},
    "Commerzbank": {"url": "https://www.commerzbank.com/careers", "careers_page": "https://careers.commerzbank.com"},
    "Allianz": {"url": "https://www.allianz.com/careers", "careers_page": "https://www.allianz.com/careers"},
    "Continental": {"url": "https://www.continental.com/careers", "careers_page": "https://jobs.continental.com"},
    "Bosch": {"url": "https://www.bosch.com/careers", "careers_page": "https://jobs.bosch.com"},
    "Bayer": {"url": "https://www.bayer.com/careers", "careers_page": "https://careers.bayer.com"},
    
    # Software/IT Companies
    "SoundCloud": {"url": "https://soundcloud.com/careers", "careers_page": "https://soundcloud.com/careers"},
    "Zalando": {"url": "https://careers.zalando.com", "careers_page": "https://careers.zalando.com"},
    "Delivery Hero": {"url": "https://www.deliveryhero.com/careers", "careers_page": "https://careers.deliveryhero.com"},
    "Rocket Internet": {"url": "https://www.rocket-internet.com/careers", "careers_page": "https://careers.rocket-internet.com"},
    "Scribd": {"url": "https://www.scribd.com/about/careers", "careers_page": "https://scribd.com/careers"},
    "SoundCloud": {"url": "https://soundcloud.com/careers", "careers_page": "https://soundcloud.com/careers"},
    "N26": {"url": "https://n26.com/careers", "careers_page": "https://careers.n26.com"},
    "Klarna": {"url": "https://www.klarna.com/careers", "careers_page": "https://jobs.klarna.com"},
    
    # AI/ML Startups and Companies
    "Celonis": {"url": "https://www.celonis.com/careers", "careers_page": "https://careers.celonis.com"},
    "Rasa": {"url": "https://rasa.com/careers", "careers_page": "https://rasa.com/careers"},
    "Fraugster": {"url": "https://fraugster.com/careers", "careers_page": "https://fraugster.com/careers"},
    "Flixbus": {"url": "https://flixbus.com/careers", "careers_page": "https://careers.flixbus.com"},
    "Eight Sleep": {"url": "https://www.eightsleep.com/careers", "careers_page": "https://www.eightsleep.com/careers"},
    "Wolt": {"url": "https://careers.wolt.com/", "careers_page": "https://careers.wolt.com/"},
    
    # Tech Consulting & Services
    "McKinsey": {"url": "https://www.mckinsey.com/careers", "careers_page": "https://www.mckinsey.com/careers"},
    "Deloitte": {"url": "https://www2.deloitte.com/de/de/careers.html", "careers_page": "https://careers.deloitte.com/"},
    "EY": {"url": "https://www.eycareersfirst.com", "careers_page": "https://careers.ey.com/"},
    "Accenture": {"url": "https://www.accenture.com/de-de/careers", "careers_page": "https://careers.accenture.com/"},
    "Capgemini": {"url": "https://www.capgemini.com/de-de/careers", "careers_page": "https://www.capgemini.com/careers/"},
    "IBM": {"url": "https://www.ibm.com/careers", "careers_page": "https://careers.ibm.com/"},
    "Microsoft": {"url": "https://careers.microsoft.com/", "careers_page": "https://careers.microsoft.com/"},
    "Google": {"url": "https://careers.google.com/", "careers_page": "https://careers.google.com/"},
    "Amazon": {"url": "https://www.amazon.jobs/", "careers_page": "https://www.amazon.jobs/"},
}

# Job Level Keywords (for filtering)
JOB_LEVEL_KEYWORDS = [
    "junior",
    "entry level",
    "entry-level",
    "graduate",
    "trainee",
    "einstieg",
    "anfänger",
    "abschluss",
    "berufseinsteiger",
    "einstiegsposition",
    "starter",
    "career starter",
    "fresh",
    "recent graduate",
    "no experience",
    "erfahrung nicht erforderlich",
]

# Technical Keywords (for job field matching)
TECHNICAL_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "data science",
    "data scientist",
    "python",
    "software development",
    "software engineer",
    "sde",
    "backend",
    "frontend",
    "fullstack",
    "web development",
    "neural network",
    "deep learning",
    "nlp",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "data analysis",
    "analytics",
]

# Configuration parameters
CONFIG = {
    "max_results_per_board": 100,
    "hours_back": 24,  # Search for jobs posted in last 24 hours
    "timeout": 30,  # Request timeout in seconds
    "retry_attempts": 3,
    "retry_delay": 5,  # seconds
    "headless_browser": True,  # Use headless browser for Selenium
    "output_dir": "output",
    "log_file": "job_finder.log",
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}

# Date/Time utilities
def get_24h_ago():
    """Get datetime from 24 hours ago"""
    from datetime import datetime, timedelta
    return datetime.now() - timedelta(hours=24)

def get_current_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Export configurations
EXPORT_CONFIG = {
    "columns": [
        "Company Name",
        "Job Title",
        "Job URL",
        "Posted Date",
        "Job Board",
        "Location",
        "Job Level",
        "Keywords Match",
    ],
    "excel_filename": f"job_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    "sheet_name": "German Job Postings",
}
