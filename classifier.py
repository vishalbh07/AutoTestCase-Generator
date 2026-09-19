class ActionClassifier:
    @staticmethod
    def classify(page_data):
        actions = []
        elements = page_data['elements']
        mod_name = page_data['title']

        # 1. Lead/Enquiry Forms (Highest Priority for Real Estate)
        form_elements = [e for e in elements if e['form_id'] != 'none' or e['tag'] in ['input', 'textarea']]
        if form_elements:
            actions.append({"type": "lead_form", "fields": form_elements, "module": mod_name})

        # 2. Property Filters (Residential, Commercial, etc.)
        filter_keywords = ["residential", "commercial", "plots", "budget", "bhk", "launch", "city"]
        filters = [e for e in elements if any(kw in e['text'].lower() for kw in filter_keywords)]
        if len(filters) >= 2:
            actions.append({"type": "property_filter", "fields": filters, "module": mod_name})

        # 3. FAQ / Accordions
        faq_items = [e for e in elements if "?" in e['text'] or "+" in e['text'] or "faq" in e['class'].lower()]
        if faq_items:
            actions.append({"type": "faq_section", "fields": faq_items, "module": mod_name})

        # 4. Navigation Menu
        nav_keywords = ["menu", "nav", "header", "sticky"]
        nav_elements = [e for e in elements if any(kw in e['class'].lower() or kw in e['parent_class'].lower() for kw in nav_keywords)]
        if nav_elements:
            actions.append({"type": "navigation_menu", "fields": nav_elements, "module": mod_name})

        return actions