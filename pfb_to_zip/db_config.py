"""Load export whitelist/blacklist from amanuensis project_datapoints."""

import os
import sys
import types
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Optional
import psycopg2



def load_config_module(config_file_path: str):
    path = Path(config_file_path).resolve()
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    return import_module(path.stem)


def get_db_kwargs(
    host: str = "localhost",
    port: int = 5432,
    dbname: str = "amanuensis_pcdc",
    user: str = "amanuensis_pcdc",
    password: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "host": os.environ.get("AMANUENSIS_DB_HOST", host),
        "port": int(os.environ.get("AMANUENSIS_DB_PORT", port)),
        "dbname": os.environ.get("AMANUENSIS_DB_NAME", dbname),
        "user": os.environ.get("AMANUENSIS_DB_USER", user),
        "password": os.environ.get("AMANUENSIS_DB_PASSWORD", password),
    }


def load_config(project_id: int, db_kwargs: Dict[str, Any], fallback_module):
    """
    Load white_list and black_list from project_datapoints for project_id.
    exclude_files and data_dictionary always come from fallback_module.
    Falls back to fallback_module when the DB is unavailable or has no rows.
    """
    white_list = {}
    black_list = {}

    try:
        conn = psycopg2.connect(**db_kwargs)
    except Exception as exc:
        return fallback_module, (
            f"Config source: local file (could not connect to amanuensis DB: {exc})"
        )

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT term, type, value_list
                    FROM project_datapoints
                    WHERE project_id = %s AND active = true
                    """,
                    (project_id,),
                )
                rows = cur.fetchall()
    except Exception as exc:
        return fallback_module, (
            f"Config source: local file (error querying project_datapoints: {exc})"
        )
    finally:
        conn.close()

    if not rows:
        return fallback_module, (
            f"Config source: local file (no datapoints found for project_id={project_id})"
        )

    for term, dtype, value_list in rows:
        if dtype == "w":
            white_list[term] = list(value_list)
        elif dtype == "b":
            black_list[term] = list(value_list)

    config = types.SimpleNamespace(
        white_list=white_list,
        black_list=black_list,
        exclude_files=list(getattr(fallback_module, "exclude_files", [])),
        data_dictionary=getattr(fallback_module, "data_dictionary", None),
    )
    summary = (
        f"Config source: database (project_id={project_id}, "
        f"{len(white_list)} whitelist and {len(black_list)} blacklist entries). "
        f"exclude_files and data_dictionary from local file."
    )
    return config, summary
