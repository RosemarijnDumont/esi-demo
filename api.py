
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, EmailTemplate, InquiryType

app = Flask(__name__)

# Database setup (replace with your actual database URL)
DATABASE_URL = "sqlite:///./customer_support.db"
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/email_templates', methods=['POST'])
def create_email_template():
    session = DBSession()
    data = request.get_json()
    new_template = EmailTemplate(
        name=data['name'],
        subject=data['subject'],
        body_html=data.get('body_html'),
        body_text=data['body_text'],
        inquiry_type_id=data.get('inquiry_type_id')
    )
    session.add(new_template)
    session.commit()
    session.close()
    return jsonify({"message": "Email template created successfully", "id": new_template.id}), 201

@app.route('/email_templates', methods=['GET'])
def get_email_templates():
    session = DBSession()
    templates = session.query(EmailTemplate).all()
    session.close()
    return jsonify([
        {
            "id": template.id,
            "name": template.name,
            "subject": template.subject,
            "body_html": template.body_html,
            "body_text": template.body_text,
            "inquiry_type_id": template.inquiry_type_id,
        }
        for template in templates
    ])

@app.route('/email_templates/<int:template_id>', methods=['GET'])
def get_email_template(template_id):
    session = DBSession()
    template = session.query(EmailTemplate).filter_by(id=template_id).first()
    session.close()
    if not template:
        return jsonify({"message": "Email template not found"}), 404
    return jsonify({
        "id": template.id,
        "name": template.name,
        "subject": template.subject,
        "body_html": template.body_html,
        "body_text": template.body_text,
        "inquiry_type_id": template.inquiry_type_id,
    })

@app.route('/email_templates/<int:template_id>', methods=['PUT'])
def update_email_template(template_id):
    session = DBSession()
    template = session.query(EmailTemplate).filter_by(id=template_id).first()
    if not template:
        session.close()
        return jsonify({"message": "Email template not found"}), 404

    data = request.get_json()
    template.name = data.get('name', template.name)
    template.subject = data.get('subject', template.subject)
    template.body_html = data.get('body_html', template.body_html)
    template.body_text = data.get('body_text', template.body_text)
    template.inquiry_type_id = data.get('inquiry_type_id', template.inquiry_type_id)
    session.commit()
    session.close()
    return jsonify({"message": "Email template updated successfully"})

@app.route('/email_templates/<int:template_id>', methods=['DELETE'])
def delete_email_template(template_id):
    session = DBSession()
    template = session.query(EmailTemplate).filter_by(id=template_id).first()
    if not template:
        session.close()
        return jsonify({"message": "Email template not found"}), 404
    session.delete(template)
    session.commit()
    session.close()
    return jsonify({"message": "Email template deleted successfully"}), 204

@app.route('/inquiry_types', methods=['POST'])
def create_inquiry_type():
    session = DBSession()
    data = request.get_json()
    new_inquiry_type = InquiryType(
        name=data['name'],
        keywords=data.get('keywords')
    )
    session.add(new_inquiry_type)
    session.commit()
    session.close()
    return jsonify({"message": "Inquiry type created successfully", "id": new_inquiry_type.id}), 201

@app.route('/inquiry_types', methods=['GET'])
def get_inquiry_types():
    session = DBSession()
    inquiry_types = session.query(InquiryType).all()
    session.close()
    return jsonify([
        {
            "id": inquiry.id,
            "name": inquiry.name,
            "keywords": inquiry.keywords,
        }
        for inquiry in inquiry_types
    ])

@app.route('/inquiry_types/<int:inquiry_id>', methods=['GET'])
def get_inquiry_type(inquiry_id):
    session = DBSession()
    inquiry = session.query(InquiryType).filter_by(id=inquiry_id).first()
    session.close()
    if not inquiry:
        return jsonify({"message": "Inquiry type not found"}), 404
    return jsonify({
        "id": inquiry.id,
        "name": inquiry.name,
        "keywords": inquiry.keywords,
    })

@app.route('/inquiry_types/<int:inquiry_id>', methods=['PUT'])
def update_inquiry_type(inquiry_id):
    session = DBSession()
    inquiry = session.query(InquiryType).filter_by(id=inquiry_id).first()
    if not inquiry:
        session.close()
        return jsonify({"message": "Inquiry type not found"}), 404

    data = request.get_json()
    inquiry.name = data.get('name', inquiry.name)
    inquiry.keywords = data.get('keywords', inquiry.keywords)
    session.commit()
    session.close()
    return jsonify({"message": "Inquiry type updated successfully"})

@app.route('/inquiry_types/<int:inquiry_id>', methods=['DELETE'])
def delete_inquiry_type(inquiry_id):
    session = DBSession()
    inquiry = session.query(InquiryType).filter_by(id=inquiry_id).first()
    if not inquiry:
        session.close()
        return jsonify({"message": "Inquiry type not found"}), 404
    session.delete(inquiry)
    session.commit()
    session.close()
    return jsonify({"message": "Inquiry type deleted successfully"}), 204

if __name__ == '__main__':
    # Run migrations before starting the app (example using Alembic)
    # from alembic.config import Config
    # from alembic import command
    # alembic_cfg = Config("alembic.ini") # Assuming alembic.ini is configured
    # command.upgrade(alembic_cfg, "head")
    
    # For a simple run without Alembic, create tables directly:
    Base.metadata.create_all(engine)
    app.run(debug=True)
