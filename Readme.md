# RoleModelConnect: 2-Stage Data Pipeline

## Project Overview

**RoleModelConnect** is a comprehensive data pipeline project that builds a knowledge base of inspirational, real-world stories from well-known public figures who have navigated significant mental, emotional, or ethical challenges. The project demonstrates end-to-end data engineering skills through a two-phase approach: automated data collection and structured data curation.

📹 Demo Video
Watch the complete implementation walkthrough:
▶️ View Implementation Demo
Alternative if hosted online:
markdown[![Demo Video](https://img.shields.io/badge/Watch-Demo%20Video-red?style=for-the-badge&logo=youtube)](https://your-video-link-here.com)
Or embed directly (if viewing on GitHub/supporting platform):
markdownhttps://user-images.githubusercontent.com/your-video-file.mp4

## Table of Contents

- [Project Purpose](#project-purpose)
- [Pipeline Architecture](#pipeline-architecture)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Role Models & Sources](#role-models--sources)
- [Output Structure](#output-structure)
- [Challenges Faced](#challenges-faced)
- [Technical Details](#technical-details)
- [Ethical Considerations](#ethical-considerations)
- [Project Structure](#project-structure)

---

## Project Purpose

This project creates a validated, traceable dataset documenting how public figures have overcome personal challenges. The two-stage pipeline ensures:
- **Data Integrity**: Every piece of information is verifiable
- **Traceability**: All content can be traced back to legitimate sources
- **Reproducibility**: The entire process can be replicated and validated

---

## Pipeline Architecture

### Phase 1: Data Collection (Automated)
**Script**: `Data_Collection_24BDS058.ipynb`

The collection phase:
1. Accepts a role model's name as input
2. Takes a list of high-quality seed URLs (reputable interviews, articles, biographies)
3. Scrapes full text content from each URL
4. Saves raw, unstructured text to the `/Raw_Data/` folder
5. Handles errors gracefully and respects web scraping ethics

### Phase 2: Data Curation (Manual/Semi-Automated)
**Output**: `/Generated_JSON_Entries/`

The curation phase:
1. Uses **only** the raw text files from Phase 1
2. Identifies distinct challenges faced by each role model
3. Creates structured JSON entries following the required schema
4. Ensures all quotes and narratives are directly traceable to source files
5. Generates 2-3 entries per role model (minimum 5 total)

---

## Installation & Setup

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Required Libraries
```bash
pip install requests
pip install beautifulsoup4
pip install lxml
pip install pandas
pip install urllib3
```

### Alternative: Install from requirements.txt
```bash
pip install -r requirements.txt
```

---

## How to Run

### Phase 1: Data Collection

#### Option 1: Jupyter Notebook
```bash
# Open the notebook
jupyter notebook Data_Collection_24BDS058.ipynb

# Follow the instructions in the notebook cells
```

#### Option 2: Python Script
```python
# Run the collection script
python Data_Collection_24BDS058.py

# The script will prompt you for:
# 1. Role Model Name (e.g., "Selena Gomez")
# 2. List of seed URLs
```

#### Example Usage
```python
role_model = "Selena Gomez"
seed_urls = [
    "https://www.vogue.com/article/selena-gomez-interview-2023",
    "https://www.harpersbazaar.com/celebrity/latest/selena-gomez-mental-health",
    "https://time.com/selena-gomez-story/"
]

# Script automatically:
# - Scrapes content from each URL
# - Saves to /Raw_Data/SelenaGomez_Source_1.txt, etc.
# - Handles errors and rate limiting
```

### Phase 2: Data Curation

#### Manual Approach
1. Open raw text files from `/Raw_Data/`
2. Read through content and identify distinct challenges
3. Extract relevant information for each JSON field
4. Create JSON files following the naming convention: `RoleModelName_StoryNumber_24BDS058.json`

#### Semi-Automated Approach (Recommended)
```python
# Run the curation helper script
python Curation_Helper.py

# The script will:
# 1. Load a raw text file
# 2. Prompt you to fill in each JSON field
# 3. Validate the schema
# 4. Save the structured JSON file
```

---

## Role Models & Sources

### Role Model 1: Virat Kohli

**Sources**:
1. **Source 1**: "https://www.hindustantimes.com/cricket/virat-kohli-says-he-went-through-depression-during-england-tour-in-2014-in-a-podcast-with-mark-nicholas-101613719225354.html"
   - **Type**: Interview
   - **Publisher**: Hindustan Times
   - **File**: `Virat_Kohli_Source_1.txt`
   
2. **Source 2**: "https://www.icc-cricket.com/news/virat-kohli-opens-up-about-his-struggles-with-mental-health"
   - **Type**: Article
   - **Publisher**: International Cricket Council (ICC)
   - **File**: `Virat_Kohli_Source_2.txt`

### Role Model 2: Michael Phelps

**Sources**:
1. **Source 1**: "https://www.additudemag.com/michael-phelps-adhd-advice-from-the-olympians-mom/"
   - **Type**: Interview
   - **Publisher**: "www.additudemag.com"
   - **File**: `Michael_Phelps_Source_1.txt`

2. **Source 2**: "https://edition.cnn.com/2018/01/19/health/michael-phelps-depression/index.html?sr=twCNN011918michael-phelps-depression0534PMVODtop/"
   - **Type**: Article
   - **Publisher**: CNN
   - **File**: `Michael_Phelps_Source_2.txt`

### Directory Layout
```
YourRollNumber.zip
│
├── Data_Collection_YourRollNumber.ipynb
├── README.md
├── Implementation_YourRollNumber.mp4
├── requirements.txt (optional)
│
├── Raw_Data/
│   ├── RoleModel1_Source_1.txt
│   ├── RoleModel1_Source_2.txt
│   ├── RoleModel2_Source_1.txt
│   └── ...
│
└── Generated_JSON_Entries/
    ├── RoleModel1_1_YourRollNumber.json
    ├── RoleModel1_2_YourRollNumber.json
    ├── RoleModel2_1_YourRollNumber.json
    └── ...
```

### JSON Schema

Each JSON file follows this structure:

```json
{
  "Role_Model_Name": "Full name of the individual",
  "Role_Model_Context": "Brief 1-sentence description of their role/profession",
  "Situation_Faced": "Specific emotional or psychological conflict navigated",
  "Challenge_Narrative": "2-3 sentence factual summary derived from raw text",
  "Mental_Health_Themes": [
    "theme1",
    "theme2",
    "theme3"
  ],
  "Coping_Strategies_Used": [
    "strategy1",
    "strategy2"
  ],
  "Key_Action_Taken": "Single decisive action the role model took",
  "Key_Quote_or_Insight": "Powerful direct quote from role model (present in raw text)",
  "Summary_Psychological": "2-3 sentence psychological lesson from this story",
  "Outcome_Resolution": "Behavioral or ethical resolution",
  "Source_Reference": "RoleModelName_Source_Number.txt"
}
```

### Available Mental Health Themes
- anxiety
- depression
- stress_management
- burnout
- grief
- addiction_recovery
- imposter_syndrome
- self_esteem
- relationship_challenges
- public_pressure

---

## Challenges Faced

### Challenge 1: robots.txt Restrictions
**Issue**: Some websites blocked automated scraping via robots.txt

**Solution**: 
- Implemented robots.txt checker before scraping
- Used alternative sources when blocked
- Added user-agent headers to identify the scraper

### Challenge 2: Dynamic Content Loading
**Issue**: Some websites load content via JavaScript

**Solution**:
- Used Selenium for JavaScript-heavy sites (if applicable)
- Focused on static content sources
- Selected articles with server-side rendering

### Challenge 3: Rate Limiting
**Issue**: Multiple rapid requests triggered rate limiting

**Solution**:
- Implemented delays between requests (2-3 seconds)
- Added retry logic with exponential backoff
- Cached successful responses

### Challenge 4: Content Extraction
**Issue**: Different websites have different HTML structures

**Solution**:
- Created flexible parsing functions
- Used multiple CSS selectors as fallbacks
- Manually verified extracted content quality

### Challenge 5: Data Traceability
**Issue**: Ensuring quotes and narratives are verifiable

**Solution**:
- Strict requirement: all JSON data must appear in raw files
- Cross-referenced each entry with source material
- Documented exact source file for each JSON entry

---

## Technical Details

### Web Scraping Implementation

#### Key Functions

**1. URL Validation**
```python
def validate_url(url):
    """Validates URL format and accessibility"""
    # Checks URL structure
    # Verifies domain accessibility
    # Returns True/False
```

**2. robots.txt Checker**
```python
def check_robots_txt(url):
    """Checks if scraping is allowed by robots.txt"""
    # Parses robots.txt
    # Checks user-agent permissions
    # Returns allowed/disallowed
```

**3. Content Scraper**
```python
def scrape_content(url, output_path):
    """Scrapes content from URL and saves to file"""
    # Sends HTTP request with headers
    # Parses HTML with BeautifulSoup
    # Extracts main content
    # Saves to specified path
```

**4. Batch Processing**
```python
def scrape_role_model(name, urls):
    """Processes all URLs for a given role model"""
    # Iterates through URL list
    # Calls scrape_content for each
    # Implements error handling
    # Saves with proper naming convention
```

### Error Handling

The scraper implements comprehensive error handling:
- **HTTP Errors**: Retry with exponential backoff
- **Timeout Errors**: Skip and log failed URLs
- **Parsing Errors**: Use alternative parsing methods
- **File I/O Errors**: Create directories as needed

### Rate Limiting Strategy

```python
# Respectful scraping parameters
REQUEST_DELAY = 2.5  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 15  # seconds
USER_AGENT = "RoleModelConnect-Educational-Scraper/1.0"
```

---

## Ethical Considerations

### Web Scraping Ethics

1. **robots.txt Compliance**
   - All scrapers check and respect robots.txt
   - Disallowed URLs are skipped automatically

2. **Rate Limiting**
   - Minimum 2-second delay between requests
   - No concurrent requests to same domain

3. **Server Load**
   - Limited to small number of pages per site
   - No recursive or deep crawling

4. **Source Selection**
   - Only public, reputable sources used
   - No paywalled or private content accessed
   - Focus on major publications and official interviews

5. **Data Usage**
   - Educational purpose only
   - Proper attribution maintained
   - No commercial use

### Privacy & Consent

- Only public figures with extensive public records
- Only publicly available information used
- No private or sensitive information collected
- All information verifiable through public sources

---

## Project Structure

### File Descriptions

#### `Data_Collection_24BDS058.ipynb`
Main scraping script that automates Phase 1. Contains:
- URL validation and robots.txt checking
- HTTP request handling with proper headers
- HTML parsing and content extraction
- File saving with naming conventions
- Error handling and logging

#### `README.md`
Comprehensive documentation (this file) covering:
- Complete pipeline explanation
- Installation and usage instructions
- Role models and sources list
- Challenges and solutions
- Technical implementation details

#### `Raw_Data/`
Contains all scraped raw text files:
- Named as `RoleModelName_Source_N.txt`
- Unstructured, complete text from sources
- Source material for all JSON entries

#### `Generated_JSON_Entries/`
Contains all structured JSON files:
- Named as `RoleModelName_N_[YourRollNumber].json`
- Schema-compliant structured data
- Traceable to raw data files
- Minimum 5 entries total

#### `Implementation_24BDS058.mp4`
Video demonstration showing:
- Phase 1: Running scraper and generating raw files
- Phase 2: Raw text to JSON curation process
- Complete pipeline walkthrough

---

## Validation & Verification

### Data Traceability Checklist

For each JSON entry, verify:
- [ ] `Key_Quote_or_Insight` appears verbatim in source file
- [ ] `Challenge_Narrative` facts are present in source file
- [ ] `Source_Reference` matches actual raw data filename
- [ ] `Coping_Strategies_Used` are mentioned in source
- [ ] `Key_Action_Taken` is documented in source

### Schema Validation

Each JSON file must have:
- [ ] All required fields present
- [ ] Correct data types (strings, arrays)
- [ ] Mental health themes from approved list
- [ ] 2-4 mental health themes selected
- [ ] Proper filename format

---

## Future Improvements

### Potential Enhancements

1. **Automated Curation**: NLP-based extraction of challenges and quotes
2. **Expanded Sources**: API integration for news aggregators
3. **Quality Scoring**: Automatic assessment of source reliability
4. **Duplicate Detection**: Identify similar stories across role models
5. **Database Integration**: Store structured data in database instead of JSON files

---

## Credits & Acknowledgments

**Project**: RoleModelConnect - Educational Data Pipeline
**Course**: Foundation of Machine Learning and Generative Learning
**Institution**: Indian Institute of Information Technology, Dharwad
**Submission Date**: 30/11/2025

**Developed by**: Priyanshu Mittal
**Roll Number**: 24BDS058

---

## Contact & Support

For questions or issues:
- **Email**: 24bds058@iiitdwd.ac.in
- **Roll Number**: 24BDS058

---

## License


This project is for educational purposes only. All scraped content remains property of original publishers. No commercial use permitted.

