"""Provides the configuration for the ODM plugin."""

from pydantic import BaseModel, ConfigDict


class ODMConfig(BaseModel):
    """Provides the configuration model for the ODM plugin."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    mongo_uri: str = "mongodb://localhost:27017/"

    mongo_database: str = "test"
