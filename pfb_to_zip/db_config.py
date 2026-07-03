"""Load export whitelist/blacklist from amanuensis project_datapoints API."""

import os
import sys
import types
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests


def load_config_module(config_file_path: str):
    path = Path(config_file_path).resolve()
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    return import_module(path.stem)


def get_api_config(
    base_url: str = "https://localhost",
    token: Optional[str] = None):
    return {
        "base_url": os.environ.get("AMANUENSIS_URL", base_url),
        "token": os.environ.get("AMANUENSIS_ACCESS_TOKEN", token),
    }


def project_datapoints_url(base_url: str, endpoint: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/amanuensis"):
        return f"{base}/project-datapoints/{endpoint}"
    return f"{base}/amanuensis/project-datapoints/{endpoint}"


def _auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _request_verify():
    """SSL verification for amanuensis API requests.

    Set AMANUENSIS_INSECURE_SSL=1 for local dev when the portal uses a
    self-signed cert without a localhost SAN (common with gen3-helm).
    """
    if os.environ.get("AMANUENSIS_INSECURE_SSL", "").lower() in ("1", "true", "yes"):
        return False
    ca_bundle = os.environ.get("REQUESTS_CA_BUNDLE")
    return ca_bundle if ca_bundle else True


def fetch_project_datapoints(
    api_config: Dict[str, Any], project_id: int
) -> List[Dict[str, Any]]:
    token = api_config.get("token")
    if not token:
        raise ValueError("AMANUENSIS_ACCESS_TOKEN is required")

    url = project_datapoints_url(api_config["base_url"], "get-datapoints")
    response = requests.get(
        url,
        json={"project_id": project_id, "many": True},
        headers=_auth_headers(token),
        timeout=30,
        verify=_request_verify(),
    )
    response.raise_for_status()
    data = response.json()
    if not data:
        return []
    if isinstance(data, list):
        return data
    return [data]


def add_project_datapoint(
    api_config: Dict[str, Any],
    term: str,
    value_list: List[str],
    dtype: str,
    project_id: int,
) -> None:
    token = api_config.get("token")
    if not token:
        raise ValueError("AMANUENSIS_ACCESS_TOKEN is required")

    url = project_datapoints_url(api_config["base_url"], "add-datapoints")
    response = requests.post(
        url,
        json={
            "term": term,
            "value_list": value_list,
            "type": dtype,
            "project_id": project_id,
        },
        headers=_auth_headers(token),
        timeout=30,
        verify=_request_verify(),
    )
    response.raise_for_status()


def load_config(project_id: int, api_config: Dict[str, Any], fallback_module):
    """
    Load white_list and black_list from project_datapoints for project_id.
    exclude_files and data_dictionary always come from fallback_module.
    Falls back to fallback_module when the API is unavailable or has no rows.
    """
    white_list = {}
    black_list = {}

    try:
        rows = fetch_project_datapoints(api_config, project_id)
    except Exception as exc:
        return fallback_module, (
            f"Config source: local file (could not fetch from amanuensis API: {exc})"
        )

    if not rows:
        return fallback_module, (
            f"Config source: local file (no datapoints found for project_id={project_id})"
        )

    for row in rows:
        term = row.get("term")
        dtype = row.get("type")
        value_list = row.get("value_list") or []
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
        f"Config source: amanuensis API (project_id={project_id}, "
        f"{len(white_list)} whitelist and {len(black_list)} blacklist entries). "
        f"exclude_files and data_dictionary from local file."
    )
    return config, summary
