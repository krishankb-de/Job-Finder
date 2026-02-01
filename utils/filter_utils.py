"""
Filtering and processing utilities for job data
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict
import re

logger = logging.getLogger(__name__)


class JobFilter:
    """Filter and process job postings"""
    
    def __init__(self, job_level_keywords: List[str], technical_keywords: List[str]):
        self.job_level_keywords = [kw.lower() for kw in job_level_keywords]
        self.technical_keywords = [kw.lower() for kw in technical_keywords]
    
    def is_entry_level(self, job_title: str, job_description: str = "") -> bool:
        """Check if job is entry level or junior"""
        text = f"{job_title} {job_description}".lower()
        
        for keyword in self.job_level_keywords:
            if keyword in text:
                return True
        
        # Check for salary indicators (if available)
        if any(neg_keyword in text for neg_keyword in ['senior', 'lead', 'principal', 'architect', 'manager']):
            return False
        
        return False
    
    def matches_technical_keywords(self, job_title: str, job_description: str = "") -> List[str]:
        """Find matching technical keywords in job posting"""
        text = f"{job_title} {job_description}".lower()
        matches = []
        
        for keyword in self.technical_keywords:
            # Use word boundary matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                matches.append(keyword)
        
        return list(set(matches))  # Remove duplicates
    
    def is_german_location(self, location: str) -> bool:
        """Check if job location is in Germany"""
        german_states = [
            'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen',
            'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
            'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
            'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen', 'Germany',
            'Deutschland', 'DE'
        ]
        
        location_lower = location.lower()
        return any(state.lower() in location_lower for state in german_states)
    
    def is_recent(self, posted_date: datetime, hours: int = 24) -> bool:
        """Check if job was posted within specified hours"""
        if posted_date is None:
            return True  # Include jobs with unknown dates
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            return posted_date >= cutoff_time
        except Exception as e:
            logger.warning(f"Error checking if date is recent: {str(e)}")
            return True
    
    def filter_jobs(self, jobs: List[Dict], hours: int = 24) -> List[Dict]:
        """Filter jobs based on criteria"""
        filtered_jobs = []
        
        for job in jobs:
            try:
                # Check if entry level
                if not self.is_entry_level(job.get('title', ''), job.get('description', '')):
                    continue
                
                # Check if location is Germany
                if not self.is_german_location(job.get('location', '')):
                    continue
                
                # Check if recent
                if not self.is_recent(job.get('posted_date'), hours):
                    continue
                
                # Check if has matching technical keywords
                matches = self.matches_technical_keywords(job.get('title', ''), job.get('description', ''))
                if matches:
                    job['keyword_matches'] = matches
                    filtered_jobs.append(job)
            
            except Exception as e:
                logger.warning(f"Error filtering job: {str(e)}")
                continue
        
        return filtered_jobs
    
    def deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on URL and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier
            identifier = (job.get('url', ''), job.get('company', ''), job.get('title', ''))
            
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        logger.info(f"Deduplicated {len(jobs)} jobs to {len(unique_jobs)} unique jobs")
        return unique_jobs
    
    def rank_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Rank jobs by relevance"""
        def calculate_score(job):
            score = 0
            
            # Technical keyword matches (weighted)
            matches = job.get('keyword_matches', [])
            score += len(matches) * 10
            
            # Bonus for specific keywords
            title_lower = job.get('title', '').lower()
            if 'ai' in title_lower or 'artificial intelligence' in title_lower:
                score += 5
            if 'data scientist' in title_lower or 'data science' in title_lower:
                score += 5
            if 'machine learning' in title_lower or 'ml engineer' in title_lower:
                score += 5
            
            # Recency bonus (if date available)
            if job.get('posted_date'):
                hours_ago = (datetime.now() - job.get('posted_date')).total_seconds() / 3600
                if hours_ago < 1:
                    score += 20
                elif hours_ago < 6:
                    score += 15
                elif hours_ago < 12:
                    score += 10
            
            return score
        
        # Sort by score descending
        ranked_jobs = sorted(jobs, key=calculate_score, reverse=True)
        
        for i, job in enumerate(ranked_jobs, 1):
            job['rank'] = i
        
        return ranked_jobs


class DataProcessor:
    """Process and clean job data"""
    
    @staticmethod
    def clean_job_data(job: Dict) -> Dict:
        """Clean and standardize job data"""
        cleaned = {
            'company_name': job.get('company', '').strip(),
            'job_title': job.get('title', '').strip(),
            'job_url': job.get('url', '').strip(),
            'posted_date': job.get('posted_date'),
            'job_board': job.get('board', 'Unknown'),
            'location': job.get('location', 'Unknown'),
            'job_level': 'Entry Level / Junior',
            'keyword_matches': ', '.join(job.get('keyword_matches', [])),
        }
        
        return cleaned
    
    @staticmethod
    def format_date(date_obj: datetime, format_str: str = "%d.%m.%Y %H:%M") -> str:
        """Format datetime object to string"""
        if date_obj is None:
            return "Unknown"
        
        try:
            return date_obj.strftime(format_str)
        except Exception as e:
            logger.warning(f"Error formatting date: {str(e)}")
            return "Unknown"
    
    @staticmethod
    def prepare_export_data(jobs: List[Dict]) -> List[Dict]:
        """Prepare job data for Excel export"""
        export_data = []
        
        for job in jobs:
            export_data.append({
                'Company Name': job.get('company_name', ''),
                'Job Title': job.get('job_title', ''),
                'Job URL': job.get('job_url', ''),
                'Posted Date': DataProcessor.format_date(job.get('posted_date')),
                'Job Board': job.get('job_board', ''),
                'Location': job.get('location', ''),
                'Job Level': job.get('job_level', ''),
                'Keywords Match': job.get('keyword_matches', ''),
            })
        
        return export_data
