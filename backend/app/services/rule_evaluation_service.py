import json
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.app.crud import email_automation as crud_email
from backend.app.services.email_service import email_service
from backend.app.db.session import SessionLocal

class RuleEvaluationService:
    def __init__(self):
        pass

    def _evaluate_condition(self, condition_json: str, data: Dict[str, Any]) -> bool:
        if not condition_json:
            return True  # No conditions means always true
        try:
            conditions = json.loads(condition_json)
            # Simple evaluation for now, can be extended for complex expressions
            # Example: {"ticket_status": "Closed", "department": "Billing"}
            for key, expected_value in conditions.items():
                if data.get(key) != expected_value:
                    return False
            return True
        except json.JSONDecodeError:
            print(f"Warning: Invalid condition_json: {condition_json}")
            return False # Treat invalid JSON as a failed condition

    def evaluate_and_trigger_rules(
        self, 
        trigger_event: str, 
        event_data: Dict[str, Any]
    ):
        with SessionLocal() as db:
            active_rules = crud_email.get_automation_rules(db)
            
            for rule in active_rules:
                if rule.trigger_event == trigger_event and rule.is_active:
                    if rule.condition_json:
                        if not self._evaluate_condition(rule.condition_json, event_data):
                            continue # Condition not met, skip this rule

                    if rule.template_id:
                        # Assuming event_data contains necessary info like 'recipient_email'
                        recipient_email = event_data.get("recipient_email")
                        if not recipient_email:
                            print(f"Warning: No recipient_email found in event_data for rule {rule.id}")
                            continue
                        
                        try:
                            # The event_data itself can serve as context for the template
                            email_service.send_templated_email(
                                template_id=rule.template_id,
                                recipient_email=recipient_email,
                                context=event_data, 
                                automation_rule_id=rule.id
                            )
                            print(f"Triggered email for rule {rule.id} to {recipient_email}")
                        except ValueError as e:
                            print(f"Error triggering email for rule {rule.id}: {e}")
                        except Exception as e:
                            print(f"Unexpected error triggering email for rule {rule.id}: {e}")
                    else:
                        print(f"Rule {rule.id} has no template_id defined. Skipping email dispatch.")

rules_evaluation_service = RuleEvaluationService()
