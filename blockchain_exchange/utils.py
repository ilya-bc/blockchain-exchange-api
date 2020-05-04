from datetime import datetime


def timestamp_to_datetime(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
