data_dictionary = "https://portal.pedscommons.org/api/v0/submission/_dictionary/_all"

exclude_files = ['program', 'project', 'external_reference', 'biospecimen']

white_list = {}
white_list["person"] = ["type", "submitter_id", "sex", "race", "ethnicity"]
white_list["subject"] = ["type", "submitter_id", "honest_broker_subject_id", "consortium", "data_contributor_id", "censor_status", "age_at_censor_status", "persons.submitter_id"]
white_list["medical_history"] = ["type", "submitter_id", "medical_history", "medical_history_category", "medical_history_status", "assisted_conception", "subjects.submitter_id"]
white_list["timing"] = ["type", "submitter_id", "timing_type", "disease_phase", "course", "disease_phase_number", "age_at_disease_phase", "year_at_disease_phase", "subjects.submitter_id"]
white_list["biopsy_surgical_procedure"] = ["type", "submitter_id", "age_at_procedure", "tumor_classification", "procedure_site", "procedure_type", "margins", "subjects.submitter_id", "timings.submitter_id"]
white_list["histology"] = ["type", "submitter_id" ,"age_at_hist_assessment", "histology", "histology_grade", "histology_inpc", "subjects.submitter_id", "timings.submitter_id"] 
white_list["molecular_analysis"] = ["type", "submitter_id", "age_at_molecular_analysis", "molecular_abnormality", "gene1", "gene2", "molecular_abnormality_result", "dna_index", "subjects.submitter_id", "timings.submitter_id"] 
white_list["secondary_malignant_neoplasm"] = ["type", "submitter_id", "age_at_smn", "smn_morph_sno", "smn_morph_icdo", "smn_morph_txt", "smn_top_sno", "smn_top_icdo", "smn_top_txt", "smn_yn", "subjects.submitter_id"]
white_list["staging"] = ["type", "submitter_id", "age_at_staging", "stage_system", "stage", "subjects.submitter_id", "timings.submitter_id"] 
white_list["study"] = ["type", "submitter_id", "study_id", "subjects.submitter_id", "treatment_arm"]
white_list["survival_characteristic"] = ["type", "submitter_id", "age_at_lkss", "lkss", "cause_of_death", "cause_of_death_other", "subjects.submitter_id", "timings.submitter_id"]
white_list["tumor_assessment"] = ["type", "submitter_id", "age_at_tumor_assessment", "tumor_classification", "tumor_site", "tumor_site_other", "tumor_state", "subjects.submitter_id", "timings.submitter_id"]
white_list["radiation_therapy"] = ["type", "submitter_id", "age_at_rt_start", "age_at_rt_end", "tumor_classification", "rt_tissue_type", "rt_site", "rt_laterality", "energy_type", "rt_dose", "rt_unit", "boost", "boost_dose", "num_fraction", "transposition_organ", "administration_status", "rt_timing", "subjects.submitter_id", "timings.submitter_id"]
white_list["subject_response"] = ["type", "submitter_id", "age_at_response", "response_category", "tx_prior_response", "interim_response", "response", "response_method", "response_criteria", "response_criteria_version", "necrosis", "necrosis_pct", "bm_pct_blasts_at_response", "bm_analysis_method_at_response", "anc_at_response", "anc_threshold_at_response", "platelet_count_at_response", "platelet_threshold_at_response", "symptoms", "palpable_nodes", "subjects.submitter_id", "timings.submitter_id"]
white_list["total_dose"] = ["type", "submitter_id", "age_at_total_dose_start", "age_at_total_dose_end", "cycle_number", "route", "route_detail", "antineoplastic_agent", "number_doses", "total_dose_administered", "normalization_basis", "total_dose_intended", "total_dose_units", "administration_status", "subjects.submitter_id", "timings.submitter_id"]
white_list["disease_characteristic"] = ["type", "submitter_id", "mki", "nodular_splenic", "initial_treatment_category", "subjects.submitter_id", "timings.submitter_id"]
white_list["lab"] = ["type", "submitter_id", "age_at_lab", "lab_test", "lab_result", "lab_result_numeric", "lab_result_unit", "subjects.submitter_id", "timings.submitter_id"]
		




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