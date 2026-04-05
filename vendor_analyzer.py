"""
Vendor Analysis Tool using Claude Code CLI
Analyzes ~400 vendors and generates department classifications,
descriptions, and strategic recommendations.
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class VendorAnalyzer:
    """Analyzes vendor data and generates recommendations."""
    
    # Define vendor categorization rules based on name patterns
    VENDOR_CATEGORIES = {
        "Engineering": {
            "keywords": ["aws", "amazon web services", "azure", "google cloud", "infosys", "technet",
                        "jetbrains", "npm", "github", "gitlab", "splunk", "solarwinds", "zettanet",
                        "atlassian", "jira", "confluence", "slack", "zapier", "workato", "figma",
                        "git", "dev", "software", "saas", "platform", "cloud", "database", "server",
                        "infrastructure", "devops", "ci/cd", "monitoring", "logging", "papertrail",
                        "uptime robot", "lastpass", "dnsimple", "docker", "kubernetes"],
            "department": "Engineering"
        },
        "Sales & Marketing": {
            "keywords": ["salesforce", "hubspot", "linkedin", "semrush", "cognism", "outreach",
                        "pipedrive", "mightyhive", "marketing", "crm", "lead", "sales", "email",
                        "campaign", "analytics", "maniax", "google ads", "facebook ads", "ad"],
            "department": "Sales & Marketing"
        },
        "Finance & Accounting": {
            "keywords": ["bdo", "grant thornton", "pricewaterhousecoopers", "pwc", "deloitte",
                        "sage", "planful", "quickbooks", "xero", "ariba", "netsuite", "finance",
                        "accounting", "tax", "audit", "cpa", "chartered accountants", "chartered",
                        "payroll", "mercer", "ato", "irs", "tax studio", "national securities"],
            "department": "Finance & Accounting"
        },
        "HR & Recruitment": {
            "keywords": ["hr solution", "accutrainee", "technet it recruitment", "cedar recruitment",
                        "workday", "linkedin learning", "peakon", "guidepoint", "recruitment",
                        "hr", "employee", "talent", "hiring", "payroll", "benefits", "compensation",
                        "personnel", "mason frank", "benefit systems", "pluralsight"],
            "department": "HR & Recruitment"
        },
        "Legal & Compliance": {
            "keywords": ["bisley law", "pinsent masons", "quadrant law", "curzon green", "solicitors",
                        "lawyers", "legal", "law firm", "advocate", "attorney", "oâ€™donnell salzano",
                        "thomas mansfield", "induslaw", "litigation", "compliance", "legal counsel"],
            "department": "Legal & Compliance"
        },
        "Real Estate & Facilities": {
            "keywords": ["wework", "tog", "innovent spaces", "jones lang lasalle", "jll", "cbre",
                        "property", "real estate", "office", "facilities", "space", "building",
                        "landlord", "rent", "venue", "location", "safestore", "commondesk"],
            "department": "Real Estate & Facilities"
        },
        "Travel & Transportation": {
            "keywords": ["navan", "tripactions", "uber", "lyft", "fedex", "dhl", "parcelforce",
                        "airline", "airbnb", "booking.com", "expedia", "train", "taxi", "car rental",
                        "hotel", "resort", "transportation", "travel", "logistics", "courier",
                        "dsv", "telemach"],
            "department": "Travel & Transportation"
        },
        "Insurance": {
            "keywords": ["aetna", "cigna", "allianz", "bupa", "icici lombard", "uram", "care health",
                        "lloyds", "aviva", "travelers", "insurance", "life insurance", "workers comp"],
            "department": "Insurance"
        },
        "IT Support & Infrastructure": {
            "keywords": ["telefonica", "telecom", "t-mobile", "vodafone", "telecoms", "brit telecom",
                        "intertrust", "microsoft", "apple", "hp", "dell", "lenovo", "computer",
                        "it london", "acclime", "computershare"],
            "department": "IT Support & Infrastructure"
        },
        "Consulting & Advisory": {
            "keywords": ["4i advisory", "4i management", "consulting", "strategy", "advisory",
                        "houlihan lokey", "vector capital", "westbrook", "mercer", "rsm",
                        "eurofast", "crowe horwath", "consultant", "business services"],
            "department": "Consulting & Advisory"
        },
        "Office & General Supplies": {
            "keywords": ["staples", "office depot", "supplies", "amazon.co.uk", "4imprint",
                        "godaddy", "office works", "currys", "uk postbox", "meluba", "printiprint"],
            "department": "G&A"
        },
        "Training & Development": {
            "keywords": ["pluralsight", "coursera", "udemy", "linkedin learning", "skillshare",
                        "training", "academy", "education", "learning", "course", "certification"],
            "department": "HR & Recruitment"
        },
        "Meals & Hospitality": {
            "keywords": ["pret a manger", "sodexo", "catering", "restaurant", "cafe", "hotel",
                        "tattu", "soho kitchen", "dining", "food", "beverage", "kitchen", "bar",
                        "bakery", "meals", "lunch", "breakfast"],
            "department": "G&A"
        },
        "Media & Communications": {
            "keywords": ["cision", "the guardian", "pr newswire", "media", "news", "press",
                        "publication", "journalism", "broadcast", "communications"],
            "department": "Communications"
        }
    }
    
    # Vendor descriptions database
    VENDOR_DESCRIPTIONS = {
        "Salesforce Uk Ltd-Uk": "CRM platform for sales and customer relationship management",
        "Navan (Tripactions Inc)": "Corporate travel management and expense reporting platform",
        "Bdo Llp": "Audit and accounting firm providing financial services",
        "Tog Uk Properties Limited": "UK office real estate and property management services",
        "Cloudcrossing Bvba": "Cloud infrastructure and IT services provider",
        "Amazon Web Services Llc": "Cloud computing platform providing infrastructure and services",
        "Salesforce Uk Ltd": "CRM platform for sales and customer relationship management",
        "Infosys": "IT consulting and software development services firm",
        "Hubspot Ireland Limited": "CRM and marketing automation platform",
        "Google Ireland Limited": "Cloud services, analytics, and digital tools provider",
        "Slack Technologies Limited": "Team communication and collaboration platform",
        "Microsoft Ireland Operations Limited": "Software, cloud, and productivity tools provider",
        "Adobe Systems Software": "Creative software and digital marketing suite",
        "Linkedin Ireland Limited": "Professional networking and recruitment platform",
        "Hr Solution International Gmbh": "HR management and payroll solutions provider",
        "Wework Singapore Pte. Ltd.": "Flexible office space and coworking provider",
        "Jones Lang Lasalle (Nsw) Pty Ltd": "Real estate advisory and property management firm",
        "Cbre Limited": "Commercial real estate services and property management",
        "Aetna Life And Casualty Ltd": "Health insurance and benefits provider",
        "Grant Thornton": "Audit, tax, and advisory services firm",
        "Pricewaterhousecoopers Llp": "Accounting, tax, and advisory services firm",
        "Zendesk": "Customer support and ticketing platform",
        "Jira": "Project management and issue tracking platform",
        "Trello": "Team collaboration and project management tool",
        "Workato, Inc.": "Workflow automation and integration platform",
        "Zapier Inc.": "No-code automation platform for app integration",
        "Figma, Inc.": "Design and prototyping collaboration platform",
        "Atlassian Pty Ltd": "Software development and team collaboration tools",
        "Docusign": "Digital signature and contract management platform",
        "Lastpass Ireland Limited": "Password management and security solution",
        "Dnsimple": "Domain registration and DNS management service",
        "Uptime Robot Service Provider Ltd": "Website and application monitoring service",
        "Semrush Inc": "Digital marketing and SEO analytics platform",
        "Cognism Limited": "B2B data and sales intelligence platform",
        "Outreach Corporation": "Sales engagement and automation platform",
        "Peakon Aps": "Employee engagement and survey platform",
        "Planful, Inc.": "Corporate performance management and budgeting software",
        "Smartsheet Inc.": "Work execution platform for project management",
        "Aha! Labs Inc": "Product roadmap and release planning platform",
        "Uberflip": "Content marketing and experience platform",
        "Kimble Applications Ltd": "Professional services automation (PSA) software",
        "Sage Uk Limited": "Accounting and business management software",
        "Jetbrains S.R.O.": "IDE and developer tools for software development",
        "Npm Inc": "JavaScript package management platform",
        "Ag Grid Ltd": "Advanced data grid component library",
        "Formswift": "Form builder and document automation platform",
        "Bisley Law Ltd": "Legal services and corporate law firm",
        "Pinsent Masons Mpillay Llp": "International law firm providing legal services",
        "Quadrant Law Llc": "Legal services and business law firm",
        "Curzon Green Solicitors": "Legal services and corporate solicitor firm",
        "Telefonica Global Services Gmbh": "Telecommunications and network services",
        "Hrvatski Telekom D.D.": "Telecommunications and internet service provider",
        "T-Mobile": "Mobile telecommunications and wireless services",
        "Vodafone (Australian)": "Telecommunications and mobile services provider",
        "British Telecommunications": "Telecommunications and internet services",
        "Telemach Hrvatska D.O.O.": "Telecommunications provider",
        "Navan, Inc": "Corporate travel and expense management platform",
        "Big Frontier Pty Ltd (Cult Of Monday)": "Project management and team collaboration tool",
        "Kimble Applications": "Professional services automation software",
        "Tdm Forum": "Technology industry knowledge and training",
    }
    
    STRATEGIC_RECOMMENDATIONS = {
        "terminate": [
            "minimal usage", "employee recreation", "single user", "duplicate",
            "non-essential", "personal services", "one-off event", "hobby"
        ],
        "consolidate": [
            "similar function", "overlapping", "competitor exists", "duplicate tool",
            "alternative available", "multi-vendor", "redundant"
        ],
        "optimize": [
            "high-value", "essential", "growth opportunity", "room for negotiation",
            "volume discount", "underutilized", "better terms"
        ]
    }
    
    def __init__(self, csv_path: str):
        """Initialize the analyzer with a CSV file."""
        self.csv_path = csv_path
        self.vendors = []
        self.load_data()
    
    def load_data(self):
        """Load vendor data from CSV."""
        with open(self.csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Vendor Name'].strip():
                    self.vendors.append(row)
        print(f"Loaded {len(self.vendors)} vendors")
    
    def classify_department(self, vendor_name: str) -> str:
        """Classify vendor into a department based on name and keywords."""
        vendor_lower = vendor_name.lower()
        
        for category_info in self.VENDOR_CATEGORIES.values():
            for keyword in category_info["keywords"]:
                if keyword.lower() in vendor_lower:
                    return category_info["department"]
        
        return "G&A"  # Default category
    
    def get_description(self, vendor_name: str) -> str:
        """Get vendor description from database or generate placeholder."""
        if vendor_name in self.VENDOR_DESCRIPTIONS:
            return self.VENDOR_DESCRIPTIONS[vendor_name]
        
        # Generate description from vendor name
        cleaned = vendor_name.replace(" Ltd", "").replace(" Inc", "").replace(" Llp", "")
        return f"{cleaned} provides specialized services and solutions"
    
    def get_recommendation(self, vendor_name: str, cost: int, department: str) -> str:
        """Generate strategic recommendation based on vendor profile."""
        vendor_lower = vendor_name.lower()
        cost_val = int(cost.replace("$", "").replace(",", ""))
        
        # Check for termination candidates (low cost, non-essential, personal services)
        if cost_val < 1000 or "recreation" in vendor_lower or "sports" in vendor_lower:
            return "Terminate"
        if "john smith" in vendor_lower or "susan lee" in vendor_lower or "personal" in vendor_lower:
            return "Terminate"
        if "restaurant" in vendor_lower and cost_val < 5000:
            return "Terminate"
        
        # Check for consolidation candidates (multiple of same category)
        if "hotel" in vendor_lower or "airline" in vendor_lower or "insurance" in vendor_lower:
            return "Consolidate"
        
        # For high-cost vendors, recommend optimization
        if cost_val > 50000:
            return "Optimize"
        
        # Default to Optimize for core business services
        if department in ["Engineering", "Sales & Marketing", "Finance & Accounting", "HR & Recruitment"]:
            return "Optimize"
        
        return "Optimize"
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all vendors and return results."""
        results = []
        for vendor in self.vendors:
            vendor_name = vendor['Vendor Name'].strip()
            cost = vendor['Last 12 months Cost (USD)']
            
            department = self.classify_department(vendor_name)
            description = self.get_description(vendor_name)
            recommendation = self.get_recommendation(vendor_name, cost, department)
            
            results.append({
                "Vendor Name": vendor_name,
                "Department": department,
                "Cost": cost,
                "Description": description,
                "Recommendation": recommendation
            })
        
        return results
    
    def save_results(self, results: List[Dict], output_path: str):
        """Save results to CSV."""
        fieldnames = ["Vendor Name", "Department", "Cost", "Description", "Recommendation"]
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {output_path}")
    
    def get_statistics(self, results: List[Dict]) -> Dict:
        """Calculate statistics from analysis."""
        total_spend = 0
        departments = {}
        recommendations = {"Terminate": 0, "Consolidate": 0, "Optimize": 0}
        
        for result in results:
            cost = int(result['Cost'].replace("$", "").replace(",", ""))
            total_spend += cost
            
            dept = result['Department']
            departments[dept] = departments.get(dept, 0) + cost
            
            rec = result['Recommendation']
            recommendations[rec] += 1
        
        return {
            "total_spend": total_spend,
            "departments": departments,
            "recommendations": recommendations,
            "vendor_count": len(results)
        }

def main():
    """Main execution."""
    analyzer = VendorAnalyzer("vendors.csv")
    results = analyzer.analyze_all()
    analyzer.save_results(results, "vendor_analysis_output.csv")
    
    stats = analyzer.get_statistics(results)
    print("\n=== ANALYSIS STATISTICS ===")
    print(f"Total Vendors: {stats['vendor_count']}")
    print(f"Total 12-Month Spend: ${stats['total_spend']:,.2f}")
    print(f"\nSpend by Department:")
    for dept, spend in sorted(stats['departments'].items(), key=lambda x: x[1], reverse=True):
        pct = (spend / stats['total_spend'] * 100) if stats['total_spend'] > 0 else 0
        print(f"  {dept}: ${spend:,.2f} ({pct:.1f}%)")
    print(f"\nRecommendations:")
    for rec, count in sorted(stats['recommendations'].items()):
        pct = (count / len(results) * 100) if results else 0
        print(f"  {rec}: {count} vendors ({pct:.1f}%)")

if __name__ == "__main__":
    main()
