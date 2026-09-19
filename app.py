import streamlit as st
from crawler import WebCrawler
from classifier import ActionClassifier
from generator import TestGenerator
from exporter import ExcelExporter

st.set_page_config(page_title="AutoTestCase Gen Pro", layout="wide")

st.title("🏗️ Complete Website QA Generator")
st.markdown("Crawl an entire site and generate comprehensive test cases for Forms, Filters, Nav, and FAQs.")

# Default URL for the user
url = st.text_input("Enter Website URL:", value="http://dev.gaursnewprojects.in/")
max_p = st.slider("Pages to crawl:", 1, 15, 5)

if st.button("Generate Complete Test Plan"):
    if url:
        try:
            with st.spinner("🕷️ Crawling multiple pages and detecting components..."):
                crawler = WebCrawler(url)
                pages_data = crawler.get_elements(max_pages=max_p)
                
            all_tcs = []
            gen = TestGenerator()
            
            if not pages_data:
                st.error("Could not extract data from the website. Please check the URL or your internet connection.")
            else:
                for p_data in pages_data:
                    cls = ActionClassifier()
                    actions = cls.classify(p_data)
                    # Corrected variable name here
                    generated_cases = gen.generate(actions)
                    all_tcs.extend(generated_cases)
                
                if all_tcs:
                    # Corrected the variable name in the success message
                    st.success(f"Done! Scanned {len(pages_data)} pages and generated {len(all_tcs)} test cases.")
                    
                    st.subheader("Preview of Generated Test Cases")
                    st.dataframe(all_tcs)
                    
                    excel_file = ExcelExporter.to_excel(all_tcs)
                    st.download_button(
                        label="📥 Download Full Excel Test Plan", 
                        data=excel_file, 
                        file_name="Complete_QA_Test_Plan.xlsx", 
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("Crawl finished but no testable elements (forms, filters, or buttons) were found.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")