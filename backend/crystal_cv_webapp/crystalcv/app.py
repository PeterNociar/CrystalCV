from pathlib import Path

import connexion
from flask import Flask

from crystalcv import PROJECT_ROOT
from crystalcv.extensions import db, migrate


class AppFactory:
    @classmethod
    def create_app(cls, config_path, app_name):
        """Application factory, used to create application
        """
        app = Flask(app_name)
        app.config.from_object(config_path)
        spec_dir = Path(PROJECT_ROOT, "crystalcv", "openapi")
        cls.init_connexion(app=app, spec_dir=spec_dir)
        cls.register_extensions(app)

        return app

    @classmethod
    def init_connexion(cls, app: Flask, spec_dir: Path):
        """Initialize API from openapi spec"""
        connexion_app = connexion.App(__name__, specification_dir=spec_dir, skip_error_handlers=True)
        connexion_app.app = app

        connexion_app.add_api(
            specification="api.yaml",
            base_path="/api/v1",
            validate_responses=False,
            strict_validation=True,
            resolver_error=501,
        )

    @classmethod
    def register_extensions(cls, app):
        db.init_app(app)
        migrate.init_app(app, db)

