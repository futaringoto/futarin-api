from sqlalchemy.orm import Session

import v2.models.user as user_model


def get_user_by_raspi_id(db: Session, id: int):
    return db.query(user_model.User).filter(user_model.User.raspi_id == id).first()
