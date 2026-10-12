# 🎯 Kamdhondho - European Internship Job Board

A personalized, automated job board for finding internships across Europe matching your background in **Software Engineering, IoT Security, Smart Mobility, Traffic Modeling, and Optimization**.

## ✨ Features

- **🔍 Automated Daily Scraping** - Searches LinkedIn, Indeed, StepStone, Glassdoor, and more
- **📚 Historical Archive System** - Never lose a job listing - every job is archived permanently
- **⚡ Active vs Archive View** - Toggle between recent drops and all-time history
- **🔖 Bookmark System** - Save jobs you're interested in (localStorage)
- **🎨 Modern UI** - Clean SaaS dashboard with Dark/Light mode
- **🔎 Advanced Filters** - Search by country, skill, platform, keywords
- **📊 Match Rationale** - See why each job matches your CV
- **🌍 Multi-Platform** - Aggregates from 10+ job platforms
- **🚀 Deployment Ready** - Netlify, Vercel, or GitHub Pages

## 🛠️ Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Automation**: Python + GitHub Actions
- **Deployment**: Netlify / Vercel / GitHub Pages

## 📁 Project Structure

```
Kamdhondho/
├── public/
│   ├── jobs.json          # Active jobs (daily updated)
│   └── archive.json       # All-time archive (appended)
├── src/
│   ├── components/
│   │   ├── Navbar.tsx     # Top navigation with dark mode toggle
│   │   ├── JobCard.tsx    # Job listing card component
│   │   └── FilterBar.tsx  # Search and filter controls
│   ├── hooks/
│   │   ├── useJobs.ts     # Job data fetching and filtering
│   │   ├── useBookmarks.ts# Bookmark management (localStorage)
│   │   └── useTheme.ts    # Dark/Light mode toggle
│   ├── App.tsx            # Main application component
│   ├── main.tsx           # Entry point
│   ├── index.css          # Global styles
│   └── types.ts           # TypeScript type definitions
├── scripts/
│   └── scraper.py         # Python job scraper
├── .github/
│   └── workflows/
│       └── daily-update.yml # GitHub Actions automation
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── netlify.toml           # Netlify deployment config
└── vercel.json            # Vercel deployment config
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd Kamdhondho
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

### 3. Build for Production

```bash
npm run build
```

### 4. Preview Production Build

```bash
npm run preview
```

## 🔄 Running the Scraper

### Manual Run

```bash
python scripts/scraper.py
```

### What the Scraper Does

1. Searches DuckDuckGo for internship listings matching your skills
2. Extracts job details (title, company, location, skills, etc.)
3. Filters based on CV skills (Python, C++, IoT, etc.)
4. Saves new jobs to `public/jobs.json` (active)
5. Appends to `public/archive.json` (never overwrites)
6. Tracks seen URLs in `seen_jobs.json` (deduplication)

### Target Skills

The scraper looks for internships matching:
- **Languages**: Python, C++, C, JavaScript, TypeScript
- **Frameworks**: React, MERN, TensorFlow
- **Tools**: CPLEX, PTV Vissim, MATLAB, Simulink
- **Domains**: IoT, Security, Mobility, Optimization, Traffic
- **Infrastructure**: AWS, Docker, Cloud, Embedded

### Target Countries

France, Germany, Netherlands, Belgium, Switzerland, Austria, Poland, Czech Republic, Slovakia, Spain, Italy, Ireland, Denmark, Sweden, Norway, UK, Portugal, Finland, Estonia, Latvia, Lithuania, Romania, Hungary

## 🤖 GitHub Actions Automation

### Setup

1. Push your repository to GitHub
2. GitHub Actions will automatically detect the workflow
3. Jobs will update daily at 8:00 AM UTC

### Manual Trigger

1. Go to GitHub Actions tab
2. Select "Daily Job Update" workflow
3. Click "Run workflow"
4. Optionally choose run type (search/update/archive)

### Workflow Details

- **Schedule**: Every day at 8:00 AM UTC
- **Timeout**: 15 minutes
- **Actions**:
  - Checks out repository
  - Sets up Python 3.11
  - Runs scraper
  - Commits changes if new jobs found
  - Reports summary

## 🌐 Deployment

### Option 1: Netlify (Recommended)

1. Push repository to GitHub
2. Go to https://netlify.com
3. Click "Add new site" → "Import an existing project"
4. Select your GitHub repository
5. Build command: `npm run build`
6. Publish directory: `dist`
7. Click "Deploy"

**Netlify.toml** is already configured.

### Option 2: Vercel

1. Push repository to GitHub
2. Go to https://vercel.com
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Framework: Vite (auto-detected)
6. Build command: `npm run build`
7. Output directory: `dist`
8. Click "Deploy"

**vercel.json** is already configured.

### Option 3: GitHub Pages

1. Install gh-pages: `npm install -D gh-pages`
2. Add to package.json:
   ```json
   "scripts": {
     "deploy": "gh-pages -d dist"
   }
   ```
3. Run: `npm run build && npm run deploy`
4. Configure Pages in GitHub repository settings

## 🎨 Customization

### Add New Skills to Scanner

Edit `scripts/scraper.py` and add to `TARGET_SKILLS`:

```python
TARGET_SKILLS = [
    # ... existing skills ...
    'your_new_skill',
]
```

### Add New Search Queries

Edit `scripts/scraper.py` and add to `SEARCH_QUERIES`:

```python
SEARCH_QUERIES = [
    # ... existing queries ...
    "your new search query",
]
```

### Change Update Schedule

Edit `.github/workflows/daily-update.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC
  # OR
  - cron: '*/2 * * * *'  # Every 2 hours
```

### Customize Colors

Edit `tailwind.config.js` to change the primary color scheme.

## 📊 Job Data Format

Each job in `jobs.json` and `archive.json` has this structure:

```json
{
  "id": "unique-hash-id",
  "title": "Job Title",
  "company": "Company Name",
  "location": "City, Country",
  "country": "Country Name",
  "startDate": "2027",
  "duration": "6 months",
  "platform": "LinkedIn",
  "url": "https://apply-link.com",
  "matchRationale": "Why this job matches your CV",
  "skills": ["Python", "C++", "IoT"],
  "postedDate": "2026-10-12",
  "archived": true,
  "matchScore": 8
}
```

## 🔖 Bookmark System

Bookmarks are stored in your browser's localStorage. This means:
- ✅ Works without a backend
- ✅ Private to your browser
- ✅ Persists across sessions
- ❌ Not synced across devices

To share bookmarks, export them manually or implement a backend.

## 📈 Archive System

The archive system ensures you never lose a job listing:

1. **Daily Update**: `jobs.json` is overwritten with today's finds
2. **Permanent Archive**: `archive.json` is appended (never deleted)
3. **Deduplication**: `seen_jobs.json` tracks all seen URLs
4. **Browse History**: Toggle between Active and Archive views

## 🐛 Troubleshooting

### Scraper Not Finding Jobs

- DuckDuckGo may block automated requests
- Try increasing delays between requests
- Consider using a headless browser (Playwright/Puppeteer)

### Build Errors

```bash
# Clear build cache
rm -rf dist node_modules
npm install
npm run build
```

### Deployment Issues

- Ensure `dist` directory exists after build
- Check environment variables are set
- Verify repository is public (for free tier)

## 📝 License

MIT License - Feel free to use, modify, and share!

## 👤 Author

Built for **Muhammad Waseem** - Software Engineering, IoT Security, Smart Mobility & Optimization

## 🙏 Acknowledgments

- [Vite](https://vitejs.dev/) for build tooling
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Lucide React](https://lucide.dev/) for icons
- [GitHub Actions](https://github.com/features/actions) for automation

---

**Kamdhondho** - Your personalized European internship companion 🎯