from enum import Enum


class VisibilityEnum(str, Enum):
    PUBLIC = "PUBLIC"  # anyone
    PRIVATE = "PRIVATE"  # only uploaded owner


class ShelfTypeEnum(str, Enum):
    SYSTEM = "SYSTEM"  # default: Islamic, General
    CUSTOM = "CUSTOM"  # created by user


class ReadStatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    DROPPED = "DROPPED"  # stopped reading


class AuthorRoleEnum(str, Enum):
    WRITER = "WRITER"
    TRANSLATOR = "TRANSLATOR"
    EDITOR = "EDITOR"
    REVIEWER = "REVIEWER"
