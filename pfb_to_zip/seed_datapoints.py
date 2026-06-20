"""Seed project_datapoints from a pfb_to_zip config file."""

import argparse
import os

import psycopg2

from db_config import get_db_kwargs, load_config_module


def ensure_project(cur, project_id, project_name):
    if project_id is not None:
        cur.execute("SELECT id FROM project WHERE id = %s", (project_id,))
        if cur.fetchone():
            return project_id
        cur.execute(
            """
            INSERT INTO project (id, name, description, institution, active)
            VALUES (%s, %s, %s, %s, true)
            """,
            (
                project_id,
                project_name,
                "Seeded for pfb_to_zip export testing",
                "PCDC",
            ),
        )
        return project_id

    cur.execute(
        """
        INSERT INTO project (name, description, institution, active)
        VALUES (%s, %s, %s, true)
        RETURNING id
        """,
        (
            project_name,
            "Seeded for pfb_to_zip export testing",
            "PCDC",
        ),
    )
    return cur.fetchone()[0]


def seed_datapoints(cur, project_id, config_module):
    inserted = 0
    for term, cols in config_module.white_list.items():
        cur.execute(
            """
            INSERT INTO project_datapoints (term, value_list, type, active, project_id)
            VALUES (%s, %s, 'w', true, %s)
            """,
            (term, cols, project_id),
        )
        inserted += 1

    for term, cols in config_module.black_list.items():
        cur.execute(
            """
            INSERT INTO project_datapoints (term, value_list, type, active, project_id)
            VALUES (%s, %s, 'b', true, %s)
            """,
            (term, cols, project_id),
        )
        inserted += 1

    return inserted


def main():
    parser = argparse.ArgumentParser(
        description="Seed amanuensis project_datapoints from a config file"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="./configs/config_inrg.py",
        help="Config file with white_list and black_list",
    )
    parser.add_argument(
        "-p",
        "--project-id",
        type=int,
        default=1,
        help="Project id to seed (creates project if missing)",
    )
    parser.add_argument(
        "--project-name",
        default="INRG Test Export",
        help="Name for the test project if it must be created",
    )
    parser.add_argument("--db-host", default=os.environ.get("AMANUENSIS_DB_HOST", "127.0.0.1"))
    parser.add_argument("--db-port", type=int, default=int(os.environ.get("AMANUENSIS_DB_PORT", "5433")))
    parser.add_argument("--db-name", default=os.environ.get("AMANUENSIS_DB_NAME", "amanuensis_pcdc"))
    parser.add_argument("--db-user", default=os.environ.get("AMANUENSIS_DB_USER", "amanuensis_pcdc"))
    parser.add_argument("--db-password", default=os.environ.get("AMANUENSIS_DB_PASSWORD"))
    args = parser.parse_args()

    config_module = load_config_module(args.config)
    db_kwargs = get_db_kwargs(
        host=args.db_host,
        port=args.db_port,
        dbname=args.db_name,
        user=args.db_user,
        password=args.db_password,
    )

    with psycopg2.connect(**db_kwargs) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM project_datapoints WHERE project_id = %s AND active = true",
                (args.project_id,),
            )
            existing = cur.fetchone()[0]
            if existing:
                print(
                    f"project_id={args.project_id} already has {existing} active datapoints; skipping"
                )
                return

            project_id = ensure_project(cur, args.project_id, args.project_name)
            count = seed_datapoints(cur, project_id, config_module)
            conn.commit()
            print(f"Seeded project_id={project_id} with {count} datapoint rows")


if __name__ == "__main__":
    main()
