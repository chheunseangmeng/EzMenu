import os
from datetime import datetime
from fpdf import FPDF

def generate_pdf_receipt(cart_items, subtotal, telegram_id, customer_name):
    if not os.path.exists("receipts"):
        os.makedirs("receipts")

    receipt_no = f"R{datetime.now().strftime('%Y%m%d%H%M%S')}"
    file_path = f"receipts/{receipt_no}.pdf"

    #pdf width & height
    pdf = FPDF(unit='mm', format=(98, 160))
    pdf.add_page()
    
    # Set font
    pdf.set_font('Courier', '', 8)
    
    # Header
    pdf.cell(0, 4, 'EZMENU SHOP', ln=True, align='C')
    pdf.ln(2)
    
    # Customer info
    pdf.cell(0, 4, f"Receipt No     :         {receipt_no}", ln=True)
    pdf.cell(0, 4, f"Date           :         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 4, f"Customer       :         {customer_name}", ln=True)
    pdf.ln(2)
    
    # Separator
    pdf.cell(0, 4, '-' * 45, ln=True)
    pdf.ln(0.5)
    
    #Header labels
    pdf.cell(30, 4, "Name", ln=0)
    pdf.cell(15, 4, "Qty", ln=0)
    pdf.cell(20, 4, "Price", ln=0)
    pdf.cell(26, 4, "Total", ln=True)
    
    pdf.cell(0, 4, '-' * 45, ln=True)
    pdf.ln(2)
    
    # Items
    for item in cart_items:
        name = item["name"]
        qty = item["quantity"]
        price = item["price"]
        total = qty * price
        
        # Truncate name if too long
        if len(name) > 12:
            name = name[:10] + ".."
        
        # Print item in columns
        pdf.cell(30, 4, name, ln=0)
        pdf.cell(15, 4, str(qty), ln=0)
        pdf.cell(20, 4, f"${price:.2f}", ln=0)
        pdf.cell(26, 4, f"${total:.2f}", ln=True)
    
    pdf.ln(2)
    pdf.cell(0, 4, '-' * 45, ln=True)
    pdf.ln(2)
    
    # Totals
    pdf.cell(0, 4, f"Subtotal       :                      ${subtotal:.2f}", ln=True)
    pdf.cell(0, 4, f"TOTAL          :                      ${subtotal:.2f}", ln=True)
    pdf.cell(0, 4, f"Payment Status :                      PAID", ln=True)
    
    pdf.ln(4)
    pdf.cell(0, 4, '-' * 45, ln=True)
    pdf.ln(2)

    #img path fixed
    qr_image_path = "qrcodes/qr_open_bot.png" 
    
    # QR code in center
    pdf.image(qr_image_path, x=34, y=pdf.get_y(), w=30, h=30)
    pdf.ln(32)
    
    # Scan instruction
    pdf.set_font('Courier', '', 6)
    pdf.cell(0, 3, 'Scan for new ordering', ln=True, align='C')
    pdf.ln(4)
    
    # Footer
    pdf.set_font('Courier', '', 8)
    pdf.cell(0, 4, '-' * 45, ln=True)
    pdf.ln(2)
    pdf.cell(0, 4, f"Thank you, {customer_name}!", ln=True, align='C')
    
    # Output
    pdf.output(file_path)

    return file_path