class TestGenerator:
    def __init__(self):
        self.tc_count = 0

    def generate(self, actions):
        tcs = []
        for action in actions:
            atype = action['type']
            fields = action['fields']
            mod = action['module']
            
            if atype == "lead_form":
                self.tc_count += 1
                tcs.append(self._row(self.tc_count, mod, "Verify Lead Enquiry submission with valid data", 
                    "User is on the enquiry section", 
                    "1. Fill all mandatory fields\n2. Click Submit/Enquire button", 
                    "Form submitted successfully; Success message displayed", "High"))
                
                self.tc_count += 1
                tcs.append(self._row(self.tc_count, mod, "Verify Lead Form validation for empty fields", 
                    "User leaves mandatory fields blank", 
                    "1. Click Submit without entering data", 
                    "System should display validation error messages", "Medium"))

            elif atype == "property_filter":
                btn_names = ", ".join([f"'{f['text']}'" for f in fields[:3]])
                self.tc_count += 1
                tcs.append(self._row(self.tc_count, mod, f"Verify content filtering for: {btn_names}", 
                    "Projects listing section is visible", 
                    f"1. Click on {btn_names}\n2. Verify listing update", 
                    "Only properties matching the selected filter should be shown", "High"))

            elif atype == "faq_section":
                self.tc_count += 1
                tcs.append(self._row(self.tc_count, mod, "Verify FAQ Accordion expand/collapse functionality", 
                    "FAQ section is visible", 
                    "1. Click on a question (+)\n2. Click again to collapse (-)", 
                    "The answer should expand and collapse smoothly", "Low"))

            elif atype == "navigation_menu":
                self.tc_count += 1
                tcs.append(self._row(self.tc_count, mod, "Verify Main Navigation Menu links", 
                    "User is at the top of the page", 
                    "1. Click each main menu item (Home, About, etc.)", 
                    "User should be navigated to the correct corresponding page", "Medium"))
        
        return tcs

    def _row(self, id_num, mod, desc, pre, steps, exp, prio):
        return {
            "TC ID": f"TC_{str(id_num).zfill(3)}", "Module": mod, "Test Case Description": desc,
            "Pre-conditions": pre, "Test Steps": steps, "Expected Result": exp,
            "Actual Result": "", "Status": "", "Priority": prio
        }