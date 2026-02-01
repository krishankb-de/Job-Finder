"""
Web scraper for job postings from various sources
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import logging
from typing import List, Dict
from urllib.parse import urljoin, quote
import json

logger = logging.getLogger(__name__)


class JobScraper:
    """Base class for job scraping"""
    
    def __init__(self, timeout=30, retry_attempts=3, retry_delay=5):
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.jobs = []
    
    def fetch_page(self, url, params=None):
        """Fetch a webpage with retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to fetch {url} after {self.retry_attempts} attempts")
                    return None
    
    def parse_date(self, date_string):
        """Parse various date formats"""
        date_string = str(date_string).lower().strip()
        
        try:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]:
                try:
                    return datetime.strptime(date_string[:10], fmt)
                except ValueError:
                    continue
            
            # Handle relative dates
            if "today" in date_string or "heute" in date_string:
                return datetime.now()
            elif "yesterday" in date_string or "gestern" in date_string:
                return datetime.now() - timedelta(days=1)
            elif "hour" in date_string or "stunde" in date_string:
                hours = int(''.join(filter(str.isdigit, date_string[:2]))) if date_string[0].isdigit() else 1
                return datetime.now() - timedelta(hours=hours)
            elif "day" in date_string or "tag" in date_string:
                days = int(''.join(filter(str.isdigit, date_string[:2]))) if date_string[0].isdigit() else 1
                return datetime.now() - timedelta(days=days)
            else:
                return None
        except Exception as e:
            logger.warning(f"Could not parse date: {date_string}. Error: {str(e)}")
            return None
    
    def is_recent(self, posted_date, hours=24):
        """Check if job was posted within specified hours"""
        if posted_date is None:
            return False
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return posted_date >= cutoff_time
        except Exception as e:
            logger.warning(f"Error checking if date is recent: {str(e)}")
            return False


class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn job postings"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.linkedin.com/jobs/search/"
    
    def search(self, keywords: List[str], location="Germany"):
        """Search LinkedIn for jobs"""
        logger.info(f"Searching LinkedIn for jobs: {', '.join(keywords)}")
        jobs = []
        
        for keyword in keywords:
            try:
                params = {
                    "keywords": keyword,
                    "location": location,
                    "sort": "date",
                    "datePosted": "past24h"
                }
                
                response = self.fetch_page(self.base_url, params=params)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # LinkedIn job listings
                job_listings = soup.find_all('div', {'class': 'base-card'})
                
                for job in job_listings[:self.timeout]:  # Limit results
                    try:
                        title_elem = job.find('h3', {'class': 'base-search-card__title'})
                        company_elem = job.find('h4', {'class': 'base-search-card__subtitle'})
                        link_elem = job.find('a', {'class': 'base-card__full-link'})
                        date_elem = job.find('time')
                        
                        if title_elem and company_elem and link_elem:
                            job_data = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'url': link_elem.get('href', ''),
                                'posted_date': date_elem.get('datetime') if date_elem else None,
                                'board': 'LinkedIn',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing LinkedIn job: {str(e)}")
                        continue
                
                time.sleep(2)  # Be respectful with requests
            
            except Exception as e:
                logger.error(f"Error searching LinkedIn for '{keyword}': {str(e)}")
                continue
        
        self.jobs.extend(jobs)
        logger.info(f"Found {len(jobs)} jobs on LinkedIn")
        return jobs


class StepstoneScraper(JobScraper):
    """Scraper for Stepstone job postings"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.stepstone.de/jobs"
    
    def search(self, keywords: List[str]):
        """Search Stepstone for jobs"""
        logger.info(f"Searching Stepstone for jobs: {', '.join(keywords)}")
        jobs = []
        
        for keyword in keywords:
            try:
                params = {
                    'fulltext': keyword,
                    'ps': 1,
                    'sort': 'jobPostDate-desc'
                }
                
                response = self.fetch_page(self.base_url, params=params)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Stepstone job listings
                job_listings = soup.find_all('article', {'class': 'listing'})
                
                for job in job_listings[:50]:  # Limit results
                    try:
                        title_elem = job.find('h2', {'class': 'listing-job-headline'})
                        company_elem = job.find('p', {'class': 'listing-company-name'})
                        link_elem = job.find('a', {'class': 'listing-link'})
                        date_elem = job.find('span', {'class': 'listing-publish-date'})
                        
                        if title_elem and company_elem and link_elem:
                            job_url = link_elem.get('href', '')
                            if not job_url.startswith('http'):
                                job_url = urljoin(self.base_url, job_url)
                            
                            job_data = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'url': job_url,
                                'posted_date': self.parse_date(date_elem.text.strip()) if date_elem else None,
                                'board': 'Stepstone',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing Stepstone job: {str(e)}")
                        continue
                
                time.sleep(2)
            
            except Exception as e:
                logger.error(f"Error searching Stepstone for '{keyword}': {str(e)}")
                continue
        
        self.jobs.extend(jobs)
        logger.info(f"Found {len(jobs)} jobs on Stepstone")
        return jobs


class XingScraper(JobScraper):
    """Scraper for XING job postings"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.xing.com/jobs"
    
    def search(self, keywords: List[str]):
        """Search XING for jobs"""
        logger.info(f"Searching XING for jobs: {', '.join(keywords)}")
        jobs = []
        
        for keyword in keywords:
            try:
                params = {
                    'query': keyword,
                    'location[country]': 'de',
                    'sort': 'date'
                }
                
                response = self.fetch_page(self.base_url, params=params)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # XING job listings
                job_listings = soup.find_all('article', {'class': 'job-item'})
                
                for job in job_listings[:50]:
                    try:
                        title_elem = job.find('h2', {'class': 'job-item__title'})
                        company_elem = job.find('p', {'class': 'job-item__company'})
                        link_elem = job.find('a', {'class': 'job-item__link'})
                        date_elem = job.find('span', {'class': 'job-item__date'})
                        
                        if title_elem and company_elem and link_elem:
                            job_url = link_elem.get('href', '')
                            if not job_url.startswith('http'):
                                job_url = urljoin(self.base_url, job_url)
                            
                            job_data = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'url': job_url,
                                'posted_date': self.parse_date(date_elem.text.strip()) if date_elem else None,
                                'board': 'XING',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing XING job: {str(e)}")
                        continue
                
                time.sleep(2)
            
            except Exception as e:
                logger.error(f"Error searching XING for '{keyword}': {str(e)}")
                continue
        
        self.jobs.extend(jobs)
        logger.info(f"Found {len(jobs)} jobs on XING")
        return jobs


class IndeedScraper(JobScraper):
    """Scraper for Indeed job postings"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://de.indeed.com/jobs"
    
    def search(self, keywords: List[str]):
        """Search Indeed for jobs"""
        logger.info(f"Searching Indeed for jobs: {', '.join(keywords)}")
        jobs = []
        
        for keyword in keywords:
            try:
                params = {
                    'q': keyword,
                    'l': 'Germany',
                    'sort': 'date',
                    'fromage': 1  # Last 24 hours
                }
                
                response = self.fetch_page(self.base_url, params=params)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Indeed job listings
                job_listings = soup.find_all('div', {'class': 'job_seen_beacon'})
                
                for job in job_listings[:50]:
                    try:
                        title_elem = job.find('h2', {'class': 'jobTitle'})
                        company_elem = job.find('span', {'class': 'companyName'})
                        link_elem = job.find('a', {'class': 'jcs-JobTitle'})
                        date_elem = job.find('span', {'class': 'date'})
                        
                        if title_elem and company_elem and link_elem:
                            job_url = link_elem.get('href', '')
                            if not job_url.startswith('http'):
                                job_url = urljoin(self.base_url, job_url)
                            
                            job_data = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip(),
                                'url': job_url,
                                'posted_date': self.parse_date(date_elem.text.strip()) if date_elem else None,
                                'board': 'Indeed',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing Indeed job: {str(e)}")
                        continue
                
                time.sleep(2)
            
            except Exception as e:
                logger.error(f"Error searching Indeed for '{keyword}': {str(e)}")
                continue
        
        self.jobs.extend(jobs)
        logger.info(f"Found {len(jobs)} jobs on Indeed")
        return jobs


class CompanyWebsiteScraper(JobScraper):
    """Scraper for company career pages"""
    
    def search_company_careers(self, company_name: str, careers_url: str):
        """Search a company's careers page for job postings"""
        logger.info(f"Searching {company_name} careers page")
        jobs = []
        
        try:
            response = self.fetch_page(careers_url)
            if not response:
                return jobs
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for job links and titles
            # This is a generic approach - some companies have different structures
            job_elements = soup.find_all(['a', 'div'], string=True)
            
            for element in job_elements:
                text = element.text.lower() if element.text else ""
                if any(keyword in text for keyword in ['job', 'position', 'vacancy', 'opening', 'stelle', 'position']):
                    try:
                        # Try to extract URL
                        if element.name == 'a':
                            job_url = element.get('href', '')
                            if not job_url.startswith('http'):
                                job_url = urljoin(careers_url, job_url)
                            
                            job_data = {
                                'title': element.text.strip()[:100],
                                'company': company_name,
                                'url': job_url,
                                'posted_date': None,
                                'board': 'Company Website',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing company job: {str(e)}")
                        continue
            
            time.sleep(1)
        
        except Exception as e:
            logger.error(f"Error searching {company_name}: {str(e)}")
        
        self.jobs.extend(jobs)
        return jobs


class GoogleJobsScraper(JobScraper):
    """Scraper for Google Jobs search results"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.google.com/search"
    
    def search(self, keywords: List[str]):
        """Search Google Jobs for postings"""
        logger.info(f"Searching Google Jobs for: {', '.join(keywords)}")
        jobs = []
        
        for keyword in keywords:
            try:
                search_query = f"{keyword} jobs Germany site:google.com/jobs"
                params = {
                    'q': search_query,
                }
                
                response = self.fetch_page(self.base_url, params=params)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Google job listings
                job_listings = soup.find_all('div', {'class': 'g'})
                
                for job in job_listings[:20]:
                    try:
                        link_elem = job.find('a', {'class': 'l'})
                        title_elem = job.find('h3')
                        
                        if link_elem and title_elem:
                            job_data = {
                                'title': title_elem.text.strip(),
                                'company': 'Unknown',
                                'url': link_elem.get('href', ''),
                                'posted_date': None,
                                'board': 'Google',
                                'location': 'Germany',
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error parsing Google job: {str(e)}")
                        continue
                
                time.sleep(2)
            
            except Exception as e:
                logger.error(f"Error searching Google Jobs for '{keyword}': {str(e)}")
                continue
        
        self.jobs.extend(jobs)
        logger.info(f"Found {len(jobs)} jobs on Google")
        return jobs
