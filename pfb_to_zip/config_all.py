data_dictionary = "https://portal.pedscommons.org/api/v0/submission/_dictionary/_all"

exclude_files = ['program', 'project']


black_list = {}
black_list["person"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "projects.id", "projects.submitter_id"]
black_list["subject"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "persons.id"]
black_list["medical_history"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
black_list["timing"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
black_list["biopsy_surgical_procedure"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["histology"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["molecular_analysis"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["secondary_malignant_neoplasm"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
black_list["staging"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["study"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
black_list["survival_characteristic"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["tumor_assessment"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["radiation_therapy"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["subject_response"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["total_dose"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["disease_characteristic"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["lab"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["lesion_characteristic"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["myeloid_sarcoma_involvement"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["non_protocol_therapy"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["external_reference"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["transfusion_medicine_procedure"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["adverse_event"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["biospecimen"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["immunohistochemistry"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["growing_teratoma_syndrome"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["off_protocol_therapy_study"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["protocol_treatment_modification"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["family_medical_history"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["concomitant_medication"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["minimal_residual_disease"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["stem_cell_transplant"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["function_test"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["cytology"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["cellular_immunotherapy"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["late_effect"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["patient_reported_outcomes_metadata"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
black_list["imaging"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]























