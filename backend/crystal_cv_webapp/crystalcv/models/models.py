from uuid import UUID

import pydantic_sqlalchemy
from pydantic import BaseModel as PyBaseModel
from passlib.hash import sha256_crypt
from sqlalchemy import Column, String, ForeignKey, Date, Integer
from sqlalchemy.dialects.postgresql import UUID as puuid

from crystalcv.models.base_model import BaseModel


class PUUID(puuid):
    """this is just to trick pydantic into behaving"""

    @property
    def python_type(self):
        return UUID


class UserModel(BaseModel):
    __tablename__ = "user"

    id = Column(PUUID(as_uuid=True), primary_key=True)
    username = Column(String)
    password = Column(String)

    @classmethod
    def get_user_by_username_and_password(cls, username, password):
        enc_password = sha256_crypt.encrypt(password)
        user = cls.get_one_by_keys(keys={
            "username": username,
            "password": enc_password,
        })
        return user


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id = Column(PUUID(as_uuid=True), primary_key=True)
    user_id = Column(PUUID(as_uuid=True), ForeignKey('user.id'))
    company = Column(String)


class ProjectModel(BaseModel):
    __tablename__ = "project"

    id = Column(PUUID(as_uuid=True), primary_key=True)
    project_name = Column(String)
    position = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    description = Column(String)


class SkillModel(BaseModel):
    __tablename__ = "skill"

    id = Column(PUUID(as_uuid=True), primary_key=True)
    skill_name = Column(String)
    skill_rank = Column(Integer)


#### Pydantic Models ####

_User = pydantic_sqlalchemy.sqlalchemy_to_pydantic(UserModel)
_Company = pydantic_sqlalchemy.sqlalchemy_to_pydantic(CompanyModel)
_Project = pydantic_sqlalchemy.sqlalchemy_to_pydantic(ProjectModel)
_Skill = pydantic_sqlalchemy.sqlalchemy_to_pydantic(SkillModel)


class User(_User):
    pass


class Company(_Company):
    pass


class Project(_Project):
    pass


class Skill(_Skill):
    pass
