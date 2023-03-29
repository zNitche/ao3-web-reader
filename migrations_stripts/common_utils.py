from config import Config
import sqlalchemy
import sqlalchemy.orm
import json
from datetime import datetime


def init_db_session(db_path=None):
    db_path = Config.SQLALCHEMY_DATABASE_URI if db_path is None else f"sqlite:////{db_path}"
    engine = sqlalchemy.create_engine(db_path)

    return sqlalchemy.orm.sessionmaker(engine)


def get_data_from_models(session, models):
    data = {}

    for base_model in models:
        print(f"getting data for {base_model.__name__}...")
        data[base_model.__name__] = [model.__dict__ for model in session.query(base_model).all()]

    data = clear_db_data(data)

    return data


def clear_db_data(db_data):
    for model_name in db_data:
        for model in db_data[model_name]:
            del model["_sa_instance_state"]

    return db_data


def write_data(db_data, file_path):
    with open(file_path, "w") as file:
        file.write(json.dumps(db_data, indent=4, sort_keys=True, default=str))


def copy_models(model_db_data, model, session):
    models_ids_in_db = [model.id for model in session.query(model).all()]

    for data in model_db_data:
        model_id = data["id"]
        if model_id not in models_ids_in_db:
            new_model = model(**data)
            session.add(new_model)


def tweak_json_dates(data):
    for model_name in data:
        for model in data[model_name]:
            for model_key in model:
                if "date" in model_key:
                    model[model_key] = datetime.fromisoformat(model[model_key])

    return data


def load_db_data(data_path):
    with open(data_path, "r") as file:
        data = json.loads(file.read())

    return data


def add_model(base_model, session, data):
    model = base_model(**data)
    session.add(model)
