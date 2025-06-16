import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

def create_specification_files():
    """Create text specification and convert to PDF"""
    
    spec_content = """DATA SPECIFICATION DOCUMENT
Version 1.0

1. CUSTOMER DATA SHEET
Required Columns:
- CustomerID (Text, Required): Format "CUST-XXXXX" where X is digit
- FirstName (Text, Required): Max 50 characters
- LastName (Text, Required): Max 50 characters
- Email (Text, Required): Valid email format
- Phone (Text, Optional): Format "(XXX) XXX-XXXX"
- DateJoined (Date, Required): Format DD/MM/YYYY
- Status (Text, Required): Values "Active", "Inactive", "Pending"

2. ORDERS SHEET
Required Columns:
- OrderID (Text, Required): Format "ORD-XXXXXXXX" where X is digit
- CustomerID (Text, Required): Must exist in Customer Data
- OrderDate (Date, Required): Format DD/MM/YYYY
- TotalAmount (Number, Required): Decimal, max value 99999.99
- PaymentMethod (Text, Required): Values "Credit", "Debit", "Cash", "PayPal"
- ShippingStatus (Text, Required): Values "Pending", "Shipped", "Delivered"

3. PRODUCTS SHEET
Required Columns:
- ProductCode (Text, Required): Format "PROD-XXX-YYY" where X is letter, Y is digit
- ProductName (Text, Required): Max 100 characters
- Category (Text, Required): Values "Electronics", "Clothing", "Food", "Other"
- Price (Number, Required): Decimal, positive value
- StockQuantity (Number, Required): Integer, non-negative
- LastUpdated (Date, Required): Format DD/MM/YYYY

BUSINESS RULES:
- OrderDate must be after customer DateJoined
- TotalAmount must be positive and less than 100000
- All dates must be between 01/01/2020 and 31/12/2025
- No duplicate CustomerID or OrderID allowed
- Email addresses must be unique"""

    # First, create the text file
    with open('spec.txt', 'w') as f:
        f.write(spec_content)
    print("✅ Created spec.txt")
    
    # Then convert to PDF if reportlab is available
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        
        # Create PDF from the text file
        c = canvas.Canvas("spec.pdf", pagesize=letter)
        width, height = letter
        
        # Starting position
        y = height - 50
        x = 50
        
        # Read from the text file
        with open('spec.txt', 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.rstrip('\n')
            if y < 50:  # New page if needed
                c.showPage()
                y = height - 50
            
            # Different formatting for headers
            if line.startswith('DATA SPECIFICATION'):
                c.setFont("Helvetica-Bold", 16)
            elif line.strip() and (line[0].isdigit() if line else False) or line.startswith('BUSINESS RULES:'):
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFont("Helvetica", 10)
            
            # Handle long lines
            if len(line) > 80:
                wrapped_lines = simpleSplit(line, "Helvetica", 10, width - 100)
                for wrapped_line in wrapped_lines:
                    c.drawString(x, y, wrapped_line)
                    y -= 15
            else:
                c.drawString(x, y, line)
                y -= 15
        
        c.save()
        print("✅ Created spec.pdf from spec.txt")
        
    except ImportError:
        print("⚠️  reportlab not installed. PDF creation skipped.")
        print("   Install with: pip install reportlab")

def create_excel_with_issues():
    """Create an Excel file with intentional data quality issues"""
    
    # Customer Data Sheet - with various issues
    customer_data = {
        'CustomerID': ['CUST-12345', 'CUST-12346', '', 'CUST-12347', 'CUST-12345', 'CUST12348', 'CUST-12349'],
        'FirstName': ['John', 'Jane', 'Bob', 'Alice', 'John', 'Charlie', ''],
        'LastName': ['Doe', 'Smith', 'Johnson', 'Williams', 'Doe', 'Brown', 'Davis'],
        'Email': ['john.doe@email.com', 'jane.smith@email.com', 'bob.j@email.com', 'alice.w@email', 'john.doe@email.com', 'charlie.b@email.com', 'davis@email.com'],
        'Phone': ['(555) 123-4567', '555-234-5678', '(555) 345-6789', '(555) 456-7890', '(555) 123-4567', None, '(555) 567-8901'],
        'DateJoined': ['15/03/2023', '2024/13/45', '01/01/2024', '20/06/2023', '15/03/2023', '05/09/2023', '10/10/2023'],
        'Status': ['Active', 'Active', 'Pending', 'Invalid', 'Active', 'Inactive', 'Active']
    }
    
    # Orders Sheet - with various issues
    orders_data = {
        'OrderID': ['ORD-12345678', 'ORD-12345679', 'ORD-12345680', 'ORD12345681', 'ORD-12345682', ''],
        'CustomerID': ['CUST-12345', 'CUST-12346', 'CUST-99999', 'CUST-12347', 'CUST-12345', 'CUST-12349'],
        'OrderDate': ['20/03/2023', '10/01/2023', '15/04/2023', '25/06/2023', '32/13/2023', '15/11/2023'],
        'TotalAmount': [150.50, 299.99, 450000, -50, 'abc', 89.99],
        'PaymentMethod': ['Credit', 'PayPal', 'Cash', 'Debit', 'Credit', 'Bitcoin'],
        'ShippingStatus': ['Delivered', 'Shipped', 'Pending', 'Processing', 'Delivered', 'Pending']
    }
    
    # Products Sheet - with various issues
    products_data = {
        'ProductCode': ['PROD-ABC-123', 'PROD-DEF-456', 'PROD-123-ABC', 'PROD-GHI-789', 'PROD-ABC-123', 'PRD-JKL-012', ''],
        'ProductName': ['Laptop Computer', 'Winter Jacket', 'Organic Apples', 'Mystery Item', 'Laptop Computer', 'Smart Watch', 'Unnamed Product'],
        'Category': ['Electronics', 'Clothing', 'Food', 'Unknown', 'Electronics', 'Electronics', 'Other'],
        'Price': [999.99, 149.99, 4.99, 0, 999.99, -299.99, 19.99],
        'StockQuantity': [50, 100, -10, 25, 50, 'many', 5],
        'LastUpdated': ['01/06/2024', '15/05/2024', '20/06/2024', '2024-07-01', '01/06/2024', '10/06/2024', '30/02/2024']
    }
    
    # Data Dictionary Sheet (this should be ignored by the agent)
    data_dict = {
        'Field': ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone'],
        'Type': ['Text', 'Text', 'Text', 'Text', 'Text'],
        'Description': ['Unique customer identifier', 'Customer first name', 'Customer last name', 'Customer email address', 'Customer phone number'],
        'Required': ['Yes', 'Yes', 'Yes', 'Yes', 'No']
    }
    
    # Create Excel writer object
    with pd.ExcelWriter('data.xlsx', engine='openpyxl') as writer:
        # Write each sheet
        pd.DataFrame(customer_data).to_excel(writer, sheet_name='Customer Data', index=False)
        pd.DataFrame(orders_data).to_excel(writer, sheet_name='Orders', index=False)
        pd.DataFrame(products_data).to_excel(writer, sheet_name='Products', index=False)
        pd.DataFrame(data_dict).to_excel(writer, sheet_name='Data Dictionary', index=False)
    
    print("✅ Created data.xlsx")
    print("\n📋 Intentional issues included:")
    print("- Invalid date format: '2024/13/45' in Customer Data")
    print("- Missing CustomerID in row 3")
    print("- Invalid email format: 'alice.w@email'")
    print("- Phone format inconsistency: '555-234-5678' (missing parentheses)")
    print("- Duplicate CustomerID: 'CUST-12345'")
    print("- Order date before customer join date")
    print("- Amount exceeding max: 450000")
    print("- Negative values: -50 (amount), -10 (stock)")
    print("- Invalid date: '32/13/2023'")
    print("- Non-numeric values in numeric fields")
    print("- Invalid status/category values")
    print("- And more...")

if __name__ == "__main__":
    print("🚀 Generating test files for Data QC Agent...\n")
    
    # Create specification files (text and PDF)
    create_specification_files()
    
    # Create Excel file with issues
    create_excel_with_issues()
    
    print("\n✨ Test files generated successfully!")
    print("You can now run your data QC agent with these files.")