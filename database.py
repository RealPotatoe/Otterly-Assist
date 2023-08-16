import logging
import os

import pymongo

from models.guild_config import GuildConfig  # Import the updated GuildConfig model

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self) -> None:
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")

        if not connection_string or not database_name:
            raise ValueError(
                "MONGO_CONNECTION_STRING and DATABASE_NAME environment variables must be set"
            )

        try:
            self.client = pymongo.MongoClient(connection_string)
            self.db = self.client[database_name]
        except pymongo.errors.ConnectionFailure as e:
            logger.error("Failed to connect to the database: %s", str(e))
            raise

    def get_guild_config(self, guild_id: int) -> GuildConfig:
        try:
            config_collection = self.db["guild_configs"]
            config_data = config_collection.find_one({"_id": guild_id})
            if config_data:
                logger.info("Retrieved guild config for guild ID %s", guild_id)
                return GuildConfig.from_dict(config_data)
        except Exception as e:
            logger.error("Error while retrieving guild config: %s", str(e))
            raise
        return None

    def update_guild_config(self, guild_config: GuildConfig) -> None:
        try:
            config_collection = self.db["guild_configs"]
            config_collection.update_one(
                {"_id": guild_config._id},
                {"$set": guild_config.to_dict()},
                upsert=True,
            )
            logger.info("Updated guild config for guild ID %s", guild_config._id)
        except Exception as e:
            logger.error("Error while updating guild config: %s", str(e))
            raise

    def add_guild_config(self, guild_config: GuildConfig) -> None:
        try:
            config_collection = self.db["guild_configs"]
            config_collection.update_one(
                {"_id": guild_config._id},
                {"$set": guild_config.to_dict()},
                upsert=True,
            )
            logger.info("Added guild config for guild ID %s", guild_config._id)
        except Exception as e:
            logger.error("Error while adding guild config: %s", str(e))
            raise

    def delete_guild_config(self, guild_id: int) -> None:
        try:
            config_collection = self.db["guild_configs"]
            config_collection.delete_one({"_id": guild_id})
            logger.info("Deleted guild config for guild ID %s", guild_id)
        except Exception as e:
            logger.error("Error while deleting guild config: %s", str(e))
            raise

    def is_guild_config_present(self, guild_id: int) -> bool:
        try:
            config_collection = self.db["guild_configs"]
            config_data = config_collection.find_one({"_id": guild_id})
            logger.info("Checked if guild config is present for guild ID %s", guild_id)
            return config_data is not None
        except Exception as e:
            logger.error("Error while checking guild config presence: %s", str(e))
            raise
