# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emailsystem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# --- Models ---
class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    version = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Template {self.name}>'

class AutomationRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    conditions = db.Column(db.JSON, nullable=False)  # e.g., {'priority': 'high', 'category': 'billing'}
    actions = db.Column(db.JSON, nullable=False)    # e.g., {'send_template': 'template_name', 'assign_to': 'team_lead'}
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Rule {self.name}>'

# --- API Endpoints ---

# Email Templates
@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.get_json()
    new_template = EmailTemplate(name=data['name'], subject=data['subject'], body=data['body'])
    db.session.add(new_template)
    db.session.commit()
    return jsonify({'message': 'Template created successfully!', 'template': {'id': new_template.id, 'name': new_template.name}}), 201

@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = EmailTemplate.query.all()
    return jsonify([{'id': t.id, 'name': t.name, 'subject': t.subject, 'body': t.body, 'is_active': t.is_active, 'version': t.version} for t in templates])

@app.route('/api/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    template = EmailTemplate.query.get_or_404(template_id)
    return jsonify({'id': template.id, 'name': template.name, 'subject': template.subject, 'body': template.body, 'is_active': template.is_active, 'version': template.version})

@app.route('/api/templates/<int:template_id>', methods=['PUT'])
def update_template(template_id):
    template = EmailTemplate.query.get_or_404(template_id)
    data = request.get_json()
    template.subject = data.get('subject', template.subject)
    template.body = data.get('body', template.body)
    template.is_active = data.get('is_active', template.is_active)
    template.version += 1  # Increment version on update
    db.session.commit()
    return jsonify({'message': 'Template updated successfully!'})

@app.route('/api/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    template = EmailTemplate.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': 'Template deleted successfully!'})

# Automation Rules
@app.route('/api/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    new_rule = AutomationRule(name=data['name'], conditions=data['conditions'], actions=data['actions'], priority=data.get('priority', 1))
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({'message': 'Rule created successfully!', 'rule': {'id': new_rule.id, 'name': new_rule.name}}), 201

@app.route('/api/rules', methods=['GET'])
def get_rules():
    rules = AutomationRule.query.order_by(AutomationRule.priority.asc()).all()
    return jsonify([{'id': r.id, 'name': r.name, 'conditions': r.conditions, 'actions': r.actions, 'is_active': r.is_active, 'priority': r.priority} for r in rules])

@app.route('/api/rules/<int:rule_id>', methods=['GET'])
def get_rule(rule_id):
    rule = AutomationRule.query.get_or_404(rule_id)
    return jsonify({'id': rule.id, 'name': rule.name, 'conditions': rule.conditions, 'actions': rule.actions, 'is_active': rule.is_active, 'priority': rule.priority})

@app.route('/api/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    rule = AutomationRule.query.get_or_404(rule_id)
    data = request.get_json()
    rule.name = data.get('name', rule.name)
    rule.conditions = data.get('conditions', rule.conditions)
    rule.actions = data.get('actions', rule.actions)
    rule.is_active = data.get('is_active', rule.is_active)
    rule.priority = data.get('priority', rule.priority)
    db.session.commit()
    return jsonify({'message': 'Rule updated successfully!'})

@app.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    rule = AutomationRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'message': 'Rule deleted successfully!'})

# Analytics (Placeholder for actual implementation)
@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    # In a real system, this would query a database of sent emails and their statuses
    return jsonify({
        'total_emails_sent': 12345,
        'open_rate': '75%',
        'click_through_rate': '15%',
        'bounced_emails': 120,
        'delivery_success_rate': '98%'
    })

@app.route('/api/analytics/template_performance', methods=['GET'])
def get_template_performance():
    # Extended analytics for each template would be fetched here
    # This is a mock-up
    return jsonify([
        {'template_name': 'Welcome Email', 'sent': 5000, 'opened': 4000, 'clicked': 800},
        {'template_name': 'Password Reset', 'sent': 2000, 'opened': 1800, 'clicked': 100},
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
