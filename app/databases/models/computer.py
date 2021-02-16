from app.databases.db_sql import db_sql
from app.utils.time_utils import datetime_jakarta, timestamp_jakarta


class Computer(db_sql.Model,):
    id = db_sql.Column(db_sql.Integer(), primary_key=True)
    computer_id = db_sql.Column(db_sql.String(40), nullable=False, unique=True)
    computer_name = db_sql.Column(db_sql.String(32), nullable=False)
    computer_location = db_sql.Column(db_sql.String(32), nullable=False)
    computer_power_status = db_sql.Column(db_sql.Integer(), default=0, nullable=False)  # 0: off, 1: on
    computer_cmd = db_sql.Column(db_sql.Integer(), default=1, nullable=False)  # 0: off, 1: on, 2: restart
    computer_cmd_date = db_sql.Column(db_sql.Integer(), default=timestamp_jakarta(), nullable=False)
    computer_ping_timestamp = db_sql.Column(db_sql.Integer(), default=timestamp_jakarta(), nullable=False)
    computer_instance = db_sql.Column(db_sql.String(32), nullable=False)
    created = db_sql.Column(db_sql.DateTime())
    updated = db_sql.Column(db_sql.DateTime())

    def add_timestamp(self):
        self.created = datetime_jakarta()
        self.updated = self.created

    def update_timestamp(self):
        self.updated = datetime_jakarta()

    @staticmethod
    def add(data):
        try:
            data.add_timestamp()
            db_sql.session.add(data)
            db_sql.session.commit()
            return True
        except Exception as e:
            print(e)
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def update(data):
        try:
            data.update_timestamp()
            db_sql.session.commit()
            return True
        except Exception as e:
            print(e)
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    @staticmethod
    def delete(id_data):
        try:
            data = Computer.query.get(id_data)
            db_sql.session.delete(data)
            db_sql.session.commit()
            return True
        except Exception as e:
            print(e)
            db_sql.session.rollback()
            db_sql.session.flush()
            return False

    def to_dict(self):
        data = {
            'id': self.computer_id,
            'name': self.computer_name,
            'location': self.computer_location,
            'power_status': self.computer_power_status,
            'instance': self.computer_instance,
            'cmd': self.computer_cmd,
            'cmd_date': self.computer_cmd_date
        }
        return data

    def on_ping(self):
        try:
            self.computer_ping_timestamp = timestamp_jakarta()
            self.computer_power_status = 1
            db_sql.session.commit()
        except Exception as e:
            print(e)
            db_sql.session.rollback()
            db_sql.session.flush()

    def on_action(self):
        self.computer_cmd_date = timestamp_jakarta()
