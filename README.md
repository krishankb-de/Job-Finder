# Job Finder for German Companies

A comprehensive Python application to search for entry-level and junior job positions in German companies across multiple job boards and company career pages.

## Features

✅ **Multi-Source Job Search**
- LinkedIn
- Stepstone
- XING
- Indeed
- Google Jobs
- Google Web Search (with advanced site filters)
- Company Career Pages (60+ German companies)

✅ **Smart Filtering**
- Entry-level and junior position filtering
- AI Engineer, Data Scientist, ML Engineer, SDE, Software Developer positions
- Last 24 hours job postings
- Germany location filtering
- Technical keyword matching

✅ **Data Processing**
- Deduplication of job postings
- Job relevance ranking
- Automatic data cleaning and standardization

✅ **Export to Excel**
- Professional Excel spreadsheet with formatted headers
- Clickable job URLs
- Summary sheet with statistics
- Fallback to CSV if needed

## Project Structure

```
Job Finder/
├── main.py                  # Main orchestrator script
├── requirements.txt         # Python dependencies
├── config/
│   ├── __init__.py
│   └── config.py           # Configuration, keywords, companies
├── scrapers/
│   ├── __init__.py
│   └── job_scraper.py      # Web scrapers for all job boards
├── utils/
│   ├── __init__.py
│   ├── filter_utils.py     # Job filtering and processing
│   └── excel_exporter.py   # Excel export functionality
├── output/                 # Generated Excel files
└── job_finder.log         # Application logs
```

## Installation

### 1. Clone or navigate to the project directory

```bash
cd "d:\Job FInder"
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the job search:

```bash
python main.py
```

The script will:
1. Search all job boards for relevant positions
2. Search company career pages
3. Filter and rank results
4. Export to Excel file
5. Print summary statistics

### Output

After running, you'll find:
- **Excel File**: `output/job_results_YYYYMMDD_HHMMSS.xlsx`
- **Log File**: `job_finder.log`

The Excel file contains:
- **Job Postings Sheet**: All filtered job postings with details
- **Summary Sheet**: Statistics and breakdown by job board

## Configuration

Edit `config/config.py` to customize:

### Job Keywords
```python
JOB_KEYWORDS = [
    "Junior AI Engineer",
    "Data Scientist Entry Level",
    # Add more...
]
```

### Technical Keywords
```python
TECHNICAL_KEYWORDS = [
    "ai",
    "machine learning",
    "python",
    # Add more...
]
```

### German Companies
```python
GERMAN_COMPANIES = {
    "Company Name": {
        "url": "https://company.com",
        "careers_page": "https://careers.company.com"
    },
    # Add more...
}
```

### Search Parameters
```python
CONFIG = {
    "max_results_per_board": 100,
    "hours_back": 24,  # Search last 24 hours
    "timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 5,
}
```

## Features Explained

### 1. Multi-Board Scraping
The application searches:
- **LinkedIn**: Official LinkedIn job search API
- **Stepstone**: German job board
- **XING**: German professional network
- **Indeed**: Global job search
- **Google Jobs**: Google job search integration
- **Google Web Search**: Advanced Google search with site filters for major job boards
  - Searches across: Stepstone, XING, LinkedIn, Indeed, Arbeitsagentur, MyWorkday, Greenhouse, Personio, SoftGarden, Join.com, Recruitee
  - Filters by: Last 24 hours, Germany/Deutschland location
  - Job titles: AI Engineer, Artificial Intelligence, Machine Learning, Data Scientist, Software Engineer
- **Company Websites**: Direct company career pages

### 2. Smart Filtering
Jobs are filtered based on:
- **Level**: Junior, Entry-level, Trainee, Graduate
- **Field**: AI, Data Science, ML, Software Development
- **Location**: Germany only
- **Recency**: Posted within last 24 hours
- **Keywords**: Technical skill matches

### 3. Job Ranking
Jobs are ranked by:
- Number of matching keywords
- Specific role relevance (bonus for AI/ML roles)
- Posting recency

### 4. Data Export
Creates professional Excel spreadsheet with:
- Formatted headers and alternating row colors
- Clickable job URLs
- Summary statistics
- Easy sorting and filtering

## Supported Job Titles and Keywords

### Entry-Level Positions
- Junior AI Engineer
- AI Engineer (Entry Level)
- Data Scientist Junior
- ML Engineer (Starting Career)
- Software Developer Trainee
- Graduate Software Engineer
- Junior Developer
- Einstiegsposition (German)

### Technical Fields
- AI / Artificial Intelligence
- Machine Learning
- Data Science
- Software Development
- Python, Java, C++
- Backend, Frontend, Full-Stack
- Web Development
- Deep Learning
- Neural Networks

## German Companies Included

The application searches 50+ major German companies including:
- **Large MNCs**: SAP, Siemens, BMW, Volkswagen, Deutsche Telekom
- **Tech Companies**: Zalando, N26, Flixbus, Wolt
- **AI/ML Focused**: Celonis, Rasa, Fraugster
- **Consulting**: McKinsey, Deloitte, EY, Accenture
- **Tech Giants**: Google, Amazon, Microsoft, IBM
- And many more...

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "openpyxl not found"
**Solution**: Install openpyxl separately:
```bash
pip install openpyxl
```

The application will automatically fall back to CSV export if openpyxl is not available.

### Issue: No jobs found
**Possible causes**:
- Job boards may require authentication (LinkedIn, XING)
- Websites may have changed their HTML structure
- Network/firewall issues

**Solutions**:
1. Check `job_finder.log` for detailed error messages
2. Verify internet connection
3. Check if websites are accessible
4. Update selectors in `job_scraper.py` if website structure changed

### Issue: Too many timeout errors
**Solution**: Increase timeout in config:
```python
CONFIG = {
    "timeout": 60,  # Increase from 30
}
```

## Advanced Usage

### Running with Specific Keywords

Modify `main.py` to search specific keywords:

```python
search_keywords = [
    "AI Engineer Germany",
    "Data Science Berlin",
    "ML Engineer Munich",
]
self.linkedin_scraper.search(search_keywords)
```

### Adding New Job Boards

Create a new scraper class in `scrapers/job_scraper.py`:

```python
class NewBoardScraper(JobScraper):
    def search(self, keywords):
        # Implementation
        pass
```

Then add to `main.py`:
```python
new_scraper = NewBoardScraper()
new_scraper.search(keywords)
self.jobs.extend(new_scraper.jobs)
```

### Customizing Export Format

Edit `excel_exporter.py` to change:
- Column names
- Styling (colors, fonts)
- Additional sheets
- Summary calculations

## Performance Notes

- **First run**: May take 5-10 minutes depending on number of companies and job boards
- **Network**: Respectful delays (2 seconds) between requests to avoid overload
- **Memory**: Efficient deduplication and filtering for large result sets
- **Output**: Typically 50-200 relevant jobs per search

## Dependencies

- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests
- **openpyxl**: Excel file generation
- **selenium**: Advanced web scraping (optional)
- **lxml**: HTML/XML processing
- **python-dateutil**: Date parsing

## Logs

The application logs all activities to:
- **Console**: Real-time progress updates
- **File**: `job_finder.log` for detailed debugging

Log levels:
- INFO: General progress information
- WARNING: Non-critical issues
- ERROR: Critical errors that prevent processing
- DEBUG: Detailed debugging information

## Legal Notice

This tool is for personal job search purposes. When using this tool:
- Respect robots.txt and website terms of service
- Use reasonable request delays
- Don't overload servers
- Some websites may require authentication
- LinkedIn and XING may have restrictions on automated access

## Future Enhancements

Planned features:
- [ ] Email notifications for new jobs
- [ ] Database storage of historical jobs
- [ ] Advanced filtering UI
- [ ] Job alert subscriptions
- [ ] Salary information extraction
- [ ] Application tracking
- [ ] Browser-based dashboard

## Support

For issues or questions:
1. Check `job_finder.log` for error messages
2. Verify all dependencies are installed
3. Ensure internet connection is active
4. Check if job boards are accessible

## License

This project is provided as-is for personal use.

---

**Happy Job Hunting! 🚀**
