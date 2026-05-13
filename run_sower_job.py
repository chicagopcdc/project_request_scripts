import time
import json
from pathlib import Path

import requests
            

def get_fence_user_by_email(base_url, headers, email):
    url = f"{base_url}/amanuensis/admin/get_users"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        filtered_users = [
            user for user in data["users"]
            if user.get("username") == email
        ]
        if len(filtered_users) > 1:
            print(filtered_users)
            print("There should be only one user.")
            exit()
        return filtered_users[0]

    print(f"Failed to run the job. Status code: {response.status_code}")
    print(response.text)
    return None


def save_filterset(base_url, headers, user_id, name, description=None, subject_submitter_id_list=None, export_filter=None):
    url = f"{base_url}/amanuensis/admin/filter-sets"

    payload = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "filters": build_export_input(
            subject_submitter_id_list=subject_submitter_id_list,
            export_filter=export_filter,
        ),
        "ids_list": subject_submitter_id_list
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Filterset saved successfully.")
        return response.json()

    print(f"Failed to save the filterset. Status code: {response.status_code}")
    print(response.text)
    return


def create_project(base_url, headers, user_id, name, code, institution, filterset_id, email):
    url = f"{base_url}/amanuensis/admin/projects"

    payload = {
        "user_id": user_id,
        "name": name,
        "description": code,
        "institution": institution,
        "filter_set_ids": [filterset_id],
        "associated_users_emails": [email]
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("FProject created successfully.")
        return response.json()

    print(f"Failed to create the project. Status code: {response.status_code}")
    print(response.text)
    return


def download_file(url, file_path):
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"File downloaded successfully to {file_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")


def build_export_input(subject_submitter_id_list=None, export_filter=None):
    has_ids = subject_submitter_id_list is not None
    has_filter = export_filter is not None

    if has_ids == has_filter:
        raise ValueError(
            "You must provide exactly one of `subject_submitter_id_list` or `export_filter`."
        )

    if has_ids:
        if not isinstance(subject_submitter_id_list, list) or not subject_submitter_id_list:
            raise ValueError("`subject_submitter_id_list` must be a non-empty list.")

        return {

                "AND": [
                    {
                        "IN": {
                            "subject_submitter_id": subject_submitter_id_list
                        }
                    }
                ]
            }

    if not isinstance(export_filter, dict):
        raise ValueError("`export_filter` must be a dictionary.")

    # Support either:
    # 1. full wrapper: {"filter": {...}}
    # 2. raw filter body: {...}
    return export_filter


def run_export_job(base_url, headers, subject_submitter_id_list=None, export_filter=None):
    url = f"{base_url}/job/dispatch"

    payload = {
        "action": "export",
        "input": {"filter": build_export_input(
            subject_submitter_id_list=subject_submitter_id_list,
            export_filter=export_filter,
        )},
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Success running the job.")
        data = response.json()
        return data["uid"]

    print(f"Failed to run the job. Status code: {response.status_code}")
    print(response.text)
    return None


def get_job_status(base_url, headers, job_uid):
    url = f"{base_url}/job/status?UID={job_uid}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error getting job status")
        print(f"Status code: {response.status_code}")
        print(response.text)
        return False

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from job status response")
        print("Raw response:")
        print(response.text)
        return False

    print(f"Job status: {data.get('status')}")

    return data.get("status") == "Completed"


def get_job_output(base_url, headers, job_uid):
    url = f"{base_url}/job/output?UID={job_uid}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error getting job output")
        print(response.text)
        return None

    data = response.json()
    return data["output"]


if __name__ == "__main__":
    base_url = "https://portal.pedscommons.org"
    access_token = "ACCESS_TOKEN"
    
    skip_create_filterset = False
    local_file_path = "./pfb_to_zip/"
    file_name = "20260513_interact_2026_01.avro"

    # If skip_create_filterset if False please update the following values.
    user_email = "stanley.pounds@stjude.org"
    filterset_name = "INTERACT 2026-01"
    filterset_description = ""
    project_name = "International large-scale clinical and genetic study of congenital and infant acute myeloid leukemia"
    project_code = "INTERACT 2026-01"
    project_institution = "St Jude"
    
    # ------------------------------------------------------------------
    # OPTION 1: Export by list of IDs
    # ------------------------------------------------------------------
    # subject_submitter_id_list = [
    #     "MMT_30127279"
    # ]
    subject_submitter_id_list = None

    # ------------------------------------------------------------------
    # OPTION 2: Export by normal filter
    # Use either this OR subject_submitter_id_list, not both.
    # You can paste either the full {"filter": {...}} wrapper
    # or just the inner filter body.
    # ------------------------------------------------------------------
    # export_filter = None

    export_filter = {
        "AND": [
          {
            "nested": {
              "path": "timings",
              "AND": [
                {
                  "AND": [
                    {
                      "IN": {
                        "disease_phase": [
                          "Initial Diagnosis"
                        ]
                      }
                    },
                    {
                      "EQ": {
                        "disease_phase_number": 1
                      }
                    },
                    {
                      "AND": [
                        {
                          "AND": [
                            {
                              "GTE": {
                                "age_at_disease_phase": 0
                              }
                            },
                            {
                              "LTE": {
                                "age_at_disease_phase": 730.5
                              }
                            }
                          ]
                        }
                      ]
                    },
                    {
                      "AND": [
                        {
                          "AND": [
                            {
                              "GTE": {
                                "year_at_disease_phase": 2000
                              }
                            },
                            {
                              "LTE": {
                                "year_at_disease_phase": 2025
                              }
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          },
          {
            "IN": {
              "consortium": [
                "INTERACT"
              ]
            }
          }
        ]
      }



    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    if not skip_create_filterset:
        print("Saving the filterset")
        user = get_fence_user_by_email(base_url, headers, user_email)
        new_search = save_filterset(
            base_url=base_url,
            headers=headers,
            user_id=user["id"],
            name=filterset_name,
            description=filterset_description,
            subject_submitter_id_list=subject_submitter_id_list,
            export_filter=export_filter,
        )
        print("filterset saved")
        project = create_project(
            base_url=base_url, 
            headers=headers, 
            user_id=user["id"], 
            name=project_name, 
            code=project_code, 
            institution=project_institution, 
            filterset_id=new_search["id"], 
            email=user_email
        )
        print("project created")
        print(project)




    start_time = time.time()

    try:
        job_uid = run_export_job(
            base_url=base_url,
            headers=headers,
            subject_submitter_id_list=subject_submitter_id_list,
            export_filter=export_filter,
        )
    except ValueError as e:
        print(f"Invalid input: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"Unexpected error starting export job: {e}")
        raise


    if not job_uid:
        raise SystemExit(1)

    print(f"Job UID: {job_uid}")

    while not get_job_status(base_url, headers, job_uid):
        elapsed_time = time.time() - start_time
        print(f"Time since start: {elapsed_time:.2f} seconds")
        time.sleep(10)

    download_url = get_job_output(base_url, headers, job_uid)
    if not download_url:
        print("ERROR: download URL is empty or missing")
        raise SystemExit(1)

    output_path = Path(local_file_path) / file_name
    print("Downloading...")
    download_file(download_url, output_path)

    print(f"PROCESS FINISHED, you should find the downloaded file at {output_path}")
    



