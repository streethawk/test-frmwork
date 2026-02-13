from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator


class OracleClient:
    def __init__(self, user: str, password: str, dsn: str):
        self.user = user
        self.password = password
        self.dsn = dsn

    @contextmanager
    def connection(self) -> Iterator[object]:
        import oracledb

        conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
        try:
            yield conn
        finally:
            conn.close()

    def fetch_rows(self, query: str, binds: dict | None = None) -> list[dict[str, object]]:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, binds or {})
                columns = [col[0] for col in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
