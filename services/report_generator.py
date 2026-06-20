import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_pdf(user_name, month, year, expenses, insights, recommendations, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = styles['Heading1']
        title_style.alignment = 1
        elements.append(Paragraph(f"Monthly Expense Report: {month}/{year}", title_style))
        elements.append(Spacer(1, 12))

        # User Info
        elements.append(Paragraph(f"User: {user_name}", styles['Normal']))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Expenses Table
        data = [['Date', 'Description', 'Category', 'Mode', 'Amount (Rs)']]
        total = 0
        for exp in expenses:
            date_str = exp.get('date', '')
            if 'T' in date_str:
                date_str = date_str.split('T')[0]
            elif ' ' in date_str:
                date_str = date_str.split(' ')[0]
            
            data.append([
                date_str, 
                exp.get('description', ''), 
                exp.get('category', ''), 
                exp.get('payment_mode', ''), 
                str(exp.get('amount', 0))
            ])
            total += float(exp.get('amount', 0))
            
        data.append(['', '', '', 'Total', str(total)])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Insights
        elements.append(Paragraph("Spending Insights", styles['Heading2']))
        for insight in insights:
            elements.append(Paragraph(f"- {insight}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Recommendations
        elements.append(Paragraph("Savings Recommendations", styles['Heading2']))
        for rec in recommendations:
            elements.append(Paragraph(f"- {rec}", styles['Normal']))

        doc.build(elements)
