data_dictionary = "https://portal.pedscommons.org/api/v0/submission/_dictionary/_all"

exclude_files = ['program', 'project']

white_list = {}
white_list["person"] = ["type", "submitter_id", "sex", "race", "ethnicity"]
white_list["subject"] = ["type", "submitter_id", "honest_broker_subject_id", "consortium", "data_contributor_id", "censor_status", "age_at_censor_status", "persons.submitter_id"]
white_list["medical_history"] = ["type", "submitter_id", "medical_history", "medical_history_status", "subjects.submitter_id"]
white_list["timing"] = ["type", "submitter_id", "timing_type", "disease_phase", "disease_phase_number", "age_at_disease_phase", "year_at_disease_phase", "course", "course_number", "age_at_course_start", "age_at_course_end", "subjects.submitter_id"]
white_list["biopsy_surgical_procedure"] = ["type", "submitter_id", "age_at_procedure", "tumor_classification", "procedure_site", "procedure_type", "margins", "procedure_treatment_timing", "procedure_performed", "subjects.submitter_id", "timings.submitter_id"]
white_list["histology"] = ["type", "submitter_id" ,"age_at_hist_assessment", "histology", "histology_grade", "subjects.submitter_id", "timings.submitter_id"]
white_list["molecular_analysis"] = ["type", "submitter_id", "age_at_molecular_analysis", "molecular_abnormality", "molecular_abnormality_result", "gene1", "gene2", "anaplasia", "anaplasia_extent", "cytodifferentiation", "mitoses", "subjects.submitter_id", "timings.submitter_id"] 
white_list["secondary_malignant_neoplasm"] = ["type", "submitter_id", "age_at_smn", "smn_site", "smn_type", "subjects.submitter_id"] 
white_list["staging"] = ["type", "submitter_id", "age_at_staging", "tnm_finding", "irs_group", "subjects.submitter_id", "timings.submitter_id"] 
white_list["study"] = ["type", "submitter_id", "study_id", "subjects.submitter_id", "treatment_arm"]
white_list["survival_characteristic"] = ["type", "submitter_id", "age_at_lkss", "lkss", "cause_of_death", "cause_of_death_other", "subjects.submitter_id", "timings.submitter_id"]
white_list["tumor_assessment"] = ["type", "submitter_id", "age_at_tumor_assessment", "tumor_classification", "tumor_site", "tumor_site_other", "tumor_state", "longest_diam_dim1", "longest_diam_dim2", "longest_diam_dim3", "tumor_size", "invasiveness", "nodal_pathology", "nodal_clinical", "parameningeal_extension", "depth", "necrosis", "necrosis_pct", "subjects.submitter_id", "timings.submitter_id"]
white_list["radiation_therapy"] = ["type", "submitter_id", "tumor_classification", "energy_type", "rt_dose", "administration_status", "rt_timing", "subjects.submitter_id", "timings.submitter_id"]
white_list["subject_response"] = ["type", "submitter_id", "age_at_response", "tx_prior_response", "response", "response_method", "necrosis", "necrosis_pct", "subjects.submitter_id", "timings.submitter_id"]
white_list["total_dose"] = ["type", "submitter_id", "route", "antineoplastic_agent", "administration_status", "subjects.submitter_id", "timings.submitter_id"]
		




# black_list = {}
# black_list["person"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "projects.id", "projects.submitter_id"]
# black_list["subject"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "persons.id"]
# black_list["medical_history"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
# black_list["timing"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
# black_list["biopsy_surgical_procedure"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["histology"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["molecular_analysis"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["secondary_malignant_neoplasm"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
# black_list["staging"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["study"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id"]
# black_list["survival_characteristic"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["tumor_assessment"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["radiation_therapy"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["subject_response"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["total_dose"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["disease_characteristic"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]
# black_list["lab"] = ["project_id", "created_datetime", "updated_datetime", "state", "id", "subjects.id", "timings.id"]