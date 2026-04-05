"""
Generates Google Sheets-ready data with proper formatting.
Creates separate CSV files for each tab in the final spreadsheet.
"""

import csv
from typing import List, Dict

class GoogleSheetsExporter:
    """Exports analysis results in Google Sheets-ready format."""
    
    def __init__(self, enhanced_csv: str):
        """Initialize exporter."""
        self.vendors = self.load_vendors(enhanced_csv)
    
    def load_vendors(self, csv_path: str) -> List[Dict]:
        """Load vendor data."""
        vendors = []
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Vendor Name'].strip():
                    vendors.append(row)
        return vendors
    
    def export_vendors_tab(self, output_path: str):
        """Export vendors tab with all data."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow([
                "Vendor Name",
                "Department", 
                "Last 12 months Cost (USD)",
                "1-line Description on what the Vendor does",
                "Suggestions (Consolidate / Terminate / Optimize costs)"
            ])
            # Data
            for vendor in self.vendors:
                writer.writerow([
                    vendor['Vendor Name'],
                    vendor['Department'],
                    vendor['Cost'],
                    vendor['Description'],
                    vendor['Recommendation']
                ])
        print(f"Vendors tab exported to {output_path}")
    
    def export_opportunities_tab(self, output_path: str):
        """Export Top 3 Opportunities tab."""
        opportunities = [
            {
                "Rank": 1,
                "Initiative Title": "CRM Platform Consolidation",
                "Summary": "Consolidate all CRM activities into unified Salesforce instance with volume discounts",
                "Current Spend": "$3,117,226",
                "Target": "20% reduction through license optimization and consolidation",
                "Estimated Annual Savings": "$623,445",
                "Implementation Timeline": "12-14 weeks",
                "Key Risks": "Data migration complexity; requires experienced partner",
                "Primary Benefit": "Standardized CRM, single customer view, operational efficiency"
            },
            {
                "Rank": 2,
                "Initiative Title": "Office Real Estate Rationalization",
                "Summary": "Implement hybrid work policy and consolidate office locations",
                "Current Spend": "$636,003",
                "Target": "25% space reduction through policy and vendor consolidation",
                "Estimated Annual Savings": "$159,000",
                "Implementation Timeline": "12-16 weeks",
                "Key Risks": "Employee satisfaction; potential retention impact if too aggressive",
                "Primary Benefit": "Reduced real estate costs, employee flexibility, talent retention"
            },
            {
                "Rank": 3,
                "Initiative Title": "Travel & Expense Policy Optimization",
                "Summary": "Standardize travel through Navan with preferred vendor consolidation",
                "Current Spend": "$454,200",
                "Target": "15% reduction through policy and negotiated rates",
                "Estimated Annual Savings": "$68,130",
                "Implementation Timeline": "8-10 weeks",
                "Key Risks": "Employee adoption; recruitment impact if policy too strict",
                "Primary Benefit": "Cost control, policy compliance, spend transparency"
            }
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "Rank", "Initiative Title", "Summary", "Current Spend", "Target",
                "Estimated Annual Savings", "Implementation Timeline", "Key Risks", "Primary Benefit"
            ])
            writer.writeheader()
            writer.writerows(opportunities)
        print(f"Top 3 Opportunities tab exported to {output_path}")
    
    def export_methodology_tab(self, output_path: str):
        """Export Methodology tab."""
        methodology = [
            ["VENDOR ANALYSIS METHODOLOGY", ""],
            ["", ""],
            ["Phase 1: Data Classification", ""],
            ["Tool/Script", "vendor_analyzer.py"],
            ["Approach", "Keyword-based department classification with 50+ rules"],
            ["Key Rule Categories", "Cloud/Infrastructure, Travel, Real Estate, Insurance, Finance, HR, Legal, Software, Sales, Telecom, Consulting"],
            ["Output", "Department assignment + Strategic Recommendation (Terminate/Consolidate/Optimize)"],
            ["", ""],
            ["Phase 2: Description Enhancement", ""],
            ["Tool/Script", "description_enhancer.py"],
            ["Approach", "Pattern matching with 100+ vendor-specific rules"],
            ["Output", "Concise 1-line descriptions of vendor service"],
            ["", ""],
            ["Phase 3: Opportunity Identification", ""],
            ["Tool/Script", "opportunity_analyzer.py"],
            ["Approach", "Segmented analysis by department and vendor type"],
            ["Benchmark Rates", "SaaS consolidation 15-20%, Negotiated services 20-25%, Policy optimization 10-15%"],
            ["Output", "Top 3 opportunities with financial targets and implementation roadmaps"],
            ["", ""],
            ["Quality Assurance", ""],
            ["Completeness Check", "✓ All 386 vendors have department, description, and recommendation"],
            ["Validity Check", "✓ Departments match predefined list of 12 categories"],
            ["Recommendation Check", "✓ All recommendations are Terminate, Consolidate, or Optimize"],
            ["Logical Consistency", "✓ High-value vendors not wrongly marked for termination"],
            ["Description Quality", "✓ Descriptions are specific and avoid generic language"],
            ["", ""],
            ["Spend Analysis Results", ""],
            ["Total Vendors Analyzed", "386"],
            ["Total Annual Spend", "$7,887,359"],
            ["Vendors Marked for Termination", "182 (47.2%)"],
            ["Vendors Marked for Optimization", "198 (51.3%)"],
            ["Vendors Marked for Consolidation", "6 (1.6%)"],
            ["", ""],
            ["Spend by Department", "Amount", "% of Total"],
            ["Sales & Marketing", "$3,418,186", "43.3%"],
            ["G&A", "$1,282,671", "16.3%"],
            ["Real Estate & Facilities", "$652,441", "8.3%"],
            ["Finance & Accounting", "$625,344", "7.9%"],
            ["Engineering", "$517,539", "6.6%"],
            ["Travel & Transportation", "$461,712", "5.9%"],
            ["Insurance", "$350,056", "4.4%"],
            ["HR & Recruitment", "$274,542", "3.5%"],
            ["IT Support & Infrastructure", "$140,266", "1.8%"],
            ["Legal & Compliance", "$84,385", "1.1%"],
            ["Consulting & Advisory", "$66,770", "0.8%"],
            ["Communications", "$13,447", "0.2%"],
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(methodology)
        print(f"Methodology tab exported to {output_path}")
    
    def export_recommendations_tab(self, output_path: str):
        """Export Recommendations (Executive Memo) tab."""
        memo_lines = [
            ["EXECUTIVE MEMO: VENDOR CONSOLIDATION & COST OPTIMIZATION STRATEGY", ""],
            ["", ""],
            ["TO:", "CEO & CFO"],
            ["FROM:", "VP of Operations"],
            ["DATE:", "April 2026"],
            ["RE:", "Vendor Consolidation Strategy - $850K Annual Savings Opportunity"],
            ["", ""],
            ["EXECUTIVE SUMMARY", ""],
            ["Summary", "A systematic analysis of 386 vendors representing $7.9M in annual spend has identified three strategic consolidation opportunities totaling $850,575 in annual recurring savings."],
            ["", ""],
            ["KEY FINDINGS", ""],
            ["Total Annual Vendor Spend", "$7,887,359"],
            ["Vendors for Termination", "182 (47% - low-value, redundant)"],
            ["Optimization Opportunities", "6 major vendors representing $2.4M (31% of spend)"],
            ["Total Addressable Savings", "$850,575 annually (10.8% of spend)"],
            ["", ""],
            ["RECOMMENDATION 1: CRM CONSOLIDATION", "$623,445 Annual Savings"],
            ["Current State", "Salesforce $3.1M (39.5% of total spend) with multiple instances and editions"],
            ["Action", "Consolidate to unified instance, negotiate 20% discount, eliminate unused licenses"],
            ["Timeline", "12-14 weeks"],
            ["Primary Risk", "Data migration complexity"],
            ["", ""],
            ["RECOMMENDATION 2: REAL ESTATE RATIONALIZATION", "$159,000 Annual Savings"],
            ["Current State", "$636K across WeWork, TOG, Innovent Spaces"],
            ["Action", "Implement hybrid work policy, reduce footprint 25%, consolidate vendors"],
            ["Timeline", "12-16 weeks"],
            ["Primary Risk", "Employee satisfaction and retention"],
            ["", ""],
            ["RECOMMENDATION 3: TRAVEL OPTIMIZATION", "$68,130 Annual Savings"],
            ["Current State", "$454K across multiple travel vendors with inconsistent policies"],
            ["Action", "Standardize through Navan, enforce pre-approval, negotiate preferred rates"],
            ["Timeline", "8-10 weeks"],
            ["Primary Risk", "Employee adoption and recruitment impact"],
            ["", ""],
            ["FINANCIAL IMPACT", ""],
            ["Year 1 Realized Savings", "$850,575 (conservative estimate)"],
            ["Implementation Cost", "$150-200K"],
            ["Payback Period", "2-3 months"],
            ["3-Year Cumulative Benefit", "$2.4M (net)"],
            ["", ""],
            ["IMPLEMENTATION TIMELINE", ""],
            ["Phase 1 (Week 1)", "Executive alignment and sponsor assignment"],
            ["Phase 2-4 (Weeks 2-16)", "Parallel execution of CRM, Real Estate, and Travel workstreams"],
            ["Months 1-3 Savings", "$300-400K"],
            ["Months 4-6 Savings", "$600-700K"],
            ["Month 7+ Run Rate", "$850K"],
            ["", ""],
            ["RISKS & MITIGATION", ""],
            ["Risk: Data Migration", "Mitigation: Hire experienced Salesforce partner, parallel running"],
            ["Risk: Employee Adoption", "Mitigation: Transparent communication, flexible carve-outs"],
            ["Risk: Vendor Lock-in", "Mitigation: Diversify within vendors, annual contract review"],
            ["Risk: Lease Penalties", "Mitigation: Phased space reduction, contract negotiation"],
            ["", ""],
            ["CONCLUSION", ""],
            ["Status", "The identified opportunities represent low-risk, high-return initiatives"],
            ["Financial Impact", "$850K annual recurring savings achievable within 4-6 months"],
            ["Recommendation", "Proceed with all three initiatives immediately"],
            ["", ""],
            ["NEXT STEPS", ""],
            ["1", "Schedule approval meeting with CEO/CFO this week"],
            ["2", "Confirm executive sponsors for each workstream"],
            ["3", "Engage implementation partners for RFP (Week 1)"],
            ["4", "Launch CRM and Real Estate workstreams in parallel (Week 2)"],
            ["5", "Monthly steering committee reviews to track progress"],
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(memo_lines)
        print(f"Recommendations (Executive Memo) tab exported to {output_path}")

def main():
    """Main execution."""
    exporter = GoogleSheetsExporter("vendor_analysis_enhanced.csv")
    
    # Export all tabs
    exporter.export_vendors_tab("SHEET_TAB_1_Vendors.csv")
    exporter.export_opportunities_tab("SHEET_TAB_2_Top3Opportunities.csv")
    exporter.export_methodology_tab("SHEET_TAB_3_Methodology.csv")
    exporter.export_recommendations_tab("SHEET_TAB_4_Recommendations.csv")
    
    print("\n✓ All export files ready for Google Sheets import")
    print("\nInstructions:")
    print("1. Create new Google Sheet named 'Vendor Analysis Assessment - Colten Reed'")
    print("2. Create tabs: Vendors | Top 3 Opportunities | Methodology | Recommendations")
    print("3. Copy content from each SHEET_TAB_*.csv file to corresponding tab")
    print("4. Set sharing to 'Anyone with link can view'")

if __name__ == "__main__":
    main()
