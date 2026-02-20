from __future__ import annotations

import csv
import json
from pathlib import Path

from .storage import Storage


def export_messages(storage: Storage, output_format: str, output_path: Path) -> int:
    rows = storage.get_all_messages()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(rows)

    if output_format == "csv":
        fieldnames = [
            "target_id",
            "target_username",
            "message_id",
            "date_utc",
            "sender_id",
            "sender_username",
            "text",
            "entities_json",
            "views",
            "forwards",
            "reply_to_msg_id",
            "media_type",
            "media_metadata_json",
            "scraped_at",
        ]
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return len(rows)

    raise ValueError(f"Unsupported export format: {output_format}")

