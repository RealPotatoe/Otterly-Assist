import datetime


class GuildConfig:
    def __init__(
        self,
        _id: int,
        prefix: str = "?",
        created_at: datetime.datetime = None,
        last_modified_at: datetime.datetime = None,
    ) -> None:
        self._id = _id
        self.prefix = prefix
        self.created_at = created_at or datetime.datetime.utcnow()
        self.last_modified_at = last_modified_at or datetime.datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "prefix": self.prefix,
            "created_at": self.created_at,
            "last_modified_at": self.last_modified_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GuildConfig":
        return cls(
            _id=data.get("_id"),
            prefix=data.get("prefix"),
            created_at=data.get("created_at"),
            last_modified_at=data.get("last_modified_at"),
        )
