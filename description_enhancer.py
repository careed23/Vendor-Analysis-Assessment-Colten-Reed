"""
Enhanced Vendor Description Generator
Uses pattern matching to generate specific 1-line descriptions for all vendors.
"""

import csv
import re
from typing import Dict, List

class DescriptionEnhancer:
    """Enhances vendor descriptions with specific details."""
    
    DESCRIPTION_RULES = {
        # Cloud & Infrastructure
        r"(amazon|aws)": "Cloud infrastructure and compute services provider",
        r"(google|gcp)": "Cloud platforms and enterprise tools provider",
        r"(azure|microsoft)": "Enterprise software and cloud services provider",
        r"salesforce": "Cloud-based CRM and customer engagement platform",
        r"cloudcross": "Cloud infrastructure and IT consulting services",
        
        # Travel & Expense
        r"(navan|tripactions)": "Corporate travel management and expense reporting",
        r"(uber|lyft)": "Ride-sharing and logistics services",
        r"(fedex|dhl|parcelforce)": "Shipping and parcel delivery services",
        r"(airline|airways|airlines)": "Air transportation services",
        
        # Real Estate
        r"(wework|coworking)": "Flexible office space and coworking solutions",
        r"tog uk": "UK office real estate and property management",
        r"(property|properties|space)": "Office real estate and property services",
        r"innovent": "Flexible office space solutions",
        r"(jll|jones lang|cbre)": "Commercial real estate advisory services",
        r"(hotel|resort|inn|guest)": "Accommodation and hospitality services",
        r"weking": "Office workspace provider",
        r"gpt space": "Office space and real estate solutions",
        r"(real estate|realty)": "Real estate and property management",
        
        # Insurance & Benefits
        r"(aetna|cigna|bupa|allianz|lloyds)": "Health and employee benefits insurance",
        r"(workers comp|workers' comp|icare|nsw)": "Workers compensation insurance",
        r"(mercer|benefit|systems)": "Employee benefits consulting and administration",
        r"(jensten|insurance broker)": "Insurance brokerage and advisory services",
        
        # Accounting & Finance
        r"(bdo|grant thornton|pwc|pricewaterhousecoopers|deloitte|crowe)": "Audit, tax, and advisory services",
        r"(sage|xero|quickbooks)": "Accounting and financial management software",
        r"(planful|anaplan)": "Financial planning and budgeting software",
        r"(ariba|netsuite)": "Procurement and ERP financial systems",
        r"(payroll|ato|australian taxation)": "Payroll processing and tax services",
        r"(rsm|eurofast)": "Audit and financial advisory services",
        r"(chartered|accountant|accounting)": "Accounting and financial services",
        r"ss&c": "Financial software and services provider",
        
        # HR & Recruitment
        r"(hr solution|workday)": "Human resources and employee management platform",
        r"(linkedin|recruitment)": "Recruitment and talent acquisition services",
        r"(peakon|engagement)": "Employee engagement and survey platform",
        r"(pluralsight|coursera|udemy|training)": "Employee training and development platform",
        r"(accutrainee|technet it)": "Technical recruitment and staffing services",
        r"(cedar recruitment|mason frank)": "Recruitment and staffing services",
        
        # Legal Services
        r"bisley": "Corporate law and legal advisory services",
        r"(pinsent|masons)": "International law firm and legal advisory",
        r"quadrant": "Business law and legal advisory",
        r"curzon": "Legal advisory and solicitor services",
        r"(law|solicitor|lawyer|legal|attorney|advocate)": "Legal consulting and corporate law services",
        r"(indu|houlihan)": "Legal and corporate advisory services",
        
        # Software & Development
        r"(slack)": "Team messaging and collaboration platform",
        r"(figma)": "Design and collaboration platform",
        r"(adobe)": "Creative software and digital tools suite",
        r"(trello)": "Project management and team collaboration",
        r"(asana|jira|confluence)": "Project management and collaboration software",
        r"(jetbrains|ide)": "Developer IDE and programming tools",
        r"(npm|github|gitlab)": "Software development and code management",
        r"(docusign)": "Digital signature and document management",
        r"(lastpass|password)": "Password management and cybersecurity",
        r"(zapier|workato)": "Workflow automation and integration platform",
        r"(splunk|monitoring|datadog)": "Application monitoring and observability",
        r"(smartsheet|monday|asana)": "Work execution and project planning",
        r"(aha)": "Product roadmap and release planning",
        r"(atlassian)": "Software development and team tools",
        r"ag grid": "Data grid component library",
        r"(information|infodata)": "Information management and services",
        
        # Marketing & Sales
        r"(hubspot|crm)": "CRM and marketing automation platform",
        r"(semrush|seo)": "SEO and digital marketing analytics",
        r"(cognism|lead|sales)": "Sales intelligence and lead database",
        r"(outreach)": "Sales engagement and automation platform",
        r"(uberflip|content)": "Content marketing and experience platform",
        r"(mightyhive|google ads)": "Digital advertising management",
        r"(cision|pr newswire)": "Public relations and media monitoring",
        r"(lusha|6sense)": "B2B sales intelligence platform",
        
        # Telecom & IT Infrastructure
        r"telefonica": "Telecommunications and network services",
        r"(vodafone|t-mobile|brit telecom|telemach|telekom)": "Mobile telecommunications services",
        r"intertrust": "Corporate IT infrastructure services",
        
        # Consulting & Advisory
        r"(4i advisory|4i management)": "Management consulting and advisory services",
        r"(houlihan|vector capital)": "Corporate financial advisory services",
        r"westbrook": "Investment and advisory services",
        r"(advisor|consulting|consultant)": "Business consulting and advisory services",
        
        # Office & Workspace
        r"(godaddy|domain)": "Domain registration and web hosting",
        r"(amazon.co|supplies|office)": "Office supplies and equipment",
        r"(postbox)": "Mailbox and office services",
        
        # Catering & Hospitality
        r"(catering|pret|restaurant|cafe|food|kitchen|dining)": "Catering and food services",
        r"(sodexo|dining)": "Catering and hospitality management services",
        
        # Media & Communications
        r"(guardian|news|media|press)": "Media and news publishing",
        
        # Other Services
        r"(dun & bradstreet)": "Business credit and data analytics",
        r"(dunsimple|dns)": "Domain and DNS management services",
        r"(zonar|fitness|gym)": "Health and wellness services",
    }
    
    def enhance_descriptions(self, input_csv: str, output_csv: str):
        """Enhance descriptions for all vendors."""
        vendors = []
        
        with open(input_csv, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Vendor Name'].strip():
                    vendors.append(row)
        
        print(f"Processing {len(vendors)} vendors...")
        
        for vendor in vendors:
            name = vendor['Vendor Name'].strip()
            current_desc = vendor['Description'].strip()
            
            # Skip if already has good description
            if current_desc and len(current_desc) > 50 and "specialized services" not in current_desc:
                continue
            
            # Generate new description based on name patterns
            new_desc = self.generate_description(name)
            vendor['Description'] = new_desc
        
        # Write enhanced results
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(vendors[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(vendors)
        
        print(f"Enhanced descriptions saved to {output_csv}")
    
    def generate_description(self, vendor_name: str) -> str:
        """Generate specific description for vendor."""
        name_lower = vendor_name.lower()
        
        # Try to match against known patterns
        for pattern, description in self.DESCRIPTION_RULES.items():
            if re.search(pattern, name_lower):
                return description
        
        # Smart fallback based on name analysis
        if "insurance" in name_lower or "aetna" in name_lower or "cigna" in name_lower:
            return "Insurance and employee benefits provider"
        elif "law" in name_lower or "solicitor" in name_lower or "llp" in name_lower:
            return "Legal advisory and corporate law services"
        elif "hotel" in name_lower or "resort" in name_lower:
            return "Hotel and accommodation services"
        elif "restaurant" in name_lower or "cafe" in name_lower or "kitchen" in name_lower:
            return "Food service and catering"
        elif "d.o.o" in name_lower or "j.d.o.o" in name_lower or "obrt" in name_lower:
            return "Local service provider"
        elif "inc" in name_lower or "llc" in name_lower or "ltd" in name_lower:
            return "Business services provider"
        else:
            # Try to extract category from name
            words = vendor_name.split()
            if len(words) > 1:
                return f"{vendor_name} services and solutions"
            return f"{vendor_name} provider"

def main():
    """Main execution."""
    enhancer = DescriptionEnhancer()
    enhancer.enhance_descriptions(
        "vendor_analysis_output.csv",
        "vendor_analysis_enhanced.csv"
    )

if __name__ == "__main__":
    main()
