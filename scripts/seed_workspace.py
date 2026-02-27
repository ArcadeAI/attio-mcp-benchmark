#!/usr/bin/env python3
"""
Attio MCP Benchmark — Workspace Seed Script

Seeds an Attio workspace with synthetic-but-realistic CRM data for
reproducible MCP toolkit benchmarking. Uses Fortune 100 companies
and their actual C-Suite executives (all public information).

WHY CUSTOM ATTRIBUTES?
======================
A fresh Attio workspace has ~15 default attributes per object. Real enterprise
workspaces have 30-70+. MCP toolkits that don't support field selection return
ALL attributes on every query, so attribute count directly drives token cost.

We add 15 realistic custom attributes (fields any B2B sales team would create)
to bring the workspace to ~30-35 attributes per object. This is intentionally
CONSERVATIVE — it understates what real enterprise workspaces look like, meaning
the benchmark ratios are lower bounds, not upper bounds.

If you want to see how ratios change with more attributes, add more custom
fields and re-run the benchmark. Ratios scale linearly with attribute count.

WHAT IT CREATES
===============
- 50 companies (F100 + well-known companies, real public data)
- ~100 contacts (real C-Suite executives, public figures)
- 50 deals (synthetic enterprise scenarios, various stages/values)
- 15 custom attributes on companies
- 10 custom attributes on deals

SCENARIO COVERAGE
=================
1. List all companies         → 50 companies exist
2. Deals by stage (Nurture)   → 22 deals in Nurture
3. Deals over $50K            → 25+ deals above $50K
4. Companies name has "Tech"  → 8 companies with "Tech" in name
5. Technology companies        → 23 companies in Technology
6. Deals before March 2026    → 20+ deals with close_date < 2026-03-01
7. Large Tech (compound)       → 10+ Technology companies with 100+ employees
8. Highest-value deal          → 1 clear winner ($480K Berkshire Hathaway deal)

USAGE
=====
    export ATTIO_API_KEY="your-sandbox-workspace-key"
    pip install httpx tiktoken
    python seed_workspace.py

REPRODUCIBILITY
===============
This script is idempotent for companies (upserts on domain) and people
(upserts on email). Deals are created fresh each run. For a clean start,
delete and recreate the workspace.

All company data is publicly available (SEC filings, Wikipedia, company
websites). Executive names are current as of early 2026.
"""

import os
import sys
import json
import time
import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("ATTIO_API_KEY")
if not API_KEY:
    print("Error: Set ATTIO_API_KEY environment variable")
    print("  export ATTIO_API_KEY='your-sandbox-key'")
    sys.exit(1)

BASE_URL = "https://api.attio.com/v2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
RATE_LIMIT_DELAY = 0.15  # seconds between API calls

client = httpx.Client(base_url=BASE_URL, headers=HEADERS, timeout=30)


# ---------------------------------------------------------------------------
# Custom Attributes
#
# These are fields any B2B sales team would create. They're not padding —
# they're the minimum set a real CRM would have beyond defaults.
# ---------------------------------------------------------------------------

COMPANY_CUSTOM_ATTRIBUTES = [
    {"title": "Industry", "api_slug": "industry", "type": "select",
     "description": "Primary industry vertical"},
    {"title": "Employee Count", "api_slug": "employee_count", "type": "number",
     "description": "Approximate number of employees"},
    {"title": "Annual Revenue", "api_slug": "annual_revenue", "type": "currency",
     "description": "Annual revenue in USD"},
    {"title": "Founded Year", "api_slug": "founded_year", "type": "number",
     "description": "Year the company was founded"},
    {"title": "Headquarters", "api_slug": "headquarters", "type": "text",
     "description": "HQ city and state"},
    {"title": "LinkedIn URL", "api_slug": "linkedin_url", "type": "text",
     "description": "Company LinkedIn page URL"},
    {"title": "Tech Stack", "api_slug": "tech_stack", "type": "text",
     "description": "Known technologies in use"},
    {"title": "Lead Source", "api_slug": "lead_source", "type": "select",
     "description": "How this company entered the pipeline"},
    {"title": "ICP Score", "api_slug": "icp_score", "type": "number",
     "description": "Ideal customer profile score (0-100)"},
    {"title": "Last Contacted", "api_slug": "last_contacted", "type": "date",
     "description": "Date of last outreach or interaction"},
    {"title": "Account Tier", "api_slug": "account_tier", "type": "select",
     "description": "Account classification by size"},
    {"title": "Funding Stage", "api_slug": "funding_stage", "type": "select",
     "description": "Current funding stage"},
    {"title": "Contract Status", "api_slug": "contract_status", "type": "select",
     "description": "Current contract status"},
    {"title": "Primary Use Case", "api_slug": "primary_use_case", "type": "text",
     "description": "Primary product use case for this account"},
    {"title": "Renewal Date", "api_slug": "renewal_date", "type": "date",
     "description": "Next contract renewal date"},
]

DEAL_CUSTOM_ATTRIBUTES = [
    {"title": "Lead Source", "api_slug": "deal_lead_source", "type": "select",
     "description": "How this deal originated"},
    {"title": "Next Step", "api_slug": "next_step", "type": "text",
     "description": "Next action item for this deal"},
    {"title": "Champion", "api_slug": "champion", "type": "text",
     "description": "Internal champion at the prospect"},
    {"title": "Competitor", "api_slug": "competitor", "type": "text",
     "description": "Primary competitor in this deal"},
    {"title": "Use Case", "api_slug": "use_case", "type": "text",
     "description": "Specific use case driving this deal"},
    {"title": "Contract Length (Months)", "api_slug": "contract_length_months", "type": "number",
     "description": "Proposed contract duration in months"},
    {"title": "Security Review Status", "api_slug": "security_review_status", "type": "select",
     "description": "Status of security/compliance review"},
    {"title": "Probability", "api_slug": "probability", "type": "number",
     "description": "Win probability percentage (0-100)"},
    {"title": "Loss Reason", "api_slug": "loss_reason", "type": "select",
     "description": "Reason deal was lost"},
    {"title": "Onboarding Date", "api_slug": "onboarding_date", "type": "date",
     "description": "Target onboarding start date"},
    {"title": "Close Date", "api_slug": "close_date", "type": "date",
     "description": "Expected or actual deal close date"},
]


# ---------------------------------------------------------------------------
# Company Data — 50 companies (F100 + well-known with "Tech" in name)
# All data is publicly available.
# ---------------------------------------------------------------------------

COMPANIES = [
    # ===== TECHNOLOGY (15) =====
    {"name": "Apple Inc.", "domain": "apple.com", "industry": "Technology", "employee_count": 166000, "annual_revenue_b": 416, "founded_year": 1976, "headquarters": "Cupertino, CA", "description": "Consumer electronics, software, and services company known for iPhone, Mac, iPad, and Apple Watch.", "ceo": {"first": "Tim", "last": "Cook", "title": "Chief Executive Officer"}, "exec2": {"first": "Kevan", "last": "Parekh", "title": "Chief Financial Officer"}},
    {"name": "Microsoft Corporation", "domain": "microsoft.com", "industry": "Technology", "employee_count": 228000, "annual_revenue_b": 282, "founded_year": 1975, "headquarters": "Redmond, WA", "description": "Global technology company providing cloud computing, productivity software, and enterprise solutions.", "ceo": {"first": "Satya", "last": "Nadella", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Amy", "last": "Hood", "title": "Chief Financial Officer"}},
    {"name": "Alphabet Inc.", "domain": "abc.xyz", "industry": "Technology", "employee_count": 183000, "annual_revenue_b": 400, "founded_year": 1998, "headquarters": "Mountain View, CA", "description": "Parent company of Google, operating the world's largest search engine, YouTube, and cloud platform.", "ceo": {"first": "Sundar", "last": "Pichai", "title": "Chief Executive Officer"}, "exec2": {"first": "Anat", "last": "Ashkenazi", "title": "Chief Financial Officer"}},
    {"name": "Meta Platforms, Inc.", "domain": "meta.com", "industry": "Technology", "employee_count": 74000, "annual_revenue_b": 165, "founded_year": 2004, "headquarters": "Menlo Park, CA", "description": "Social media and technology conglomerate operating Facebook, Instagram, WhatsApp, and Reality Labs.", "ceo": {"first": "Mark", "last": "Zuckerberg", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Susan", "last": "Li", "title": "Chief Financial Officer"}},
    {"name": "NVIDIA Corporation", "domain": "nvidia.com", "industry": "Technology", "employee_count": 36000, "annual_revenue_b": 131, "founded_year": 1993, "headquarters": "Santa Clara, CA", "description": "Semiconductor company designing GPUs and AI computing platforms for data centers, gaming, and autonomous vehicles.", "ceo": {"first": "Jensen", "last": "Huang", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Colette", "last": "Kress", "title": "Chief Financial Officer"}},
    {"name": "Broadcom Inc.", "domain": "broadcom.com", "industry": "Technology", "employee_count": 40000, "annual_revenue_b": 64, "founded_year": 1961, "headquarters": "Palo Alto, CA", "description": "Global technology company designing semiconductor and infrastructure software solutions.", "ceo": {"first": "Hock", "last": "Tan", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Kirsten", "last": "Spears", "title": "Chief Financial Officer"}},
    {"name": "Oracle Corporation", "domain": "oracle.com", "industry": "Technology", "employee_count": 162000, "annual_revenue_b": 57, "founded_year": 1977, "headquarters": "Austin, TX", "description": "Enterprise software company specializing in cloud infrastructure, database management, and business applications.", "ceo": {"first": "Safra", "last": "Catz", "title": "Chief Executive Officer"}, "exec2": {"first": "Larry", "last": "Ellison", "title": "Chairman and Chief Technology Officer"}},
    {"name": "Salesforce, Inc.", "domain": "salesforce.com", "industry": "Technology", "employee_count": 76000, "annual_revenue_b": 38, "founded_year": 1999, "headquarters": "San Francisco, CA", "description": "Cloud-based CRM platform provider offering sales, service, marketing, and analytics enterprise solutions.", "ceo": {"first": "Marc", "last": "Benioff", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Robin", "last": "Washington", "title": "Chief Operating and Financial Officer"}},
    {"name": "Cisco Systems, Inc.", "domain": "cisco.com", "industry": "Technology", "employee_count": 86000, "annual_revenue_b": 57, "founded_year": 1984, "headquarters": "San Jose, CA", "description": "Networking hardware and telecommunications company providing routers, switches, cybersecurity, and collaboration tools.", "ceo": {"first": "Chuck", "last": "Robbins", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Mark", "last": "Patterson", "title": "Chief Financial Officer"}},
    {"name": "International Business Machines Corporation", "domain": "ibm.com", "industry": "Technology", "employee_count": 282000, "annual_revenue_b": 63, "founded_year": 1911, "headquarters": "Armonk, NY", "description": "Multinational technology company providing hybrid cloud, AI, consulting, and enterprise computing solutions.", "ceo": {"first": "Arvind", "last": "Krishna", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "James", "last": "Kavanaugh", "title": "Chief Financial Officer"}},
    {"name": "Intel Corporation", "domain": "intel.com", "industry": "Technology", "employee_count": 109000, "annual_revenue_b": 53, "founded_year": 1968, "headquarters": "Santa Clara, CA", "description": "Semiconductor manufacturer producing processors and chips for computing, data centers, and IoT devices.", "ceo": {"first": "Lip-Bu", "last": "Tan", "title": "Chief Executive Officer"}, "exec2": {"first": "David", "last": "Zinsner", "title": "Chief Financial Officer"}},
    {"name": "Qualcomm Incorporated", "domain": "qualcomm.com", "industry": "Technology", "employee_count": 49000, "annual_revenue_b": 39, "founded_year": 1985, "headquarters": "San Diego, CA", "description": "Semiconductor and telecommunications company developing wireless technology, mobile chipsets, and 5G platforms.", "ceo": {"first": "Cristiano", "last": "Amon", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Akash", "last": "Palkhiwala", "title": "Chief Financial Officer"}},
    {"name": "Adobe Inc.", "domain": "adobe.com", "industry": "Technology", "employee_count": 30000, "annual_revenue_b": 22, "founded_year": 1982, "headquarters": "San Jose, CA", "description": "Software company providing creative, document management, and digital marketing solutions.", "ceo": {"first": "Shantanu", "last": "Narayen", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Dan", "last": "Durn", "title": "Chief Financial Officer"}},
    {"name": "Netflix, Inc.", "domain": "netflix.com", "industry": "Technology", "employee_count": 14000, "annual_revenue_b": 39, "founded_year": 1997, "headquarters": "Los Gatos, CA", "description": "Global streaming entertainment service offering original and licensed films, series, and games.", "ceo": {"first": "Ted", "last": "Sarandos", "title": "Co-Chief Executive Officer"}, "exec2": {"first": "Spencer", "last": "Neumann", "title": "Chief Financial Officer"}},
    {"name": "Advanced Micro Devices, Inc.", "domain": "amd.com", "industry": "Technology", "employee_count": 26000, "annual_revenue_b": 26, "founded_year": 1969, "headquarters": "Santa Clara, CA", "description": "Semiconductor company designing high-performance CPUs, GPUs, and adaptive computing solutions.", "ceo": {"first": "Lisa", "last": "Su", "title": "Chair and Chief Executive Officer"}, "exec2": {"first": "Jean", "last": "Hu", "title": "Chief Financial Officer"}},

    # ===== "TECH" IN NAME (8) — all contain the substring "Tech" =====
    {"name": "DXC Technology Company", "domain": "dxc.com", "industry": "Technology", "employee_count": 120000, "annual_revenue_b": 13, "founded_year": 2017, "headquarters": "Ashburn, VA", "description": "Global IT services company providing digital transformation, cloud, security, and analytics services.", "ceo": {"first": "Raul", "last": "Fernandez", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Rob", "last": "Del Bene", "title": "Chief Financial Officer"}},
    {"name": "Roper Technologies, Inc.", "domain": "ropertech.com", "industry": "Technology", "employee_count": 18000, "annual_revenue_b": 8, "founded_year": 1981, "headquarters": "Sarasota, FL", "description": "Diversified industrial company providing application-specific software and technology-enabled products.", "ceo": {"first": "Neil", "last": "Hunn", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Jason", "last": "Conley", "title": "Chief Financial Officer"}},
    {"name": "Agilent Technologies, Inc.", "domain": "agilent.com", "industry": "Technology", "employee_count": 18000, "annual_revenue_b": 7, "founded_year": 1999, "headquarters": "Santa Clara, CA", "description": "Life sciences and diagnostics company providing instruments, software, and services for laboratories.", "ceo": {"first": "Padraig", "last": "McDonnell", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Adam", "last": "Elinoff", "title": "Chief Financial Officer"}},
    {"name": "Zebra Technologies Corporation", "domain": "zebra.com", "industry": "Technology", "employee_count": 10000, "annual_revenue_b": 5, "founded_year": 1969, "headquarters": "Lincolnshire, IL", "description": "Enterprise asset intelligence company providing barcode printers, scanners, and RFID solutions.", "ceo": {"first": "Bill", "last": "Burns", "title": "Chief Executive Officer"}, "exec2": {"first": "Nathan", "last": "Winters", "title": "Chief Financial Officer"}},
    {"name": "Lumen Technologies, Inc.", "domain": "lumen.com", "industry": "Technology", "employee_count": 24000, "annual_revenue_b": 12, "founded_year": 1930, "headquarters": "Monroe, LA", "description": "Telecommunications company providing fiber networking, cloud connectivity, and enterprise security solutions.", "ceo": {"first": "Kate", "last": "Johnson", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Chris", "last": "Stansbury", "title": "Chief Financial Officer"}},
    {"name": "Seagate Technology Holdings plc", "domain": "seagate.com", "industry": "Technology", "employee_count": 30000, "annual_revenue_b": 10, "founded_year": 1978, "headquarters": "Fremont, CA", "description": "Data storage company manufacturing hard disk drives and solid-state drives for enterprise and consumer markets.", "ceo": {"first": "Dave", "last": "Mosley", "title": "Chief Executive Officer"}, "exec2": {"first": "Gianluca", "last": "Romano", "title": "Chief Financial Officer"}},
    {"name": "Microchip Technology Incorporated", "domain": "microchip.com", "industry": "Technology", "employee_count": 19000, "annual_revenue_b": 4, "founded_year": 1987, "headquarters": "Chandler, AZ", "description": "Semiconductor manufacturer providing microcontrollers and mixed-signal integrated circuits.", "ceo": {"first": "Steve", "last": "Sanghi", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Eric", "last": "Bjornholt", "title": "Chief Financial Officer"}},
    {"name": "Marvell Technology, Inc.", "domain": "marvell.com", "industry": "Technology", "employee_count": 7000, "annual_revenue_b": 6, "founded_year": 1995, "headquarters": "Wilmington, DE", "description": "Semiconductor company designing data infrastructure chips for cloud, enterprise networking, and 5G.", "ceo": {"first": "Matt", "last": "Murphy", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Willem", "last": "Meintjes", "title": "Chief Financial Officer"}},

    # ===== HEALTHCARE (6) =====
    {"name": "UnitedHealth Group Incorporated", "domain": "unitedhealthgroup.com", "industry": "Healthcare", "employee_count": 440000, "annual_revenue_b": 448, "founded_year": 1977, "headquarters": "Minnetonka, MN", "description": "Diversified healthcare company operating UnitedHealthcare insurance and Optum health services.", "ceo": {"first": "Stephen", "last": "Hemsley", "title": "Chief Executive Officer"}, "exec2": {"first": "Wayne", "last": "DeVeydt", "title": "Chief Financial Officer"}},
    {"name": "Johnson & Johnson", "domain": "jnj.com", "industry": "Healthcare", "employee_count": 138000, "annual_revenue_b": 94, "founded_year": 1886, "headquarters": "New Brunswick, NJ", "description": "Multinational pharmaceutical and medical technologies company.", "ceo": {"first": "Joaquin", "last": "Duato", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Joseph", "last": "Wolk", "title": "Chief Financial Officer"}},
    {"name": "Pfizer Inc.", "domain": "pfizer.com", "industry": "Healthcare", "employee_count": 83000, "annual_revenue_b": 62, "founded_year": 1849, "headquarters": "New York, NY", "description": "Global pharmaceutical and biotechnology company developing medicines and vaccines.", "ceo": {"first": "Albert", "last": "Bourla", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Dave", "last": "Denton", "title": "Chief Financial Officer"}},
    {"name": "Elevance Health, Inc.", "domain": "elevancehealth.com", "industry": "Healthcare", "employee_count": 100000, "annual_revenue_b": 176, "founded_year": 2004, "headquarters": "Indianapolis, IN", "description": "Health benefits company serving members through Blue Cross Blue Shield affiliated plans.", "ceo": {"first": "Gail", "last": "Boudreaux", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Mark", "last": "Kaye", "title": "Chief Financial Officer"}},
    {"name": "CVS Health Corporation", "domain": "cvshealth.com", "industry": "Healthcare", "employee_count": 300000, "annual_revenue_b": 358, "founded_year": 1963, "headquarters": "Woonsocket, RI", "description": "Health solutions company operating retail pharmacies and health insurance services.", "ceo": {"first": "David", "last": "Joyner", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Brian", "last": "Newman", "title": "Chief Financial Officer"}},
    {"name": "Abbott Laboratories", "domain": "abbott.com", "industry": "Healthcare", "employee_count": 114000, "annual_revenue_b": 42, "founded_year": 1888, "headquarters": "Abbott Park, IL", "description": "Global healthcare company manufacturing diagnostics, medical devices, and nutritionals.", "ceo": {"first": "Robert", "last": "Ford", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Philip", "last": "Boudreau", "title": "Chief Financial Officer"}},

    # ===== FINANCE (6) =====
    {"name": "JPMorgan Chase & Co.", "domain": "jpmorganchase.com", "industry": "Finance", "employee_count": 317000, "annual_revenue_b": 279, "founded_year": 2000, "headquarters": "New York, NY", "description": "Largest U.S. bank by assets, providing investment banking and financial services globally.", "ceo": {"first": "Jamie", "last": "Dimon", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Jeremy", "last": "Barnum", "title": "Chief Financial Officer"}},
    {"name": "Goldman Sachs Group, Inc.", "domain": "goldmansachs.com", "industry": "Finance", "employee_count": 46000, "annual_revenue_b": 54, "founded_year": 1869, "headquarters": "New York, NY", "description": "Global investment banking and financial services firm.", "ceo": {"first": "David", "last": "Solomon", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Denis", "last": "Coleman", "title": "Chief Financial Officer"}},
    {"name": "Morgan Stanley", "domain": "morganstanley.com", "industry": "Finance", "employee_count": 80000, "annual_revenue_b": 62, "founded_year": 1935, "headquarters": "New York, NY", "description": "Global financial services firm providing investment banking and wealth management.", "ceo": {"first": "Ted", "last": "Pick", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Sharon", "last": "Yeshaya", "title": "Chief Financial Officer"}},
    {"name": "Bank of America Corporation", "domain": "bankofamerica.com", "industry": "Finance", "employee_count": 213000, "annual_revenue_b": 102, "founded_year": 1998, "headquarters": "Charlotte, NC", "description": "Multinational financial services company providing banking and investing products.", "ceo": {"first": "Brian", "last": "Moynihan", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Alastair", "last": "Borthwick", "title": "Chief Financial Officer"}},
    {"name": "Visa Inc.", "domain": "visa.com", "industry": "Finance", "employee_count": 32000, "annual_revenue_b": 36, "founded_year": 1958, "headquarters": "San Francisco, CA", "description": "Global payments technology company operating the world's largest electronic payment network.", "ceo": {"first": "Ryan", "last": "McInerney", "title": "Chief Executive Officer"}, "exec2": {"first": "Chris", "last": "Suh", "title": "Chief Financial Officer"}},
    {"name": "Berkshire Hathaway Inc.", "domain": "berkshirehathaway.com", "industry": "Finance", "employee_count": 392000, "annual_revenue_b": 371, "founded_year": 1839, "headquarters": "Omaha, NE", "description": "Multinational conglomerate with subsidiaries in insurance, energy, transportation, and manufacturing.", "ceo": {"first": "Greg", "last": "Abel", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Marc", "last": "Hamburg", "title": "Chief Financial Officer"}},

    # ===== ENERGY (5) =====
    {"name": "Exxon Mobil Corporation", "domain": "exxonmobil.com", "industry": "Energy", "employee_count": 62000, "annual_revenue_b": 339, "founded_year": 1999, "headquarters": "Spring, TX", "description": "Multinational oil and gas corporation engaged in exploration, production, and refining.", "ceo": {"first": "Darren", "last": "Woods", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Kathryn", "last": "Mikells", "title": "Chief Financial Officer"}},
    {"name": "Chevron Corporation", "domain": "chevron.com", "industry": "Energy", "employee_count": 46000, "annual_revenue_b": 197, "founded_year": 1879, "headquarters": "San Ramon, CA", "description": "Integrated energy company operating across the oil, natural gas, and geothermal energy value chain.", "ceo": {"first": "Mike", "last": "Wirth", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Eimear", "last": "Bonner", "title": "Chief Financial Officer"}},
    {"name": "ConocoPhillips", "domain": "conocophillips.com", "industry": "Energy", "employee_count": 12000, "annual_revenue_b": 57, "founded_year": 2002, "headquarters": "Houston, TX", "description": "Independent exploration and production company for crude oil, natural gas, and LNG.", "ceo": {"first": "Ryan", "last": "Lance", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Andy", "last": "O'Brien", "title": "Chief Financial Officer"}},
    {"name": "NextEra Energy, Inc.", "domain": "nexteraenergy.com", "industry": "Energy", "employee_count": 17000, "annual_revenue_b": 26, "founded_year": 1925, "headquarters": "Juno Beach, FL", "description": "World's largest generator of renewable energy from wind and solar sources.", "ceo": {"first": "John", "last": "Ketchum", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Michael", "last": "Dunne", "title": "Chief Financial Officer"}},
    {"name": "Duke Energy Corporation", "domain": "duke-energy.com", "industry": "Energy", "employee_count": 27000, "annual_revenue_b": 30, "founded_year": 1904, "headquarters": "Charlotte, NC", "description": "Electric power and natural gas utility serving the southeastern and midwestern United States.", "ceo": {"first": "Harry", "last": "Sideris", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Brian", "last": "Savoy", "title": "Chief Financial Officer"}},

    # ===== RETAIL / CONSUMER (5) =====
    {"name": "Walmart Inc.", "domain": "walmart.com", "industry": "Retail", "employee_count": 2100000, "annual_revenue_b": 681, "founded_year": 1962, "headquarters": "Bentonville, AR", "description": "World's largest company by revenue, operating hypermarkets, discount stores, and grocery stores.", "ceo": {"first": "Doug", "last": "McMillon", "title": "President and Chief Executive Officer"}, "exec2": {"first": "John David", "last": "Rainey", "title": "Chief Financial Officer"}},
    {"name": "Amazon.com, Inc.", "domain": "amazon.com", "industry": "Retail", "employee_count": 1556000, "annual_revenue_b": 638, "founded_year": 1994, "headquarters": "Seattle, WA", "description": "E-commerce and cloud computing company operating the world's largest online marketplace and AWS.", "ceo": {"first": "Andy", "last": "Jassy", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Brian", "last": "Olsavsky", "title": "Chief Financial Officer"}},
    {"name": "Costco Wholesale Corporation", "domain": "costco.com", "industry": "Retail", "employee_count": 341000, "annual_revenue_b": 275, "founded_year": 1983, "headquarters": "Issaquah, WA", "description": "Membership-based warehouse club retailer offering bulk goods at discounted prices.", "ceo": {"first": "Ron", "last": "Vachris", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Gary", "last": "Millerchip", "title": "Chief Financial Officer"}},
    {"name": "The Home Depot, Inc.", "domain": "homedepot.com", "industry": "Retail", "employee_count": 521000, "annual_revenue_b": 160, "founded_year": 1978, "headquarters": "Atlanta, GA", "description": "World's largest home improvement retailer.", "ceo": {"first": "Ted", "last": "Decker", "title": "Chair, President, and Chief Executive Officer"}, "exec2": {"first": "Richard", "last": "McPhail", "title": "Chief Financial Officer"}},
    {"name": "The Procter & Gamble Company", "domain": "pg.com", "industry": "Retail", "employee_count": 109000, "annual_revenue_b": 84, "founded_year": 1837, "headquarters": "Cincinnati, OH", "description": "Multinational consumer goods corporation manufacturing household, health, and personal care products.", "ceo": {"first": "Jon", "last": "Moeller", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Andre", "last": "Schulten", "title": "Chief Financial Officer"}},

    # ===== INDUSTRIAL (5) =====
    {"name": "Lockheed Martin Corporation", "domain": "lockheedmartin.com", "industry": "Industrial", "employee_count": 122000, "annual_revenue_b": 71, "founded_year": 1995, "headquarters": "Bethesda, MD", "description": "Global aerospace, defense, and security company producing advanced aircraft and missile defense systems.", "ceo": {"first": "James", "last": "Taiclet", "title": "Chairman, President, and Chief Executive Officer"}, "exec2": {"first": "Evan", "last": "Scott", "title": "Chief Financial Officer"}},
    {"name": "Caterpillar Inc.", "domain": "caterpillar.com", "industry": "Industrial", "employee_count": 52000, "annual_revenue_b": 65, "founded_year": 1925, "headquarters": "Irving, TX", "description": "World's largest manufacturer of construction and mining equipment.", "ceo": {"first": "Joe", "last": "Creed", "title": "Chief Executive Officer"}, "exec2": {"first": "Andrew", "last": "Bonfield", "title": "Chief Financial Officer"}},
    {"name": "3M Company", "domain": "3m.com", "industry": "Industrial", "employee_count": 85000, "annual_revenue_b": 25, "founded_year": 1902, "headquarters": "Saint Paul, MN", "description": "Diversified industrial manufacturer producing adhesives, abrasives, and electronic materials.", "ceo": {"first": "William", "last": "Brown", "title": "Chairman and Chief Executive Officer"}, "exec2": {"first": "Anurag", "last": "Maheshwari", "title": "Chief Financial Officer"}},
    {"name": "FedEx Corporation", "domain": "fedex.com", "industry": "Industrial", "employee_count": 430000, "annual_revenue_b": 88, "founded_year": 1971, "headquarters": "Memphis, TN", "description": "Multinational transportation and logistics company providing express delivery and freight services.", "ceo": {"first": "Rajesh", "last": "Subramaniam", "title": "President and Chief Executive Officer"}, "exec2": {"first": "John", "last": "Dietrich", "title": "Chief Financial Officer"}},
    {"name": "The Boeing Company", "domain": "boeing.com", "industry": "Industrial", "employee_count": 156000, "annual_revenue_b": 89, "founded_year": 1916, "headquarters": "Arlington, VA", "description": "Aerospace manufacturer producing commercial jetliners, military aircraft, and space systems.", "ceo": {"first": "Kelly", "last": "Ortberg", "title": "President and Chief Executive Officer"}, "exec2": {"first": "Jay", "last": "Malave", "title": "Chief Financial Officer"}},
]

assert len(COMPANIES) == 50, f"Expected 50 companies, got {len(COMPANIES)}"


# ---------------------------------------------------------------------------
# Deal Data — 50 deals
# ---------------------------------------------------------------------------

DEALS = [
    # Nurture (22) — scenario 02
    {"name": "Apple - Enterprise License Agreement", "stage": "Nurture", "value": 75000, "close_date": "2026-02-15", "company_idx": 0, "champion": "Tim Cook", "use_case": "Enterprise platform deployment", "next_step": "Discovery call scheduled", "probability": 25, "contract_months": 24},
    {"name": "Microsoft - Cloud Migration Suite", "stage": "Nurture", "value": 120000, "close_date": "2026-04-01", "company_idx": 1, "champion": "CTO Office", "use_case": "Azure integration", "next_step": "Technical review", "probability": 20, "contract_months": 36},
    {"name": "UnitedHealth - Data Platform", "stage": "Nurture", "value": 45000, "close_date": "2026-01-30", "company_idx": 23, "champion": "VP Engineering", "use_case": "Claims analytics", "next_step": "Intro meeting", "probability": 15, "contract_months": 12},
    {"name": "JPMorgan - Risk Analytics", "stage": "Nurture", "value": 95000, "close_date": "2026-03-15", "company_idx": 29, "champion": "Head of Risk", "use_case": "Risk monitoring platform", "next_step": "Security questionnaire", "probability": 30, "contract_months": 24},
    {"name": "Lockheed Martin - IoT Sensors", "stage": "Nurture", "value": 32000, "close_date": "2026-05-01", "company_idx": 45, "champion": "VP Operations", "use_case": "Supply chain monitoring", "next_step": "RFP response", "probability": 10, "contract_months": 12},
    {"name": "Alphabet - AI Infrastructure", "stage": "Nurture", "value": 180000, "close_date": "2026-02-28", "company_idx": 2, "champion": "VP Infrastructure", "use_case": "ML pipeline tooling", "next_step": "POC scoping", "probability": 35, "contract_months": 36},
    {"name": "Intel - Analytics Tier", "stage": "Nurture", "value": 65000, "close_date": "2026-01-15", "company_idx": 10, "champion": "Data Science Lead", "use_case": "Chip design analytics", "next_step": "Demo scheduled", "probability": 25, "contract_months": 12},
    {"name": "Johnson & Johnson - Portal", "stage": "Nurture", "value": 52000, "close_date": "2026-06-01", "company_idx": 24, "champion": "IT Director", "use_case": "Research collaboration", "next_step": "Stakeholder intro", "probability": 15, "contract_months": 24},
    {"name": "NextEra Energy - Grid Monitor", "stage": "Nurture", "value": 28000, "close_date": "2026-02-20", "company_idx": 43, "champion": "Grid Operations", "use_case": "Renewable grid monitoring", "next_step": "Requirements gathering", "probability": 20, "contract_months": 12},
    {"name": "Walmart - POS Integration", "stage": "Nurture", "value": 41000, "close_date": "2026-07-01", "company_idx": 38, "champion": "VP Retail Tech", "use_case": "Checkout optimization", "next_step": "Vendor evaluation", "probability": 10, "contract_months": 12},
    {"name": "Goldman Sachs - Compliance", "stage": "Nurture", "value": 18000, "close_date": "2026-01-10", "company_idx": 30, "champion": "Compliance Officer", "use_case": "Regulatory reporting", "next_step": "Legal review", "probability": 30, "contract_months": 12},
    {"name": "Zebra Technologies - Starter Plan", "stage": "Nurture", "value": 15000, "close_date": "2026-08-01", "company_idx": 18, "champion": "Product Manager", "use_case": "Asset tracking pilot", "next_step": "Product demo", "probability": 20, "contract_months": 12},
    {"name": "Broadcom - Security Audit Tool", "stage": "Nurture", "value": 88000, "close_date": "2026-02-10", "company_idx": 5, "champion": "CISO", "use_case": "Network security assessment", "next_step": "Technical deep-dive", "probability": 35, "contract_months": 24},
    {"name": "Abbott - Lab Module", "stage": "Nurture", "value": 67000, "close_date": "2026-03-20", "company_idx": 28, "champion": "Lab Director", "use_case": "Diagnostics data pipeline", "next_step": "Site visit", "probability": 25, "contract_months": 24},
    {"name": "Morgan Stanley - Trading Platform", "stage": "Nurture", "value": 110000, "close_date": "2026-01-25", "company_idx": 31, "champion": "Head of Trading Tech", "use_case": "Algo trading infrastructure", "next_step": "Architecture review", "probability": 30, "contract_months": 36},
    {"name": "Caterpillar - QA Suite", "stage": "Nurture", "value": 37000, "close_date": "2026-04-15", "company_idx": 46, "champion": "QA Manager", "use_case": "Manufacturing QA automation", "next_step": "POC proposal", "probability": 20, "contract_months": 12},
    {"name": "Netflix - Content Platform", "stage": "Nurture", "value": 42000, "close_date": "2026-02-05", "company_idx": 13, "champion": "VP Engineering", "use_case": "Content delivery optimization", "next_step": "Technical assessment", "probability": 25, "contract_months": 12},
    {"name": "Duke Energy - Turbine Monitor", "stage": "Nurture", "value": 53000, "close_date": "2026-09-01", "company_idx": 44, "champion": "Plant Manager", "use_case": "Predictive maintenance", "next_step": "Site assessment", "probability": 15, "contract_months": 24},
    {"name": "Costco - Inventory System", "stage": "Nurture", "value": 29000, "close_date": "2026-01-20", "company_idx": 40, "champion": "VP Supply Chain", "use_case": "Warehouse optimization", "next_step": "Vendor comparison", "probability": 15, "contract_months": 12},
    {"name": "Adobe - CMS Integration", "stage": "Nurture", "value": 34000, "close_date": "2026-05-15", "company_idx": 12, "champion": "Product Lead", "use_case": "Experience platform extension", "next_step": "Integration review", "probability": 25, "contract_months": 12},
    {"name": "Visa - Payment Gateway", "stage": "Nurture", "value": 22000, "close_date": "2026-02-12", "company_idx": 33, "champion": "VP Payments", "use_case": "Real-time payment processing", "next_step": "Compliance check", "probability": 20, "contract_months": 12},
    {"name": "DXC Technology - Data Pipeline", "stage": "Nurture", "value": 156000, "close_date": "2026-06-15", "company_idx": 15, "champion": "CTO", "use_case": "Legacy modernization", "next_step": "SOW draft", "probability": 35, "contract_months": 36},

    # Qualified (8)
    {"name": "Qualcomm - Dev License", "stage": "Qualified", "value": 85000, "close_date": "2026-02-25", "company_idx": 11, "champion": "VP R&D", "use_case": "5G testing platform", "next_step": "Contract negotiation", "probability": 50, "contract_months": 24},
    {"name": "AMD - Starter Pack", "stage": "Qualified", "value": 12000, "close_date": "2026-03-10", "company_idx": 14, "champion": "Engineering Lead", "use_case": "GPU compute benchmarking", "next_step": "Trial deployment", "probability": 60, "contract_months": 12},
    {"name": "Bank of America - Trading Platform", "stage": "Qualified", "value": 250000, "close_date": "2026-01-05", "company_idx": 32, "champion": "CTO", "use_case": "High-frequency trading infra", "next_step": "Executive sponsor meeting", "probability": 45, "contract_months": 36},
    {"name": "Boeing - ERP Module", "stage": "Qualified", "value": 145000, "close_date": "2026-04-20", "company_idx": 49, "champion": "VP Manufacturing", "use_case": "Supply chain ERP", "next_step": "Procurement review", "probability": 40, "contract_months": 24},
    {"name": "Pfizer - Research Platform", "stage": "Qualified", "value": 38000, "close_date": "2026-02-18", "company_idx": 25, "champion": "Research Director", "use_case": "Clinical data management", "next_step": "Validation study", "probability": 55, "contract_months": 12},
    {"name": "ConocoPhillips - Dashboard", "stage": "Qualified", "value": 56000, "close_date": "2026-05-30", "company_idx": 42, "champion": "Operations Manager", "use_case": "Production monitoring", "next_step": "Pilot program", "probability": 50, "contract_months": 12},
    {"name": "CVS Health - Telehealth", "stage": "Qualified", "value": 92000, "close_date": "2026-01-28", "company_idx": 27, "champion": "VP Digital Health", "use_case": "Telehealth platform", "next_step": "Integration testing", "probability": 45, "contract_months": 24},
    {"name": "Chevron - Analytics Dashboard", "stage": "Qualified", "value": 47000, "close_date": "2026-03-05", "company_idx": 41, "champion": "Data Science Lead", "use_case": "Exploration analytics", "next_step": "Data pipeline review", "probability": 50, "contract_months": 12},

    # Proposal (6)
    {"name": "Home Depot - Inventory AI", "stage": "Proposal", "value": 175000, "close_date": "2026-02-08", "company_idx": 37, "champion": "VP Technology", "use_case": "Demand forecasting AI", "next_step": "Final pricing review", "probability": 65, "contract_months": 24},
    {"name": "Lumen Technologies - Platform", "stage": "Proposal", "value": 63000, "close_date": "2026-06-01", "company_idx": 19, "champion": "VP Product", "use_case": "Network automation", "next_step": "Legal redline", "probability": 60, "contract_months": 24},
    {"name": "Exxon Mobil - Supply Chain", "stage": "Proposal", "value": 98000, "close_date": "2025-12-15", "company_idx": 39, "champion": "Supply Chain VP", "use_case": "Logistics optimization", "next_step": "Executive approval", "probability": 70, "contract_months": 24},
    {"name": "3M - Quality Control", "stage": "Proposal", "value": 72000, "close_date": "2026-01-12", "company_idx": 47, "champion": "VP Manufacturing", "use_case": "Quality assurance automation", "next_step": "Procurement sign-off", "probability": 65, "contract_months": 12},
    {"name": "Seagate Technology - Render Farm", "stage": "Proposal", "value": 44000, "close_date": "2026-07-20", "company_idx": 20, "champion": "Engineering Manager", "use_case": "Storage performance testing", "next_step": "Benchmark validation", "probability": 55, "contract_months": 12},
    {"name": "Marvell Technology - ML Toolkit", "stage": "Proposal", "value": 81000, "close_date": "2026-02-22", "company_idx": 22, "champion": "ML Team Lead", "use_case": "Chip design ML pipeline", "next_step": "Technical sign-off", "probability": 70, "contract_months": 24},

    # Negotiation (4)
    {"name": "FedEx - Logistics Platform", "stage": "Negotiation", "value": 132000, "close_date": "2026-01-18", "company_idx": 48, "champion": "VP Operations", "use_case": "Route optimization engine", "next_step": "Contract redline", "probability": 75, "contract_months": 36},
    {"name": "Elevance Health - Claims System", "stage": "Negotiation", "value": 210000, "close_date": "2026-03-01", "company_idx": 26, "champion": "CTO", "use_case": "Claims processing automation", "next_step": "Final terms negotiation", "probability": 80, "contract_months": 36},
    {"name": "Amazon - API Infrastructure", "stage": "Negotiation", "value": 58000, "close_date": "2025-11-30", "company_idx": 39, "champion": "Principal Engineer", "use_case": "API gateway optimization", "next_step": "MSA execution", "probability": 85, "contract_months": 24},
    {"name": "P&G - Analytics Platform", "stage": "Negotiation", "value": 39000, "close_date": "2026-02-14", "company_idx": 36, "champion": "Brand Analytics Lead", "use_case": "Consumer insights platform", "next_step": "Payment terms", "probability": 80, "contract_months": 12},

    # Closed Won (6)
    {"name": "Meta - Developer Tools", "stage": "Closed Won", "value": 165000, "close_date": "2025-10-15", "company_idx": 3, "champion": "VP Developer Platform", "use_case": "Developer productivity tools", "next_step": "Onboarding kickoff", "probability": 100, "contract_months": 24},
    {"name": "NVIDIA - GPU Compute License", "stage": "Closed Won", "value": 78000, "close_date": "2025-09-01", "company_idx": 4, "champion": "VP Compute", "use_case": "AI training infrastructure", "next_step": "Deployment", "probability": 100, "contract_months": 12},
    {"name": "Cisco - Network Monitor", "stage": "Closed Won", "value": 54000, "close_date": "2025-11-20", "company_idx": 8, "champion": "Network Ops Director", "use_case": "Network observability", "next_step": "Integration complete", "probability": 100, "contract_months": 12},
    {"name": "Berkshire Hathaway - Enterprise Platform", "stage": "Closed Won", "value": 480000, "close_date": "2025-08-10", "company_idx": 34, "champion": "VP Technology", "use_case": "Cross-subsidiary data platform", "next_step": "Phase 2 planning", "probability": 100, "contract_months": 36},
    {"name": "Oracle - Cloud Integration", "stage": "Closed Won", "value": 33000, "close_date": "2025-12-05", "company_idx": 6, "champion": "Cloud Architect", "use_case": "Multi-cloud orchestration", "next_step": "Renewal discussion", "probability": 100, "contract_months": 12},
    {"name": "Salesforce - Platform Extension", "stage": "Closed Won", "value": 91000, "close_date": "2025-10-28", "company_idx": 7, "champion": "VP Platform", "use_case": "CRM workflow automation", "next_step": "Expansion opportunity", "probability": 100, "contract_months": 24},

    # Closed Lost (4)
    {"name": "IBM - Consulting Engagement", "stage": "Closed Lost", "value": 46000, "close_date": "2025-07-15", "company_idx": 9, "champion": "Engagement Manager", "use_case": "Consulting modernization", "next_step": "N/A", "probability": 0, "contract_months": 12, "loss_reason": "Competitor"},
    {"name": "Microchip Technology - Dev Tools", "stage": "Closed Lost", "value": 27000, "close_date": "2025-09-20", "company_idx": 21, "champion": "VP Engineering", "use_case": "Embedded dev toolchain", "next_step": "N/A", "probability": 0, "contract_months": 12, "loss_reason": "Price"},
    {"name": "Roper Technologies - SaaS Module", "stage": "Closed Lost", "value": 35000, "close_date": "2025-08-30", "company_idx": 16, "champion": "Product Director", "use_case": "Vertical SaaS integration", "next_step": "N/A", "probability": 0, "contract_months": 12, "loss_reason": "Timing"},
    {"name": "Agilent Technologies - Lab System", "stage": "Closed Lost", "value": 61000, "close_date": "2025-11-10", "company_idx": 17, "champion": "Lab Ops Manager", "use_case": "Lab automation system", "next_step": "N/A", "probability": 0, "contract_months": 24, "loss_reason": "Feature Gap"},
]

assert len(DEALS) == 50, f"Expected 50 deals, got {len(DEALS)}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def api_call(method, path, json_data=None, label=""):
    """Make an API call with rate limiting and error handling."""
    time.sleep(RATE_LIMIT_DELAY)
    try:
        if method == "GET":
            resp = client.get(path)
        elif method == "POST":
            resp = client.post(path, json=json_data)
        elif method == "PUT":
            resp = client.put(path, json=json_data)
        elif method == "PATCH":
            resp = client.patch(path, json=json_data)
        else:
            raise ValueError(f"Unknown method: {method}")

        if resp.status_code in (200, 201):
            return resp.json()
        elif resp.status_code == 409:
            # Conflict — attribute or record already exists
            return {"conflict": True, "status": 409, "detail": resp.text}
        else:
            print(f"  ERROR [{resp.status_code}] {label}: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  EXCEPTION {label}: {e}")
        return None


def validate_scenarios():
    """Check that seed data covers all 8 benchmark scenarios."""
    nurture = [d for d in DEALS if d["stage"] == "Nurture"]
    high_value = [d for d in DEALS if d["value"] > 50000]
    tech_name = [c for c in COMPANIES if "Tech" in c["name"]]
    tech_industry = [c for c in COMPANIES if c["industry"] == "Technology"]
    large_tech = [c for c in COMPANIES if c["industry"] == "Technology" and c["employee_count"] > 100]
    pre_march = [d for d in DEALS if d["close_date"] < "2026-03-01"]
    highest = max(DEALS, key=lambda d: d["value"])

    checks = [
        (len(COMPANIES) >= 25, f"01 List companies: {len(COMPANIES)} companies"),
        (len(nurture) >= 20, f"02 Nurture deals: {len(nurture)} deals"),
        (len(high_value) >= 10, f"03 Deals > $50K: {len(high_value)} deals"),
        (len(tech_name) >= 8, f"04 'Tech' in name: {len(tech_name)} companies"),
        (len(tech_industry) >= 10, f"05 Technology industry: {len(tech_industry)} companies"),
        (len(pre_march) >= 15, f"06 Before March 2026: {len(pre_march)} deals"),
        (len(large_tech) >= 5, f"07 Large Tech (compound): {len(large_tech)} companies"),
        (True, f"08 Highest deal: ${highest['value']:,} — {highest['name']}"),
    ]

    print("Scenario coverage:")
    for ok, msg in checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {msg}")
    print()
    return all(ok for ok, _ in checks)


# ---------------------------------------------------------------------------
# Phase 1: Create custom attributes
# ---------------------------------------------------------------------------

def create_custom_attributes():
    """Create custom attributes on companies and deals objects."""
    print("=" * 60)
    print("Phase 1: Creating custom attributes")
    print("=" * 60)

    # Companies
    print(f"\nCompanies ({len(COMPANY_CUSTOM_ATTRIBUTES)} attributes):")
    for attr in COMPANY_CUSTOM_ATTRIBUTES:
        payload = {
            "data": {
                "title": attr["title"],
                "api_slug": attr["api_slug"],
                "type": attr["type"],
                "description": attr.get("description", ""),
                "is_required": False,
                "is_unique": False,
                "is_multiselect": False,
            }
        }
        result = api_call("POST", "/objects/companies/attributes", payload, attr["title"])
        if result and not result.get("conflict"):
            print(f"  + {attr['title']} ({attr['type']})")
        elif result and result.get("conflict"):
            print(f"  ~ {attr['title']} (already exists)")
        else:
            print(f"  ! {attr['title']} (failed)")

    # Deals
    print(f"\nDeals ({len(DEAL_CUSTOM_ATTRIBUTES)} attributes):")
    for attr in DEAL_CUSTOM_ATTRIBUTES:
        payload = {
            "data": {
                "title": attr["title"],
                "api_slug": attr["api_slug"],
                "type": attr["type"],
                "description": attr.get("description", ""),
                "is_required": False,
                "is_unique": False,
                "is_multiselect": False,
            }
        }
        result = api_call("POST", "/objects/deals/attributes", payload, attr["title"])
        if result and not result.get("conflict"):
            print(f"  + {attr['title']} ({attr['type']})")
        elif result and result.get("conflict"):
            print(f"  ~ {attr['title']} (already exists)")
        else:
            print(f"  ! {attr['title']} (failed)")


# ---------------------------------------------------------------------------
# Phase 2: Create companies
# ---------------------------------------------------------------------------

def create_companies():
    """Create 50 companies using assert (upsert on domain)."""
    print("\n" + "=" * 60)
    print("Phase 2: Creating companies")
    print("=" * 60)

    company_records = []
    for i, c in enumerate(COMPANIES):
        values = {
            "name": [{"value": c["name"]}],
            "domains": [{"domain": c["domain"]}],
            "description": [{"value": c["description"]}],
        }

        # Custom attributes — Attio v2 requires typed array format
        if c.get("employee_count"):
            values["employee_count"] = [{"value": c["employee_count"]}]
        if c.get("annual_revenue_b"):
            values["annual_revenue"] = [{"currency_value": c["annual_revenue_b"] * 1_000_000_000, "currency_code": "USD"}]
        if c.get("founded_year"):
            values["founded_year"] = [{"value": c["founded_year"]}]
        if c.get("headquarters"):
            values["headquarters"] = [{"value": c["headquarters"]}]
        if c.get("industry"):
            values["industry"] = [{"option": {"title": c["industry"]}}]

        # Enrichment-style fields
        values["lead_source"] = [{"option": {"title": "Benchmark Seed"}}]
        values["account_tier"] = [{"option": {"title": "Enterprise" if c.get("employee_count", 0) > 50000 else "Mid-Market"}}]
        values["funding_stage"] = [{"option": {"title": "Public"}}]
        values["contract_status"] = [{"option": {"title": "Prospect"}}]
        values["icp_score"] = [{"value": min(100, max(10, c.get("employee_count", 100) // 1000 + 40))}]

        payload = {"data": {"values": values}}

        # Use assert (upsert) on domains for idempotency
        result = api_call(
            "PUT",
            "/objects/companies/records?matching_attribute=domains",
            payload,
            c["name"],
        )

        if result and "data" in result:
            record_id = result["data"]["id"]["record_id"]
            company_records.append({"record_id": record_id, "name": c["name"], "idx": i})
            print(f"  [{i+1:2d}/50] {c['name']} -> {record_id[:12]}...")
        else:
            company_records.append(None)
            print(f"  [{i+1:2d}/50] FAILED: {c['name']}")

    return company_records


# ---------------------------------------------------------------------------
# Phase 3: Create people (C-Suite contacts)
# ---------------------------------------------------------------------------

def create_people(company_records):
    """Create ~100 people (2 per company) using assert (upsert on email)."""
    print("\n" + "=" * 60)
    print("Phase 3: Creating people (C-Suite contacts)")
    print("=" * 60)

    people_created = 0
    for i, c in enumerate(COMPANIES):
        if company_records[i] is None:
            continue

        company_id = company_records[i]["record_id"]
        domain = c["domain"]

        for exec_data in [c["ceo"], c.get("exec2")]:
            if not exec_data:
                continue

            first = exec_data["first"]
            last = exec_data["last"]
            email = f"{first.lower().replace(' ', '')}.{last.lower().replace(' ', '')}@{domain}"

            values = {
                "name": [{"first_name": first, "last_name": last}],
                "email_addresses": [{"email_address": email}],
                "job_title": [{"value": exec_data["title"]}],
                "company": [{"target_object": "companies", "target_record_id": company_id}],
            }

            payload = {"data": {"values": values}}
            result = api_call(
                "PUT",
                "/objects/people/records?matching_attribute=email_addresses",
                payload,
                f"{first} {last}",
            )

            if result and "data" in result:
                people_created += 1
                if people_created <= 5 or people_created % 20 == 0:
                    print(f"  [{people_created:3d}] {first} {last} ({exec_data['title']}) @ {c['name']}")
            else:
                # Don't fail the whole script over contact creation errors
                pass

    print(f"\n  Total people created: {people_created}")
    return people_created


# ---------------------------------------------------------------------------
# Phase 4: Create deals
# ---------------------------------------------------------------------------

def create_deals(company_records):
    """Create 50 deals with associations to companies."""
    print("\n" + "=" * 60)
    print("Phase 4: Creating deals")
    print("=" * 60)

    deal_records = []
    for i, d in enumerate(DEALS):
        values = {
            "name": [{"value": d["name"]}],
        }

        # Deal value — built-in currency field
        if d.get("value"):
            values["value"] = [{"currency_value": d["value"], "currency_code": "USD"}]

        # Close date — custom date attribute
        if d.get("close_date"):
            values["close_date"] = [{"value": d["close_date"]}]

        # Associated company
        company_idx = d.get("company_idx")
        if company_idx is not None and company_records[company_idx]:
            values["associated_company"] = [{
                "target_object": "companies",
                "target_record_id": company_records[company_idx]["record_id"],
            }]

        # Custom deal attributes — Attio v2 typed array format
        if d.get("champion"):
            values["champion"] = [{"value": d["champion"]}]
        if d.get("use_case"):
            values["use_case"] = [{"value": d["use_case"]}]
        if d.get("next_step"):
            values["next_step"] = [{"value": d["next_step"]}]
        if d.get("probability") is not None:
            values["probability"] = [{"value": d["probability"]}]
        if d.get("contract_months"):
            values["contract_length_months"] = [{"value": d["contract_months"]}]
        if d.get("loss_reason"):
            values["loss_reason"] = [{"option": {"title": d["loss_reason"]}}]

        values["deal_lead_source"] = [{"option": {"title": "Benchmark Seed"}}]

        payload = {"data": {"values": values}}
        result = api_call("POST", "/objects/deals/records", payload, d["name"])

        if result and "data" in result:
            record_id = result["data"]["id"]["record_id"]
            deal_records.append({"record_id": record_id, "name": d["name"], "stage": d["stage"]})
            print(f"  [{i+1:2d}/50] {d['name']} (${d['value']:,}) -> {record_id[:12]}...")

            # Update stage — status fields require typed array format
            stage_payload = {"data": {"values": {"stage": [{"status": {"title": d["stage"]}}]}}}
            api_call("PATCH", f"/objects/deals/records/{record_id}", stage_payload, f"stage:{d['stage']}")
        else:
            deal_records.append(None)
            print(f"  [{i+1:2d}/50] FAILED: {d['name']}")

    return deal_records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 60)
    print("  ATTIO MCP BENCHMARK — WORKSPACE SEEDER")
    print("=" * 60)
    print()
    print("  50 companies (Fortune 100 + well-known)")
    print("  ~100 contacts (real C-Suite executives)")
    print("  50 deals (synthetic enterprise scenarios)")
    print("  25 custom attributes (realistic B2B CRM fields)")
    print()

    # Validate
    if not validate_scenarios():
        print("ERROR: Seed data does not cover all scenarios. Fix the data.")
        sys.exit(1)

    # Test API connection
    print("Testing API connection...")
    test = api_call("GET", "/self", label="whoami")
    if test is None:
        print("ERROR: Cannot connect to Attio API. Check your API key.")
        sys.exit(1)
    print(f"  Connected as workspace: {test.get('data', {}).get('workspace', {}).get('name', 'unknown')}")
    print()

    # Run phases
    create_custom_attributes()
    company_records = create_companies()
    create_people(company_records)
    deal_records = create_deals(company_records)

    # Save mapping
    output_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_path = os.path.join(output_dir, "..", "seed-record-mapping.json")
    mapping = {
        "companies": [r for r in company_records if r],
        "deals": [r for r in deal_records if r],
        "metadata": {
            "total_companies": sum(1 for r in company_records if r),
            "total_deals": sum(1 for r in deal_records if r),
            "total_company_custom_attrs": len(COMPANY_CUSTOM_ATTRIBUTES),
            "total_deal_custom_attrs": len(DEAL_CUSTOM_ATTRIBUTES),
            "script_version": "2.0",
            "data_source": "Fortune 100 + public company data",
        },
    }
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)

    # Summary
    created_companies = sum(1 for r in company_records if r)
    created_deals = sum(1 for r in deal_records if r)

    print()
    print("=" * 60)
    print("  SEED COMPLETE")
    print("=" * 60)
    print(f"  Companies:  {created_companies}/50")
    print(f"  Deals:      {created_deals}/50")
    print(f"  Custom attrs (companies): {len(COMPANY_CUSTOM_ATTRIBUTES)}")
    print(f"  Custom attrs (deals):     {len(DEAL_CUSTOM_ATTRIBUTES)}")
    print(f"  Record mapping: {mapping_path}")
    print()
    print("  Next steps:")
    print("    1. Connect Arcade, Composio, and Attio Official MCP servers")
    print("    2. Run the 3 benchmark prompts from CONTEXT_DUMP.md")
    print("    3. Run: python scripts/count_tokens.py")
    print()


if __name__ == "__main__":
    main()
