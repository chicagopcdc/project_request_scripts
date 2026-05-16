import time
from idc_index import IDCClient
from pathlib import Path


patient_ids = None
export_entire_idc = False

if export_entire_idc:
    client = IDCClient()
    client.index.to_json("idc_index.json", orient="records", indent=2)
    print("✅ Saved full index to idc_index.json")

    client.index.to_json("idc_index_table.json", orient="table", indent=2)
    print("✅ Saved full index to idc_index_table.json")

    import pandas as pd
    df_records = pd.read_json("idc_index.json", orient="records")
    print(df_records.shape)
    print(df_records.head())
else:
    patient_ids = ["TCGA-3L-AA1B", "PANLMU"]

    def timed(label, func, *args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[⏱️] {label} took {end - start:.3f} seconds")
        return result


    client = timed("Initialize IDCClient", IDCClient)

    total_count = timed("Count total records", lambda: len(client.index))
    print(f"Total records: {total_count}")

    selection = timed(
        "Filter by PatientID",
        lambda: client.index[client.index["PatientID"].isin(patient_ids)]
    )
    selection_count = timed("Count selection", lambda: len(selection))
    print(f"Selection count: {selection_count}")
    # print(selection["PatientID"])
    # Save entire index DataFrame to JSON
    timed(
        "Save selection to JSON",
        lambda: selection.to_json("idc_index_selection.json", orient="records", indent=2)
    )
    print("✅ Saved selection index to idc_index_selection.json")

    # Download data for selected patients
    Path("files").mkdir(exist_ok=True)
    timed(
        "Download from selection",
        client.download_from_selection,
        patientId=patient_ids,
        downloadDir="./files"
    )

    



