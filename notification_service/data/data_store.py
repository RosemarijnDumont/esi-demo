import json
import os
import logging
import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataStore:
    _data_file = 'data.json'

    @classmethod
    def _load_data(cls) -> dict:
        if not os.path.exists(cls._data_file):
            return {"cleaning_schedule": {}, "hcat_delivery_logs": [], "team_configs": {}}
        with open(cls._data_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.error("Error decoding JSON from %s. Returning empty data structure.", cls._data_file)
                return {"cleaning_schedule": {}, "hcat_delivery_logs": [], "team_configs": {}}

    @classmethod
    def _save_data(cls, data: dict):
        with open(cls._data_file, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def get_cleaning_schedule(cls) -> dict:
        data = cls._load_data()
        return data.get("cleaning_schedule", {})

    @classmethod
    def add_cleaning_schedule_entry(cls, entry: dict):
        data = cls._load_data()
        schedule_id = str(uuid.uuid4()) # Generate a unique ID for the schedule entry
        entry['id'] = schedule_id
        data["cleaning_schedule"][schedule_id] = entry
        cls._save_data(data)

    @classmethod
    def update_cleaning_schedule_entry(cls, schedule_id: str, updates: dict) -> bool:
        data = cls._load_data()
        if schedule_id in data["cleaning_schedule"]:
            data["cleaning_schedule"][schedule_id].update(updates)
            cls._save_data(data)
            return True
        return False

    @classmethod
    def delete_cleaning_schedule_entry(cls, schedule_id: str) -> bool:
        data = cls._load_data()
        if schedule_id in data["cleaning_schedule"]:
            del data["cleaning_schedule"][schedule_id]
            cls._save_data(data)
            return True
        return False

    @classmethod
    def log_hcat_delivery(cls, log_entry: dict):
        data = cls._load_data()
        log_entry["timestamp"] = datetime.now().isoformat()
        data["hcat_delivery_logs"].append(log_entry)
        cls._save_data(data)
        logging.info("Logged HCAT delivery for task_id: %s, status: %s", log_entry.get('task_id'), log_entry.get('status'))

    @classmethod
    def get_hcat_delivery_logs(cls) -> list:
        data = cls._load_data()
        return data.get("hcat_delivery_logs", [])

    @classmethod
    def get_team_config(cls, team_id: str) -> dict or None:
        data = cls._load_data()
        return data.get("team_configs", {}).get(team_id)

    @classmethod
    def get_all_team_configs(cls) -> dict:
        data = cls._load_data()
        return data.get("team_configs", {})

    @classmethod
    def add_team_config(cls, team_config: dict):
        data = cls._load_data()
        team_id = team_config.get('team_id')
        if team_id:
            data["team_configs"][team_id] = team_config
            cls._save_data(data)
        else:
            logging.error("Attempted to add team config without 'team_id'. Entry: %s", team_config)

    @classmethod
    def update_team_config(cls, team_id: str, updates: dict) -> bool:
        data = cls._load_data()
        if team_id in data["team_configs"]:
            data["team_configs"][team_id].update(updates)
            cls._save_data(data)
            return True
        return False

    @classmethod
    def delete_team_config(cls, team_id: str) -> bool:
        data = cls._load_data()
        if team_id in data["team_configs"]:
            del data["team_configs"][team_id]
            cls._save_data(data)
            return True
        return False

