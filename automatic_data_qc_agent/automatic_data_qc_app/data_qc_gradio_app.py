import gradio as gr
import asyncio
from data_qc_agent import analyze_data_quality

def process_files(pdf_file, excel_file):
    """
    Process uploaded PDF and Excel files and return the analysis report.
    
    Args:
        pdf_file: Uploaded PDF file (file object)
        excel_file: Uploaded Excel file (file object)
    
    Returns:
        str: Analysis report in markdown format
    """
    if pdf_file is None or excel_file is None:
        return "Please upload both a PDF specification file and an Excel data file."
    
    try:
        # Read file contents directly as bytes
        pdf_bytes = pdf_file.read() if hasattr(pdf_file, 'read') else pdf_file
        excel_bytes = excel_file.read() if hasattr(excel_file, 'read') else excel_file
        
        # Handle case where files might be file paths (for local testing)
        if isinstance(pdf_bytes, str):
            with open(pdf_bytes, 'rb') as f:
                pdf_bytes = f.read()
        if isinstance(excel_bytes, str):
            with open(excel_bytes, 'rb') as f:
                excel_bytes = f.read()
        
        # Run the analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            analyze_data_quality(pdf_bytes, excel_bytes)
        )
        loop.close()
        
        return result
        
    except Exception as e:
        return f"Error processing files: {str(e)}"

# Create the Gradio interface
def create_interface():
    """Create and return the Gradio interface."""
    
    with gr.Blocks(
        title="Data Quality Analysis Tool",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 📊 Data Quality Analysis Tool
        
        Upload your PDF specification file and Excel data file to get a comprehensive data quality analysis report.
        
        **Instructions:**
        1. Upload your PDF specification file (contains the data requirements and formats)
        2. Upload your Excel data file (the data to be analyzed)
        3. Click "Analyze Data Quality" to generate the report
        """)
        
        with gr.Row():
            with gr.Column():
                pdf_input = gr.File(
                    label="📄 PDF Specification File",
                    file_types=[".pdf"],
                    file_count="single"
                )
                
                excel_input = gr.File(
                    label="📊 Excel Data File", 
                    file_types=[".xlsx", ".xls"],
                    file_count="single"
                )
                
                analyze_btn = gr.Button(
                    "🔍 Analyze Data Quality",
                    variant="primary",
                    size="lg"
                )
        
        with gr.Row():
            with gr.Column():
                output = gr.Markdown(
                    label="📋 Analysis Report",
                    value="Upload files and click 'Analyze Data Quality' to see the analysis report here."
                )
        
        analyze_btn.click(
            fn=process_files,
            inputs=[pdf_input, excel_input],
            outputs=output,
            show_progress=True
        )
        
        gr.Markdown("""
        ### About this tool
        This tool analyzes your Excel data file against PDF specifications and provides:
        - **Structure Compliance**: Verification of sheets, columns, headers, and data types
        - **Format Validation**: Checking dates, numbers, text, and codes formatting
        - **Data Consistency**: Validation of temporal logic and business rules
        - **Quality Checks**: Identification of missing data, duplicates, and outliers
        
        Each issue is reported with precise location, severity, and Excel-based fix recommendations.
        """)
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    interface.launch(
        inbrowser=True,
        quiet=True,
        show_api=False
    )