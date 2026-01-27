data_dictionary = "https://portal.pedscommons.org/api/v0/submission/_dictionary/_all"

exclude_files = ['program', 'project']

white_list = {}
white_list["person"] = ["type", "submitter_id", "ethnicity", "race", "sex"]
white_list["subject"] = ["type", "submitter_id", "age_at_censor_status", "censor_status", "honest_broker_subject_id", "persons.submitter_id"]
white_list["medical_history"] = ["type", "submitter_id", "medical_history", "subjects.submitter_id"]
white_list["timing"] = ["type", "submitter_id", "age_at_course_anc_500", "age_at_course_end", "age_at_course_start", "age_at_disease_phase", "course", "course_number", "disease_phase", "disease_phase_number", "timing_type", "year_at_disease_phase", "subjects.submitter_id"]
white_list["molecular_analysis"] = ["type", "submitter_id", "aa_mutation", "age_at_molecular_analysis", "allelic_ratio", "chromosome", "gene1", "gene2", "genetic_seq", "indepen_abb", "iscn", "molecular_abnormality", "molecular_abnormality_result", "molecular_analysis_method", "num_metaphases", "variant_type", "subjects.submitter_id", "timings.submitter_id"]
white_list["secondary_malignant_neoplasm"] = ["type", "submitter_id", "age_at_smn", "smn_morph_icdo", "smn_top_icdo", "subjects.submitter_id"]
white_list["study"] = ["type", "submitter_id", "age_at_enrollment", "enrolled_status", "study_id", "treatment_arm", "subjects.submitter_id"]
white_list["survival_characteristic"] = ["type", "submitter_id", "TRM_type", "age_at_lkss", "age_lost_to_follow_up", "cause_of_death", "cause_of_death_detail", "cause_of_death_ranking", "lkss", "subjects.submitter_id", "timings.submitter_id"]
white_list["radiation_therapy"] = ["type", "submitter_id", "rt_dose", "rt_site", "rt_unit", "subjects.submitter_id", "timings.submitter_id"]
white_list["subject_response"] = ["type", "submitter_id", "age_at_response", "anc_at_response", "anc_threshold_at_response", "bm_analysis_method_at_response", "bm_pct_blasts_at_response", "platelet_count_at_response", "platelet_threshold_at_response", "response", "response_category", "subjects.submitter_id", "timings.submitter_id"]
white_list["disease_characteristic"] = ["type", "submitter_id", "CNS_disease_status", "MLDS", "MPAL", "TAMDS", "detection_method", "disease_site", "fab_type", "secondary_AML", "who_aml", "subjects.submitter_id", "timings.submitter_id"]
white_list["lab"] = ["type", "submitter_id", "age_at_lab", "lab_cat", "lab_method", "lab_result", "lab_result_numeric", "lab_result_unit", "lab_spec_type", "lab_test", "traumatic_tap", "subjects.submitter_id", "timings.submitter_id"]
white_list["minimal_residual_disease"] = ["type", "submitter_id", "age_at_mrd_assessment", "flow_cytometry_type", "mrd_method", "mrd_molecular_markers", "mrd_result", "mrd_result_numeric", "mrd_result_unit", "mrd_sample_source", "mrd_sensitivity", "subjects.submitter_id", "timings.submitter_id"]
white_list["myeloid_sarcoma_involvement"] = ["type", "submitter_id", "myeloid_sarcoma", "myeloid_sarcoma_site", "subjects.submitter_id", "timings.submitter_id"]
white_list["off_protocol_therapy_study"] = ["type", "submitter_id", "age_off", "off_type", "reason_off", "subjects.submitter_id", "timings.submitter_id"]
white_list["stem_cell_transplant"] = ["type", "submitter_id", "age_at_sct", "hla_a_result", "hla_b_result", "hla_c_result", "hla_dq_result", "hla_drb1_result", "hla_match", "number_hla", "number_matches", "sct_conditioning_type", "sct_donor_relationship", "sct_source", "sct_tbi", "sct_type", "subjects.submitter_id", "timings.submitter_id"]
white_list["transfusion_medicine_procedure"] = ["type", "submitter_id", "tmp_product", "tmp_type", "subjects.submitter_id", "timings.submitter_id"]
white_list["vital"] = ["type", "submitter_id", "age_at_vitals", "vitals_result_numeric", "vitals_result_unit", "vitals_test", "subjects.submitter_id", "timings.submitter_id"]