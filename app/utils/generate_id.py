import bson  # pyright: ignore[reportMissingTypeStubs]


def generate_id() -> str:
    return str(bson.ObjectId())
