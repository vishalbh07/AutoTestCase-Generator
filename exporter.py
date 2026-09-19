import pandas as pd
from io import BytesIO

class ExcelExporter:
    @staticmethod
    def to_excel(test_cases):
        df = pd.DataFrame(test_cases)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='QA_Test_Plan')
            worksheet = writer.sheets['QA_Test_Plan']
            for idx, col in enumerate(df.columns):
                worksheet.column_dimensions[chr(65 + idx)].width = 30
        return output.getvalue()