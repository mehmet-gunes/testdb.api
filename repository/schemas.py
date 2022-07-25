from .db import ma
from .models import Tube, User


# Tube Schema
class TubeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tube
        include_fk = True
        strict = True


# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        strict = True


# User with Tubes Schema
class UserTubesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        strict = True

    tubes = ma.Nested(TubeSchema, many=True)
