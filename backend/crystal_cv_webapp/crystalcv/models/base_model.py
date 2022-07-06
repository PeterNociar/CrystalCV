from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple, Type, TypeVar

from sqlalchemy.exc import DataError
from sqlalchemy.inspection import inspect

from crystalcv.extensions import db

T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def _get_primary_key_manes(cls):
        return [k.name for k in inspect(cls).primary_key]

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)  # pylint: disable=E1101
        if commit:
            db.session.commit()  # pylint: disable=E1101
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)  # pylint: disable=E1101
        return commit and db.session.commit()  # pylint: disable=E1101

    @classmethod
    def commit(cls):
        """Just commit any recent changes, useful if you plan to commit only after
        many changes that need to be done in a single transaction"""
        return db.session.commit()

    @classmethod
    def get_by_id(cls: Type[T], record_id) -> Optional[T]:
        """Get record by ID."""
        try:
            return cls.query.get(record_id)
        except DataError:
            # Wrong format/type of id returns None and does not break the session
            db.session.commit()
            return None

    @classmethod
    def get_by_ids(cls: Type[T], record_ids) -> List[T]:
        return cls.query.filter(cls.id.in_(record_ids)).all()

    def get_changed_attrs(self, **kwargs):
        update = {}
        for key, value in kwargs.items():
            try:
                existing_value = getattr(self, key)
            except AttributeError:
                continue
            else:
                if existing_value != value:
                    update[key] = value
        return update

    def update_if_changed(self, **kwargs):
        update = self.get_changed_attrs(**kwargs)
        if update:
            return self.update(**update)
        return self

    @classmethod
    def get_or_create(cls, keys: Dict, rest: Dict = None) -> Tuple[BaseModel, int]:
        """
        raises MultipleResultsFound
        """
        if rest is None:
            rest = dict()
        created = False
        instance = cls.get_one_by_keys(keys=keys)
        if instance is None:
            instance = cls.create(**keys, **rest)
            created = True
        return instance, created

    @classmethod
    def get_one_by_keys(cls, keys):
        return cls.query.filter_by(**keys).one_or_none()

    @classmethod
    def get_list(cls, keys: Dict = None, order_by: List = None) -> Iterable[BaseModel]:
        if keys is None:
            keys = {}
        query = cls.query.filter_by(**keys)
        if order_by:
            query = query.order_by(*order_by)
        return query.all()

    def update_or_create(self, data, keys: Dict = None):
        if keys:
            instance = self.get_one_by_keys(keys=keys)
        else:
            instance = self.get_by_id(
                tuple(getattr(self, k) for k in self._get_primary_key_manes())
            )
        if instance:
            instance.update(**data)
            return instance
        else:
            return self.save()
