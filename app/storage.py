from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


MESSAGE_COLUMNS = [
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

SOURCE_RECORD_COLUMNS = [
    "source",
    "external_id",
    "name",
    "url",
    "description",
    "website",
    "phone",
    "rating",
    "review_count",
    "location",
    "niche",
    "is_verified",
    "raw_json",
]


class Storage:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def __enter__(self) -> "Storage":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        self.conn.close()

    def init_db(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS targets (
                target_id INTEGER PRIMARY KEY,
                target_input TEXT NOT NULL,
                target_username TEXT,
                title TEXT,
                last_message_id INTEGER NOT NULL DEFAULT 0,
                last_scraped_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_targets_input ON targets(target_input);

            CREATE TABLE IF NOT EXISTS messages (
                target_id INTEGER NOT NULL,
                target_username TEXT,
                message_id INTEGER NOT NULL,
                date_utc TEXT NOT NULL,
                sender_id INTEGER,
                sender_username TEXT,
                text TEXT,
                entities_json TEXT,
                views INTEGER,
                forwards INTEGER,
                reply_to_msg_id INTEGER,
                media_type TEXT,
                media_metadata_json TEXT,
                scraped_at TEXT NOT NULL,
                PRIMARY KEY (target_id, message_id),
                FOREIGN KEY(target_id) REFERENCES targets(target_id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_messages_target_date
                ON messages(target_id, date_utc);

            CREATE TABLE IF NOT EXISTS scrape_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT NOT NULL,
                mode TEXT NOT NULL,
                target_filter TEXT,
                targets_total INTEGER NOT NULL,
                targets_ok INTEGER NOT NULL,
                targets_failed INTEGER NOT NULL,
                messages_new INTEGER NOT NULL,
                flood_waits INTEGER NOT NULL,
                error_count INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS source_records (
                source TEXT NOT NULL,
                external_id TEXT NOT NULL,
                name TEXT NOT NULL,
                url TEXT,
                description TEXT,
                website TEXT,
                phone TEXT,
                rating REAL,
                review_count INTEGER,
                location TEXT,
                niche TEXT,
                is_verified INTEGER NOT NULL DEFAULT 0,
                raw_json TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                PRIMARY KEY (source, external_id)
            );

            CREATE INDEX IF NOT EXISTS idx_source_records_source
                ON source_records(source, last_seen_at);

            CREATE TABLE IF NOT EXISTS discovery_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT NOT NULL,
                query TEXT,
                niche TEXT,
                has_website TEXT NOT NULL,
                has_phone TEXT NOT NULL,
                location TEXT,
                min_rating REAL NOT NULL,
                only_verified INTEGER NOT NULL DEFAULT 0,
                limit_value INTEGER NOT NULL,
                result_count INTEGER NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT
            );
            """
        )
        self.conn.commit()

    def upsert_target(
        self,
        *,
        target_id: int,
        target_input: str,
        target_username: str | None,
        title: str | None,
        now_utc: str,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO targets (
                target_id, target_input, target_username, title, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(target_id) DO UPDATE SET
                target_input=excluded.target_input,
                target_username=excluded.target_username,
                title=excluded.title,
                updated_at=excluded.updated_at
            """,
            (target_id, target_input, target_username, title, now_utc, now_utc),
        )
        self.conn.commit()

    def get_last_message_id(self, target_id: int) -> int:
        row = self.conn.execute(
            "SELECT last_message_id FROM targets WHERE target_id = ?",
            (target_id,),
        ).fetchone()
        if row is None:
            return 0
        return int(row["last_message_id"] or 0)

    def mark_target_scraped(self, target_id: int, now_utc: str) -> None:
        self.conn.execute(
            """
            UPDATE targets
            SET last_scraped_at = ?, updated_at = ?
            WHERE target_id = ?
            """,
            (now_utc, now_utc, target_id),
        )
        self.conn.commit()

    def update_last_message_id(self, target_id: int, last_message_id: int, now_utc: str) -> None:
        self.conn.execute(
            """
            UPDATE targets
            SET last_message_id = CASE
                    WHEN ? > last_message_id THEN ?
                    ELSE last_message_id
                END,
                last_scraped_at = ?,
                updated_at = ?
            WHERE target_id = ?
            """,
            (last_message_id, last_message_id, now_utc, now_utc, target_id),
        )
        self.conn.commit()

    def insert_message(self, message_row: dict[str, Any]) -> bool:
        placeholders = ", ".join("?" for _ in MESSAGE_COLUMNS)
        columns = ", ".join(MESSAGE_COLUMNS)
        values = [message_row.get(col) for col in MESSAGE_COLUMNS]
        cursor = self.conn.execute(
            f"INSERT OR IGNORE INTO messages ({columns}) VALUES ({placeholders})",
            values,
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_all_messages(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT target_id, target_username, message_id, date_utc, sender_id, sender_username,
                   text, entities_json, views, forwards, reply_to_msg_id, media_type,
                   media_metadata_json, scraped_at
            FROM messages
            ORDER BY target_id ASC, message_id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_target_stats(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT
                t.target_id,
                t.target_username,
                t.title,
                t.target_input,
                t.last_message_id,
                t.last_scraped_at,
                COUNT(m.message_id) AS total_messages,
                MAX(m.date_utc) AS newest_message_date
            FROM targets t
            LEFT JOIN messages m ON m.target_id = t.target_id
            GROUP BY t.target_id, t.target_username, t.title, t.target_input,
                     t.last_message_id, t.last_scraped_at
            ORDER BY total_messages DESC, t.target_id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def insert_scrape_run(self, summary: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO scrape_runs (
                started_at,
                finished_at,
                mode,
                target_filter,
                targets_total,
                targets_ok,
                targets_failed,
                messages_new,
                flood_waits,
                error_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                summary["started_at"],
                summary["finished_at"],
                summary["mode"],
                summary.get("target_filter"),
                summary["targets_total"],
                summary["targets_ok"],
                summary["targets_failed"],
                summary["messages_new"],
                summary["flood_waits"],
                summary["error_count"],
            ),
        )
        self.conn.commit()

    def get_recent_runs(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT id, started_at, finished_at, mode, target_filter,
                   targets_total, targets_ok, targets_failed, messages_new,
                   flood_waits, error_count
            FROM scrape_runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def upsert_source_records(self, rows: list[dict[str, Any]], now_utc: str) -> int:
        if not rows:
            return 0

        placeholders = ", ".join("?" for _ in SOURCE_RECORD_COLUMNS)
        columns = ", ".join(SOURCE_RECORD_COLUMNS)
        values: list[tuple[Any, ...]] = []
        for row in rows:
            payload = [row.get(col) for col in SOURCE_RECORD_COLUMNS]
            payload.extend([now_utc, now_utc])
            values.append(tuple(payload))

        cursor = self.conn.executemany(
            f"""
            INSERT INTO source_records (
                {columns},
                first_seen_at,
                last_seen_at
            )
            VALUES ({placeholders}, ?, ?)
            ON CONFLICT(source, external_id) DO UPDATE SET
                name=excluded.name,
                url=excluded.url,
                description=excluded.description,
                website=excluded.website,
                phone=excluded.phone,
                rating=excluded.rating,
                review_count=excluded.review_count,
                location=excluded.location,
                niche=excluded.niche,
                is_verified=excluded.is_verified,
                raw_json=excluded.raw_json,
                last_seen_at=excluded.last_seen_at
            """,
            values,
        )
        self.conn.commit()
        return cursor.rowcount

    def get_source_records(self, source: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 500))
        if source:
            rows = self.conn.execute(
                """
                SELECT source, external_id, name, url, description, website, phone,
                       rating, review_count, location, niche, is_verified, raw_json,
                       first_seen_at, last_seen_at
                FROM source_records
                WHERE source = ?
                ORDER BY last_seen_at DESC
                LIMIT ?
                """,
                (source, safe_limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT source, external_id, name, url, description, website, phone,
                       rating, review_count, location, niche, is_verified, raw_json,
                       first_seen_at, last_seen_at
                FROM source_records
                ORDER BY last_seen_at DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def insert_discovery_run(self, row: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO discovery_runs (
                source,
                started_at,
                finished_at,
                query,
                niche,
                has_website,
                has_phone,
                location,
                min_rating,
                only_verified,
                limit_value,
                result_count,
                status,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["source"],
                row["started_at"],
                row["finished_at"],
                row.get("query"),
                row.get("niche"),
                row["has_website"],
                row["has_phone"],
                row.get("location"),
                row["min_rating"],
                row["only_verified"],
                row["limit_value"],
                row["result_count"],
                row["status"],
                row.get("error_message"),
            ),
        )
        self.conn.commit()

    def get_recent_discovery_runs(self, source: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 100))
        if source:
            rows = self.conn.execute(
                """
                SELECT id, source, started_at, finished_at, query, niche,
                       has_website, has_phone, location, min_rating, only_verified,
                       limit_value, result_count, status, error_message
                FROM discovery_runs
                WHERE source = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (source, safe_limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT id, source, started_at, finished_at, query, niche,
                       has_website, has_phone, location, min_rating, only_verified,
                       limit_value, result_count, status, error_message
                FROM discovery_runs
                ORDER BY id DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()
        return [dict(row) for row in rows]
