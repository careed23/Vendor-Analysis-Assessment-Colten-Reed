"""
Top Opportunities and Quality Check Analysis
Identifies the 3 highest-impact recommendations and validates the analysis.
"""

import csv
from typing import List, Dict, Tuple
import re

class OpportunityAnalyzer:
    """Identifies high-impact cost-saving opportunities."""
    
    def __init__(self, results_csv: str):
        """Initialize with results from vendor analysis."""
        self.results = self.load_results(results_csv)
    
    def load_results(self, csv_path: str) -> List[Dict]:
        """Load vendor analysis results."""
        results = []
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Vendor Name'].strip():
                    results.append(row)
        return results
    
    def parse_cost(self, cost_str: str) -> int:
        """Parse cost string to integer."""
        return int(cost_str.replace("$", "").replace(",", ""))
    
    def identify_termination_savings(self) -> Tuple[str, str, int]:
        """Identify savings from terminating low-value vendors."""
        termination_candidates = [
            v for v in self.results 
            if v['Recommendation'] == 'Terminate'
        ]
        
        total_savings = sum(self.parse_cost(v['Cost']) for v in termination_candidates)
        count = len(termination_candidates)
        
        title = "Eliminate Non-Essential Vendors"
        explanation = f"Terminate {count} low-value vendors including single-person services, " \
                     f"recreation clubs, and redundant one-off expenses. These vendors are " \
                     f"below $5K annual spend and offer minimal strategic value."
        
        return title, explanation, total_savings
    
    def identify_salesforce_optimization(self) -> Tuple[str, str, int]:
        """Identify Salesforce consolidation opportunity."""
        salesforce = [v for v in self.results if 'salesforce' in v['Vendor Name'].lower()]
        
        total_cost = sum(self.parse_cost(v['Cost']) for v in salesforce)
        potential_savings = int(total_cost * 0.20)  # 20% reduction through better negotiation
        
        title = "CRM Platform Consolidation"
        explanation = f"Consolidate CRM vendors (Salesforce: ${total_cost:,.0f}). Negotiate " \
                     f"volume discounts and remove unused editions. Implement a single Salesforce " \
                     f"instance with unified licensing."
        
        return title, explanation, potential_savings
    
    def identify_office_space_optimization(self) -> Tuple[str, str, int]:
        """Identify office space consolidation opportunity."""
        office_vendors = [
            v for v in self.results 
            if any(kw in v['Vendor Name'].lower() for kw in 
                   ['wework', 'property', 'office', 'space', 'tog', 'innovent', 'cbre', 'jll'])
        ]
        
        total_cost = sum(self.parse_cost(v['Cost']) for v in office_vendors)
        potential_savings = int(total_cost * 0.25)  # 25% reduction through space rationalization
        
        title = "Office Real Estate Rationalization"
        explanation = f"Consolidate office locations and renegotiate real estate contracts " \
                     f"(Current spend: ${total_cost:,.0f} across WeWork, TOG, and other " \
                     f"office providers). Implement hybrid work policy and reduce footprint " \
                     f"by 25% through vendor consolidation and lease renegotiation."
        
        return title, explanation, potential_savings
    
    def identify_travel_optimization(self) -> Tuple[str, str, int]:
        """Identify travel and expenses optimization."""
        travel_vendors = [
            v for v in self.results 
            if any(kw in v['Vendor Name'].lower() for kw in 
                   ['navan', 'tripactions', 'uber', 'hotel', 'airline', 'travel'])
        ]
        
        total_cost = sum(self.parse_cost(v['Cost']) for v in travel_vendors)
        potential_savings = int(total_cost * 0.15)  # 15% reduction through policy
        
        title = "Travel & Expense Policy Optimization"
        explanation = f"Standardize travel booking and expense management through Navan " \
                     f"consolidation. Current spend across travel vendors: ${total_cost:,.0f}. " \
                     f"Implement strict travel policies and preferred vendor rates."
        
        return title, explanation, potential_savings
    
    def identify_professional_services_optimization(self) -> Tuple[str, str, int]:
        """Identify professional services consolidation."""
        prof_services = [
            v for v in self.results 
            if any(kw in v['Vendor Name'].lower() for kw in 
                   ['consulting', 'advisory', '4i', 'houlihan', 'vector capital', 
                    'mercer', 'rsm', 'eurofast', 'crowe'])
        ]
        
        total_cost = sum(self.parse_cost(v['Cost']) for v in prof_services)
        potential_savings = int(total_cost * 0.20)  # 20% reduction through consolidation
        
        title = "Professional Services Consolidation"
        explanation = f"Consolidate audit, tax, and advisory services to 1-2 primary firms " \
                     f"(Current multi-vendor spend: ${total_cost:,.0f}). Negotiate " \
                     f"enterprise rates for bundled services including audit, tax, and consulting."
        
        return title, explanation, potential_savings
    
    def identify_software_license_optimization(self) -> Tuple[str, str, int]:
        """Identify software licensing optimization."""
        software_vendors = [
            v for v in self.results 
            if any(kw in v['Vendor Name'].lower() for kw in 
                   ['adobe', 'microsoft', 'apple', 'jetbrains', 'slack', 'figma', 
                    'atlassian', 'npm', 'jetbrains', 'pluralsight'])
        ]
        
        total_cost = sum(self.parse_cost(v['Cost']) for v in software_vendors)
        potential_savings = int(total_cost * 0.18)  # 18% reduction through license optimization
        
        title = "Software License Optimization"
        explanation = f"Audit and optimize software licenses including Adobe, Microsoft, " \
                     f"and JetBrains (Current spend: ${total_cost:,.0f}). Implement " \
                     f"license management tool, consolidate duplicate tools, and negotiate " \
                     f"enterprise agreements."
        
        return title, explanation, potential_savings
    
    def get_top_3_opportunities(self) -> List[Tuple[str, str, int]]:
        """Get the 3 highest-impact opportunities."""
        opportunities = [
            self.identify_termination_savings(),
            self.identify_salesforce_optimization(),
            self.identify_office_space_optimization(),
            self.identify_travel_optimization(),
            self.identify_professional_services_optimization(),
            self.identify_software_license_optimization()
        ]
        
        # Sort by savings (descending)
        opportunities.sort(key=lambda x: x[2], reverse=True)
        return opportunities[:3]
    
    def print_opportunities(self):
        """Print top 3 opportunities."""
        opportunities = self.get_top_3_opportunities()
        total_opportunity = sum(opp[2] for opp in opportunities)
        
        print("\n=== TOP 3 COST-SAVING OPPORTUNITIES ===\n")
        for i, (title, explanation, savings) in enumerate(opportunities, 1):
            print(f"OPPORTUNITY {i}: {title}")
            print(f"Estimated Annual Savings: ${savings:,.0f}")
            print(f"Description: {explanation}")
            print()
        
        print(f"TOTAL ANNUAL SAVINGS FROM TOP 3: ${total_opportunity:,.0f}")
        return opportunities, total_opportunity

class QualityCheck:
    """Validates the analysis quality."""
    
    def __init__(self, results_csv: str, output_log: str = "quality_check.txt"):
        """Initialize quality check."""
        self.results = self.load_results(results_csv)
        self.output_log = output_log
        self.issues = []
    
    def load_results(self, csv_path: str) -> List[Dict]:
        """Load results."""
        results = []
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Vendor Name'].strip():
                    results.append(row)
        return results
    
    def check_completeness(self) -> bool:
        """Check if all fields are populated."""
        issues = []
        for i, vendor in enumerate(self.results, 1):
            if not vendor['Department']:
                issues.append(f"Row {i}: Missing department for {vendor['Vendor Name']}")
            if not vendor['Description']:
                issues.append(f"Row {i}: Missing description for {vendor['Vendor Name']}")
            if not vendor['Recommendation']:
                issues.append(f"Row {i}: Missing recommendation for {vendor['Vendor Name']}")
        
        if issues:
            self.issues.extend(issues)
            return False
        return True
    
    def check_department_validity(self) -> bool:
        """Check if departments are valid."""
        valid_depts = [
            "Engineering", "Sales & Marketing", "Finance & Accounting", "HR & Recruitment",
            "Legal & Compliance", "Real Estate & Facilities", "Travel & Transportation",
            "Insurance", "IT Support & Infrastructure", "Consulting & Advisory", "G&A", 
            "Communications"
        ]
        
        issues = []
        for vendor in self.results:
            dept = vendor['Department']
            if dept and dept not in valid_depts:
                issues.append(f"Invalid department '{dept}' for {vendor['Vendor Name']}")
        
        if issues:
            self.issues.extend(issues)
            return False
        return True
    
    def check_recommendation_validity(self) -> bool:
        """Check if recommendations are valid."""
        valid_recs = ["Terminate", "Consolidate", "Optimize"]
        
        issues = []
        for vendor in self.results:
            rec = vendor['Recommendation']
            if rec and rec not in valid_recs:
                issues.append(f"Invalid recommendation '{rec}' for {vendor['Vendor Name']}")
        
        if issues:
            self.issues.extend(issues)
            return False
        return True
    
    def check_descriptions(self) -> bool:
        """Check if descriptions are concise and specific."""
        issues = []
        for vendor in self.results:
            desc = vendor['Description']
            if len(desc) < 10:
                issues.append(f"Description too short for {vendor['Vendor Name']}: {desc}")
            if "business services provider" in desc.lower() or "specialized services" in desc.lower():
                issues.append(f"Description too generic for {vendor['Vendor Name']}: {desc}")
        
        if issues:
            self.issues.extend(issues)
        return len(issues) == 0
    
    def check_logical_recommendations(self) -> bool:
        """Check if recommendations make logical sense."""
        issues = []
        for vendor in self.results:
            name = vendor['Vendor Name'].lower()
            rec = vendor['Recommendation']
            cost = int(vendor['Cost'].replace("$", "").replace(",", ""))
            
            # High-cost vendors should not be terminated
            if rec == "Terminate" and cost > 10000:
                if not any(kw in name for kw in ["recreation", "sports", "personal", "event"]):
                    issues.append(f"High-cost vendor ({cost}) marked Terminate: {vendor['Vendor Name']}")
            
            # Core SaaS tools should not be terminated
            core_tools = ["salesforce", "slack", "microsoft", "google", "aws", "azure"]
            if rec == "Terminate" and any(tool in name for tool in core_tools):
                issues.append(f"Core tool marked Terminate: {vendor['Vendor Name']}")
        
        if issues:
            self.issues.extend(issues)
        return len(issues) == 0
    
    def run_all_checks(self) -> Dict[str, bool]:
        """Run all quality checks."""
        results = {
            "Completeness": self.check_completeness(),
            "Department Validity": self.check_department_validity(),
            "Recommendation Validity": self.check_recommendation_validity(),
            "Description Quality": self.check_descriptions(),
            "Logical Recommendations": self.check_logical_recommendations()
        }
        
        return results
    
    def print_report(self):
        """Print quality check report."""
        results = self.run_all_checks()
        
        print("\n=== QUALITY CHECK REPORT ===\n")
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for check, passed_check in results.items():
            status = "✓ PASS" if passed_check else "✗ FAIL"
            print(f"{status}: {check}")
        
        print(f"\nOverall: {passed}/{total} checks passed")
        
        if self.issues:
            print(f"\nIssues Found ({len(self.issues)}):")
            for issue in self.issues[:20]:  # Show first 20 issues
                print(f"  - {issue}")
            if len(self.issues) > 20:
                print(f"  ... and {len(self.issues) - 20} more issues")
        
        with open(self.output_log, 'w') as f:
            f.write("QUALITY CHECK REPORT\n")
            f.write("=" * 50 + "\n\n")
            for check, passed_check in results.items():
                status = "PASS" if passed_check else "FAIL"
                f.write(f"{status}: {check}\n")
            f.write(f"\nTotal Issues: {len(self.issues)}\n")
            f.write("\nDetailed Issues:\n")
            for issue in self.issues:
                f.write(f"  - {issue}\n")
        
        print(f"\nDetailed report saved to: {self.output_log}")

def main():
    """Main execution."""
    print("Starting opportunity analysis...")
    opp_analyzer = OpportunityAnalyzer("vendor_analysis_enhanced.csv")
    opportunities, total = opp_analyzer.print_opportunities()
    
    print("\nStarting quality check...")
    qc = QualityCheck("vendor_analysis_enhanced.csv")
    qc.print_report()

if __name__ == "__main__":
    main()
