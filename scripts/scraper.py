#!/usr/bin/env python3
"""
Kamdhondho - European Internship Job Scraper
Searches for internships matching CV skills and updates jobs.json + archive.json

CV Skills: Python, C++, MERN, IoT, TensorFlow, CPLEX, PTV Vissim, MATLAB/Simulink, Wireshark, AWS IoT Core
Focus: Software Engineering, IoT Security, Smart Mobility, Traffic Modeling, Optimization
"""

import json
import os
import re
import sys
import time
import random
import hashlib
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta
from typing import Optional

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
JOBS_FILE = os.path.join(PUBLIC_DIR, 'jobs.json')
ARCHIVE_FILE = os.path.join(PUBLIC_DIR, 'archive.json')
SEEN_FILE = os.path.join(BASE_DIR, 'seen_jobs.json')

# User's skills from CV
TARGET_SKILLS = [
    'python', 'c++', 'c', 'javascript', 'typescript', 'mern',
    'react', 'node', 'tensorflow', 'machine learning', 'ai',
    'iot', 'embedded', 'stm32', 'esp32',
    'cplex', 'optimization', 'linear programming', 'simulation',
    'ptv vissim', 'ptv visum', 'matlab', 'simulink',
    'wireshark', 'gns3', 'aws', 'cloud', 'docker',
    'wifi', 'network security', 'cybersecurity',
    'traffic', 'mobility', 'urban', 'transportation'
]

# Target countries
TARGET_COUNTRIES = [
    'france', 'germany', 'netherlands', 'belgium', 'luxembourg',
    'switzerland', 'austria', 'poland', 'czech republic', 'slovakia',
    'spain', 'italy', 'ireland', 'denmark', 'sweden', 'norway',
    'united kingdom', 'uk', 'portugal', 'finland', 'estonia',
    'latvia', 'lithuania', 'romania', 'hungary'
]

# Search queries
SEARCH_QUERIES = [
    "internship 2027 software engineering europe",
    "stage PFE 2027 logiciel sécurité IoT",
    "internship 2027 smart mobility optimization",
    "internship 2027 IoT security python C++",
    "praktikum 2027 software entwickler",
    "internship 2027 urban mobility data analysis",
    "stage 2027 mobilité intelligente France",
    "internship 2027 reinforcement learning optimization",
    "praktikum 2027 IoT embedded systems",
    "internship 2027 traffic simulation software",
]

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
]

# SSL context (ignore cert errors for compatibility)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fetch(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch URL with retry and timeout."""
    for attempt in range(3):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout)
            return response.read().decode('utf-8', errors='replace')[:50000]
        except Exception as e:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
            else:
                log(f"  Failed: {url[:80]}... ({str(e)[:50]})")
                return None


def ddg_search(query: str, n: int = 5) -> list[tuple[str, str]]:
    """Search DuckDuckGo HTML and return (title, url) pairs."""
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    html = fetch(url, timeout=20)
    if not html or 'anomaly' in html.lower() or 'captcha' in html.lower():
        return []
    
    links = re.findall(r'class="result__a"[^>]*href="([^"]+)"', html)
    titles = re.findall(r'class="result__a"[^>]*>([^<]+)</a>', html)
    
    results = []
    for i, link in enumerate(links):
        if link.startswith('//duckduckgo.com/l/?uddg='):
            url = urllib.parse.unquote(link[26:].split('&rut=')[0])
        elif link.startswith('http'):
            url = link
        else:
            continue
        
        url = re.sub(r'[?&]rut=[^&"]+', '', url)
        title = titles[i].strip()[:120] if i < len(titles) else "?"
        title = re.sub(r'\s+[-|]\s*(LinkedIn|Indeed|StepStone|Glassdoor).*$', '', title, flags=re.I)
        results.append((title.strip(), url))
    
    return results[:n]


def verify_url(url: str) -> bool:
    """Verify URL returns a valid job page (not 404, not redirect, has content)."""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml',
        }
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, context=ssl_ctx, timeout=10)
        
        # Check status code
        if response.status >= 400:
            return False
        
        # Check final URL (catches redirects)
        final_url = response.geturl()
        if '404' in final_url.lower() or 'not-found' in final_url.lower():
            return False
        
        # Check content length (very short = probably not a real job page)
        content = response.read().decode('utf-8', errors='replace')[:5000]
        if len(content) < 500:
            return False
        
        # Check for common "page not found" indicators
        if any(text in content.lower() for text in [
            'page not found', '404 not found', 'job not found',
            'position not available', 'no longer available'
        ]):
            return False
        
        return True
    except:
        return False


def extract_job_details(url: str, title: str = "") -> Optional[dict]:
    """Fetch job page, verify it's real, and extract details."""
    # First verify the URL is valid
    if not verify_url(url):
        log(f"    ⚠️  URL verification failed, skipping")
        return None
    
    html = fetch(url, timeout=10)
    if not html:
        return None
    
    tl = html.lower()
    
    # Must be an internship
    internship_keywords = ['internship', 'intern', 'stage', 'pfe', 'praktikum', 'traineeship', 'stagiaire']
    if not any(k in tl for k in internship_keywords):
        return None
    
    # Exclude senior positions
    senior_keywords = ['senior', 'staff', 'lead', 'principal', 'director', 'vp', 'head of']
    if any(k in tl for k in senior_keywords):
        return None
    
    # Extract title from page if not provided
    if not title:
        tm = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
        if tm:
            title = tm.group(1).strip()[:120]
            title = re.sub(r'\s+[-|]\s*(Careers?|Jobs?|Indeed|LinkedIn|StepStone).*$', '', title, flags=re.I)
    
    # Extract company
    company = "Unknown"
    for pattern in [
        r'"company"\s*:\s*"([^"]+)"',
        r'itemprop="orgName"[^>]*>([^<]+)',
        r'"employer"\s*:\s*"([^"]+)"',
        r'org-name">([^<]+)',
        r'company-name">([^<]+)',
    ]:
        m = re.search(pattern, html, re.I)
        if m:
            company = m.group(1).strip()[:80]
            break
    
    # Extract location
    location = "Unknown"
    country = "Unknown"
    loc_patterns = [
        r'"location"\s*:\s*"([^"]+)"',
        r'itemprop="address"[^>]*>([^<]+)',
        r'job-location[^>]*>([^<]+)',
        r'workplace[^>]*>([^<]+)',
    ]
    for pattern in loc_patterns:
        m = re.search(pattern, html, re.I)
        if m:
            loc = m.group(1).strip()[:100]
            # Clean up location
            loc = re.sub(r'<[^>]+>', '', loc)
            loc = re.sub(r'\s+', ' ', loc).strip()
            
            # Detect country
            for c in TARGET_COUNTRIES:
                if c in loc.lower():
                    country = c.capitalize()
                    # Try to extract city
                    city_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', loc)
                    if city_match:
                        location = city_match.group(1)
                    else:
                        location = loc[:50]
                    break
            else:
                location = loc[:50]
            break
    
    # Extract skills from description
    skills = []
    for skill in TARGET_SKILLS:
        if skill in tl:
            skills.append(skill.title() if len(skill) < 10 else skill.upper() if len(skill) <= 5 else skill)
    skills = list(dict.fromkeys(skills))[:10]  # Deduplicate, max 10
    
    # Check for 2027
    has_2027 = '2027' in tl
    
    # Calculate match score
    match_score = len(skills) + (2 if has_2027 else 0) + (1 if country != "Unknown" else 0)
    
    # Generate ID (hash of URL)
    job_id = hashlib.md5(url.encode()).hexdigest()[:12]
    
    # Generate match rationale
    if skills:
        rationale = f"Matches skills: {', '.join(skills[:3])}"
        if has_2027:
            rationale += " | 2027 start date"
    else:
        rationale = "Relevant internship opportunity"
    
    return {
        'id': job_id,
        'title': title,
        'company': company,
        'location': location,
        'country': country,
        'startDate': '2027' if has_2027 else 'TBD',
        'duration': '6 months' if '6' in tl or 'six' in tl else 'TBD',
        'platform': get_platform(url),
        'url': url,
        'matchRationale': rationale,
        'skills': skills,
        'postedDate': datetime.now().strftime('%Y-%m-%d'),
        'archived': False,
        'matchScore': match_score,
    }


def get_platform(url: str) -> str:
    """Determine platform from URL."""
    url_lower = url.lower()
    if 'linkedin' in url_lower:
        return 'LinkedIn'
    elif 'indeed' in url_lower:
        return 'Indeed'
    elif 'stepstone' in url_lower:
        return 'StepStone'
    elif 'glassdoor' in url_lower:
        return 'Glassdoor'
    elif 'jobteaser' in url_lower:
        return 'JobTeaser'
    elif 'welcome' in url_lower and 'jungle' in url_lower:
        return 'Welcome to the Jungle'
    elif 'internhunt' in url_lower:
        return 'InternHunt'
    elif 'tech-internships' in url_lower:
        return 'Tech-Internships.eu'
    elif 'hellowork' in url_lower:
        return 'HelloWork'
    elif 'startup.jobs' in url_lower:
        return 'Startup.jobs'
    elif 'careers' in url_lower:
        return 'Company Careers'
    else:
        return 'Other'


def load_seen() -> set:
    """Load previously seen job URLs."""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            pass
    return set()


def save_seen(seen: set):
    """Save seen job URLs."""
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(seen), f)


def load_archive() -> list[dict]:
    """Load existing archive."""
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('jobs', [])
        except:
            pass
    return []


def save_archive(jobs: list[dict]):
    """Save archive."""
    data = {
        'jobs': jobs,
        'lastUpdated': datetime.now().isoformat(),
        'totalInArchive': len(jobs),
    }
    with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_active(jobs: list[dict]):
    """Save active jobs."""
    data = {
        'jobs': jobs,
        'lastUpdated': datetime.now().isoformat(),
        'totalFound': len(jobs),
    }
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    log("=" * 60)
    log("Kamdhondho Job Scraper Starting")
    log("=" * 60)
    
    seen = load_seen()
    archive = load_archive()
    archive_urls = {job['url'] for job in archive}
    
    new_jobs = []
    new_archive_additions = []
    
    # Run searches
    queries_to_run = min(5, len(SEARCH_QUERIES))
    for i, query in enumerate(SEARCH_QUERIES[:queries_to_run], 1):
        log(f"\n[{i}/{queries_to_run}] Searching: {query[:60]}...")
        results = ddg_search(query, n=5)
        log(f"  Found {len(results)} results")
        
        for title, url in results:
            # Skip if already seen
            if url in seen or url in archive_urls:
                continue
            
            # Skip listing pages
            if any(d in url for d in ['/jobs/internship/', '/jobs/software/', '/jobs/praktikum/']):
                continue
            
            seen.add(url)
            log(f"  Processing: {title[:50]}...")
            
            job = extract_job_details(url, title)
            if job:
                job['archived'] = True
                new_jobs.append(job)
                new_archive_additions.append(job)
                archive_urls.add(url)
                log(f"  ✓ Added: {job['title'][:50]} | {job['company']} | {job['country']}")
            
            time.sleep(2 + random.uniform(0, 1))
        
        time.sleep(5 + random.uniform(0, 3))
    
    # Save seen
    save_seen(seen)
    
    # Save active jobs (top 50 by match score)
    new_jobs.sort(key=lambda x: x.get('matchScore', 0), reverse=True)
    active_jobs = new_jobs[:50]
    save_active(active_jobs)
    log(f"\n✅ Saved {len(active_jobs)} active jobs to jobs.json")
    
    # Update archive (append new, don't overwrite)
    if new_archive_additions:
        archive.extend(new_archive_additions)
        save_archive(archive)
        log(f"✅ Appended {len(new_archive_additions)} jobs to archive.json (total: {len(archive)})")
    
    log("\n" + "=" * 60)
    log(f"Summary: {len(new_jobs)} new jobs found, {len(archive)} total in archive")
    log("=" * 60)
    
    return len(new_jobs)


if __name__ == '__main__':
    # Ensure public directory exists
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    # Create initial JSON files if they don't exist
    if not os.path.exists(JOBS_FILE):
        save_active([])
        log(f"Created initial {JOBS_FILE}")
    
    if not os.path.exists(ARCHIVE_FILE):
        save_archive([])
        log(f"Created initial {ARCHIVE_FILE}")
    
    try:
        main()
    except KeyboardInterrupt:
        log("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        log(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)