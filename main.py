"""
Main orchestrator for the Job Finder application
"""

import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import (
    JOB_KEYWORDS, JOB_LEVEL_KEYWORDS, TECHNICAL_KEYWORDS,
    GERMAN_COMPANIES, CONFIG, LOGGING_CONFIG, EXPORT_CONFIG
)
from scrapers.job_scraper import (
    LinkedInScraper, StepstoneScraper, XingScraper, IndeedScraper,
    CompanyWebsiteScraper, GoogleJobsScraper, GoogleWebSearchScraper
)
from utils.filter_utils import JobFilter, DataProcessor
from utils.excel_exporter import ExcelExporter, CSVExporter


# Setup logging
def setup_logging():
    """Configure logging"""
    log_format = LOGGING_CONFIG['format']
    date_format = LOGGING_CONFIG['datefmt']
    log_level = LOGGING_CONFIG['level']
    log_file = CONFIG['log_file']
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(console_handler)
    
    return logger


class JobFinder:
    """Main Job Finder orchestrator"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.jobs = []
        self.filtered_jobs = []
        
        # Initialize scrapers
        self.linkedin_scraper = LinkedInScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.stepstone_scraper = StepstoneScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.xing_scraper = XingScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.indeed_scraper = IndeedScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.google_scraper = GoogleJobsScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.google_web_scraper = GoogleWebSearchScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        self.company_scraper = CompanyWebsiteScraper(
            timeout=CONFIG['timeout'],
            retry_attempts=CONFIG['retry_attempts'],
            retry_delay=CONFIG['retry_delay']
        )
        
        # Initialize job filter
        self.job_filter = JobFilter(JOB_LEVEL_KEYWORDS, TECHNICAL_KEYWORDS)
    
    def run(self):
        """Run the complete job search"""
        self.logger.info("=" * 80)
        self.logger.info("Starting Job Finder for German Companies")
        self.logger.info(f"Search Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 80)
        
        try:
            # Step 1: Search job boards
            self.logger.info("\n[STEP 1] Searching job boards...")
            self._search_job_boards()
            
            # Step 2: Search company career pages
            self.logger.info("\n[STEP 2] Searching company career pages...")
            self._search_company_careers()
            
            # Step 3: Filter and process jobs
            self.logger.info("\n[STEP 3] Filtering and processing jobs...")
            self._filter_and_process_jobs()
            
            # Step 4: Export results
            self.logger.info("\n[STEP 4] Exporting results...")
            export_path = self._export_results()
            
            # Print summary
            self._print_summary(export_path)
            
            self.logger.info("\n" + "=" * 80)
            self.logger.info("Job Finder completed successfully!")
            self.logger.info("=" * 80)
            
            return export_path
        
        except Exception as e:
            self.logger.error(f"Error in job finder: {str(e)}", exc_info=True)
            return None
    
    def _search_job_boards(self):
        """Search all job boards"""
        
        # Relevant keywords for German job search
        search_keywords = [
            "AI Engineer Germany",
            "Data Scientist Germany",
            "ML Engineer Germany",
            "Software Engineer Junior Germany",
            "Junior Developer Germany",
        ]
        
        self.logger.info("Searching LinkedIn...")
        self.linkedin_scraper.search(search_keywords[:3], location="Germany")
        self.jobs.extend(self.linkedin_scraper.jobs)
        self.logger.info(f"Found {len(self.linkedin_scraper.jobs)} jobs on LinkedIn")
        
        self.logger.info("Searching Stepstone...")
        self.stepstone_scraper.search([
            "Junior AI Engineer",
            "Data Scientist Einstieg",
            "ML Engineer Anfänger"
        ])
        self.jobs.extend(self.stepstone_scraper.jobs)
        self.logger.info(f"Found {len(self.stepstone_scraper.jobs)} jobs on Stepstone")
        
        self.logger.info("Searching XING...")
        self.xing_scraper.search([
            "Junior Softwareentwickler",
            "AI Engineer",
            "Data Scientist"
        ])
        self.jobs.extend(self.xing_scraper.jobs)
        self.logger.info(f"Found {len(self.xing_scraper.jobs)} jobs on XING")
        
        self.logger.info("Searching Indeed...")
        self.indeed_scraper.search([
            "Junior Software Engineer",
            "Data Scientist Entry Level",
            "ML Engineer"
        ])
        self.jobs.extend(self.indeed_scraper.jobs)
        self.logger.info(f"Found {len(self.indeed_scraper.jobs)} jobs on Indeed")
        
        self.logger.info("Searching Google Jobs...")
        self.google_scraper.search([
            "AI Engineer",
            "Data Scientist",
            "ML Engineer"
        ])
        self.jobs.extend(self.google_scraper.jobs)
        self.logger.info(f"Found {len(self.google_scraper.jobs)} jobs on Google")
        
        self.logger.info("Searching Google Web Search (with site filters)...")
        self.google_web_scraper.search(hours_back=CONFIG['hours_back'])
        self.jobs.extend(self.google_web_scraper.jobs)
        self.logger.info(f"Found {len(self.google_web_scraper.jobs)} jobs via Google Web Search")
        
        self.logger.info(f"Total jobs found from all boards: {len(self.jobs)}")
    
    def _search_company_careers(self):
        """Search company career pages"""
        company_count = 0
        success_count = 0
        
        for company_name, company_info in GERMAN_COMPANIES.items():
            company_count += 1
            careers_url = company_info.get('careers_page', company_info.get('url'))
            
            try:
                jobs = self.company_scraper.search_company_careers(company_name, careers_url)
                if jobs:
                    success_count += 1
                    self.logger.debug(f"Found {len(jobs)} jobs on {company_name}")
            except Exception as e:
                self.logger.debug(f"Error searching {company_name}: {str(e)}")
            
            # Limit searches to avoid overload
            if company_count % 10 == 0:
                self.logger.info(f"Searched {company_count} companies, found jobs on {success_count}")
        
        self.jobs.extend(self.company_scraper.jobs)
        self.logger.info(f"Completed company searches: {company_count} companies, found {len(self.company_scraper.jobs)} jobs")
    
    def _filter_and_process_jobs(self):
        """Filter jobs and prepare for export"""
        # Deduplicate
        self.jobs = self.job_filter.deduplicate_jobs(self.jobs)
        self.logger.info(f"Jobs after deduplication: {len(self.jobs)}")
        
        # Filter for entry level and recent
        self.filtered_jobs = self.job_filter.filter_jobs(self.jobs, hours=CONFIG['hours_back'])
        self.logger.info(f"Jobs after filtering (entry-level, Germany, recent): {len(self.filtered_jobs)}")
        
        # Rank jobs by relevance
        self.filtered_jobs = self.job_filter.rank_jobs(self.filtered_jobs)
        self.logger.info(f"Jobs ranked by relevance")
        
        # Clean data
        cleaned_jobs = []
        for job in self.filtered_jobs:
            cleaned_job = DataProcessor.clean_job_data(job)
            cleaned_jobs.append(cleaned_job)
        
        self.filtered_jobs = cleaned_jobs
    
    def _export_results(self):
        """Export results to Excel"""
        if not self.filtered_jobs:
            self.logger.warning("No jobs to export")
            return None
        
        # Try Excel export first
        excel_exporter = ExcelExporter(CONFIG['output_dir'])
        excel_path = excel_exporter.export_jobs_to_excel(
            self.filtered_jobs,
            EXPORT_CONFIG['excel_filename']
        )
        
        if excel_path:
            self.logger.info(f"Results exported to: {excel_path}")
            return excel_path
        
        # Fallback to CSV
        self.logger.info("Falling back to CSV export...")
        csv_exporter = CSVExporter(CONFIG['output_dir'])
        csv_path = csv_exporter.export_jobs_to_csv(
            self.filtered_jobs,
            EXPORT_CONFIG['excel_filename'].replace('.xlsx', '.csv')
        )
        
        if csv_path:
            self.logger.info(f"Results exported to: {csv_path}")
            return csv_path
        
        return None
    
    def _print_summary(self, export_path):
        """Print search summary"""
        print("\n" + "=" * 80)
        print("JOB SEARCH SUMMARY")
        print("=" * 80)
        print(f"Total Jobs Found (all sources): {len(self.jobs)}")
        print(f"Jobs After Filtering: {len(self.filtered_jobs)}")
        print(f"Search Hours: {CONFIG['hours_back']}")
        print(f"Search Date: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        
        if self.filtered_jobs:
            # Count by board
            board_counts = {}
            for job in self.filtered_jobs:
                board = job.get('job_board', 'Unknown')
                board_counts[board] = board_counts.get(board, 0) + 1
            
            print("\nJobs by Board:")
            for board, count in sorted(board_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {board}: {count}")
            
            print(f"\nTop 5 Jobs by Relevance:")
            for i, job in enumerate(self.filtered_jobs[:5], 1):
                print(f"  {i}. {job.get('job_title')} - {job.get('company_name')}")
                print(f"     Board: {job.get('job_board')} | Date: {job.get('posted_date')}")
        
        if export_path:
            print(f"\nResults exported to: {export_path}")
        
        print("=" * 80 + "\n")


def main():
    """Main entry point"""
    # Setup logging
    logger = setup_logging()
    
    try:
        # Create and run job finder
        job_finder = JobFinder()
        export_path = job_finder.run()
        
        if export_path:
            print(f"\n✓ Job search completed successfully!")
            print(f"✓ Results saved to: {export_path}")
            return 0
        else:
            print("\n✗ Job search completed with errors")
            return 1
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
