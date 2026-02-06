import os
import sys
from pathlib import Path

from sqlalchemy import text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_engine


def main() -> None:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")

    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("select 1")).scalar()
        print("DB connection OK, select 1 =", result)

        tables = conn.execute(
            text(
                """
                select table_name
                from information_schema.tables
                where table_schema = 'public'
                order by table_name
                """
            )
        ).fetchall()

        print("Tables in public schema:")
        if not tables:
            print("  (none)")
        else:
            for (name,) in tables:
                print(f"  - {name}")


if __name__ == "__main__":
    main()
