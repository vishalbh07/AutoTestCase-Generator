from playwright.sync_api import sync_playwright
import re

class WebCrawler:
    def __init__(self, url):
        self.url = url
        self.base_domain = re.search(r'https?://([^/]+)', url).group(1)
        self.pages_data = []

    def get_elements(self, max_pages=8):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()
            
            # 1. Discovery Phase
            try:
                page.goto(self.url, timeout=60000, wait_until="networkidle")
                links = page.query_selector_all("a")
                urls_to_visit = [self.url]
                
                for link in links:
                    href = link.get_attribute("href")
                    if href:
                        # Normalize relative URLs
                        if href.startswith("/"):
                            href = f"{self.url.rstrip('/')}{href}"
                        
                        if (self.base_domain in href) and (href not in urls_to_visit):
                            if len(urls_to_visit) < max_pages:
                                urls_to_visit.append(href)
            except Exception as e:
                print(f"Discovery failed: {e}")
                urls_to_visit = [self.url]

            # 2. Extraction Phase
            for target_url in urls_to_visit:
                try:
                    page.goto(target_url, timeout=45000, wait_until="load")
                    page.wait_for_timeout(2000) # Wait for JS animations
                    
                    elements = []
                    found = page.query_selector_all("input, button, select, a, [role='button'], textarea")
                    
                    for el in found:
                        if not el.is_visible(): continue
                        
                        elements.append({
                            "tag": el.evaluate("el => el.tagName.toLowerCase()"),
                            "text": el.inner_text().strip()[:100],
                            "class": el.get_attribute("class") or "",
                            "id": el.get_attribute("id") or "",
                            "name": el.get_attribute("name") or "",
                            "placeholder": el.get_attribute("placeholder") or "",
                            "form_id": el.evaluate("el => el.closest('form')?.id || 'none'"),
                            "parent_class": el.evaluate("el => el.parentElement?.className || ''")
                        })
                    
                    self.pages_data.append({
                        "title": page.title(),
                        "url": target_url,
                        "elements": elements
                    })
                except Exception as e:
                    print(f"Skipping {target_url}: {e}")
            
            browser.close()
            return self.pages_data