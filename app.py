from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE = 'proposals.db'


# Database file location
DATABASE = 'proposals.db'

def init_db():
    """Initialize the database"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS proposals
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      company_name TEXT,
                      client_name TEXT,
                      client_company TEXT,
                      title TEXT,
                      proposal_date TEXT,
                      expiry_date TEXT,
                      description TEXT,
                      terms TEXT,
                      subtotal REAL,
                      tax REAL,
                      total REAL,
                      items TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")

init_db()

# ...rest of code...

# Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'success', 'message': 'Server is running'})

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """Get all proposals"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM proposals ORDER BY created_at DESC')
        proposals = c.fetchall()
        conn.close()

        result = []
        for p in proposals:
            result.append({
                'id': p[0],
                'company_name': p[1],
                'client_name': p[2],
                'client_company': p[3],
                'title': p[4],
                'proposal_date': p[5],
                'expiry_date': p[6],
                'total': p[11],
                'created_at': p[13]
            })
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    """Get a specific proposal"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM proposals WHERE id = ?', (proposal_id,))
        proposal = c.fetchone()
        conn.close()

        if not proposal:
            return jsonify({'status': 'error', 'message': 'Proposal not found'}), 404

        return jsonify({
            'status': 'success',
            'data': {
                'id': proposal[0],
                'company_name': proposal[1],
                'client_name': proposal[2],
                'client_company': proposal[3],
                'title': proposal[4],
                'proposal_date': proposal[5],
                'expiry_date': proposal[6],
                'description': proposal[7],
                'terms': proposal[8],
                'subtotal': proposal[9],
                'tax': proposal[10],
                'total': proposal[11],
                'items': json.loads(proposal[12]) if proposal[12] else []
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/create', methods=['POST'])
def create_proposal():
    """Create a new proposal"""
    try:
        data = request.json
        
        items = data.get('items', [])
        subtotal = sum(item['quantity'] * item['unitPrice'] for item in items)
        tax = subtotal * 0.10
        total = subtotal + tax

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''INSERT INTO proposals 
                     (company_name, client_name, client_company, title, 
                      proposal_date, expiry_date, description, terms, 
                      subtotal, tax, total, items)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data.get('company_name', ''),
                   data.get('client_name', ''),
                   data.get('client_company', ''),
                   data.get('title', ''),
                   data.get('proposal_date', ''),
                   data.get('expiry_date', ''),
                   data.get('description', ''),
                   data.get('terms', ''),
                   subtotal,
                   tax,
                   total,
                   json.dumps(items)))
        conn.commit()
        proposal_id = c.lastrowid
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Proposal created successfully',
            'id': proposal_id
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>/update', methods=['PUT'])
def update_proposal(proposal_id):
    """Update an existing proposal"""
    try:
        data = request.json
        
        items = data.get('items', [])
        subtotal = sum(item['quantity'] * item['unitPrice'] for item in items)
        tax = subtotal * 0.10
        total = subtotal + tax

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE proposals 
                     SET company_name=?, client_name=?, client_company=?, 
                         title=?, proposal_date=?, expiry_date=?, 
                         description=?, terms=?, subtotal=?, tax=?, total=?, items=?
                     WHERE id=?''',
                  (data.get('company_name', ''),
                   data.get('client_name', ''),
                   data.get('client_company', ''),
                   data.get('title', ''),
                   data.get('proposal_date', ''),
                   data.get('expiry_date', ''),
                   data.get('description', ''),
                   data.get('terms', ''),
                   subtotal,
                   tax,
                   total,
                   json.dumps(items),
                   proposal_id))
        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Proposal updated successfully'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>', methods=['DELETE'])
def delete_proposal(proposal_id):
    """Delete a proposal"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM proposals WHERE id=?', (proposal_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Proposal deleted successfully'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/<int:proposal_id>/pdf', methods=['GET'])
def download_pdf(proposal_id):
    """Generate and download proposal as PDF"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM proposals WHERE id=?', (proposal_id,))
        proposal = c.fetchone()
        conn.close()

        if not proposal:
            return jsonify({'status': 'error', 'message': 'Proposal not found'}), 404

        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=6,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12
        )

        # Title
        elements.append(Paragraph(proposal[4], title_style))
        elements.append(Paragraph(f"Proposal for: <b>{proposal[3]}</b>", styles['Normal']))
        elements.append(Spacer(1, 20))

        # From section
        elements.append(Paragraph("From", heading_style))
        elements.append(Paragraph(f"<b>{proposal[1]}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))

        # To section
        elements.append(Paragraph("To", heading_style))
        elements.append(Paragraph(f"<b>{proposal[2]}</b>", styles['Normal']))
        elements.append(Paragraph(proposal[3], styles['Normal']))
        elements.append(Spacer(1, 12))

        # Dates
        elements.append(Paragraph("Dates", heading_style))
        elements.append(Paragraph(f"Proposal Date: <b>{proposal[5]}</b>", styles['Normal']))
        elements.append(Paragraph(f"Valid Until: <b>{proposal[6]}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Description
        elements.append(Paragraph("Description", heading_style))
        elements.append(Paragraph(proposal[7], styles['Normal']))
        elements.append(Spacer(1, 12))

        # Items table
        elements.append(Paragraph("Services & Items", heading_style))
        items = json.loads(proposal[12]) if proposal[12] else []
        
        table_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
        for item in items:
            total = item['quantity'] * item['unitPrice']
            table_data.append([
                item['description'],
                str(item['quantity']),
                f"${item['unitPrice']:.2f}",
                f"${total:.2f}"
            ])
        
        table_data.append(['', '', 'Subtotal:', f"${proposal[9]:.2f}"])
        table_data.append(['', '', 'Tax (10%):', f"${proposal[10]:.2f}"])
        table_data.append(['', '', 'Total:', f"${proposal[11]:.2f}"])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -4), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -3), (-1, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, -3), (-1, -1), colors.whitesmoke),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Terms
        elements.append(Paragraph("Terms & Conditions", heading_style))
        elements.append(Paragraph(proposal[8], styles['Normal']))
        elements.append(Spacer(1, 30))

        # Footer
        elements.append(Paragraph(
            "Thank you for your consideration. We look forward to working with you!",
            styles['Normal']
        ))

        doc.build(elements)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{proposal[4].replace(' ', '_')}.pdf"
        )
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/calculate', methods=['POST'])
def calculate_totals():
    """Calculate proposal totals"""
    try:
        data = request.json
        items = data.get('items', [])
        
        subtotal = sum(item['quantity'] * item['unitPrice'] for item in items)
        tax = subtotal * 0.10
        total = subtotal + tax

        return jsonify({
            'status': 'success',
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'total': round(total, 2)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proposals/search', methods=['GET'])
def search_proposals():
    """Search proposals by client name or company"""
    try:
        query = request.args.get('q', '')
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''SELECT * FROM proposals 
                     WHERE client_name LIKE ? OR client_company LIKE ? OR title LIKE ?
                     ORDER BY created_at DESC''',
                  (f'%{query}%', f'%{query}%', f'%{query}%'))
        proposals = c.fetchall()
        conn.close()

        result = []
        for p in proposals:
            result.append({
                'id': p[0],
                'company_name': p[1],
                'client_name': p[2],
                'client_company': p[3],
                'title': p[4],
                'proposal_date': p[5],
                'total': p[11],
                'created_at': p[13]
            })
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)