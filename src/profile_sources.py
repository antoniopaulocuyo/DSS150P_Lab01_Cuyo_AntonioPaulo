from pathlib import Path
import pandas as pd

# Directories
script_dir = Path(__file__).resolve().parent
RAW = script_dir.parent / "data" / "raw"
docs_dir = script_dir.parent / "docs"

supported_filetype = {".csv": pd.read_csv,
                      ".json": pd.read_json,
                      ".parquet": pd.read_parquet}

print(f"Total file count in {RAW}: {len(list(RAW.iterdir()))}\n")

for file in RAW.iterdir():

    if file.suffix in supported_filetype:
        df = supported_filetype[file.suffix](file)
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        columns = {}
        for col in df.columns:
            columns[col] = str(df[col].dtype)
        num_nulls = df.isnull().sum()
        try:
            num_duplicates = df.duplicated().sum()
        except TypeError:
            num_duplicates = "N/A - unhashable/nested values"
        head = df.head()

        numeric_cols = df.select_dtypes(include="number").columns
        mins = {}
        maxs = {}

        for col in numeric_cols:
            mins[col] = df[col].min()
            maxs[col] = df[col].max()

        # Time coercion
        time_keywords = ["time", "date"]
        mins_time = {}
        maxs_time = {}
        for col in columns:
            if any(keyword in col.lower() for keyword in time_keywords):
                df[col] = pd.to_datetime(df[col], errors="coerce")
                mins_time[col] = df[col].min()
                maxs_time[col] = df[col].max()


        # Profile Report
        output_path = docs_dir / f"{file.name}_report.txt"

        with open(output_path, "w") as new_file:
            new_file.write(f"{file.name} Profile Report \n"
                    f"Path: {file} \n"
                    f"File type: {file.suffix} \n"
                    f"File Size (bytes): {file.stat().st_size} \n"
                    f"Number of rows: {num_rows} \n"
                    f"Number of columns: {num_cols} \n"
                    f"Columns with data types: {columns}\n"
                    f"Number of nulls: \n{num_nulls} \n"
                    f"Number of duplicate rows: {num_duplicates} \n\n")

            for col in numeric_cols:
                    new_file.write(f"{col} ({columns[col]}) values\n"
                                   f"Minimum value: {mins[col]} \n"
                                   f"Maximum value: {maxs[col]} \n\n")

            for col in columns:
                if any(keyword in col.lower() for keyword in time_keywords):
                    new_file.write(f"{col} ({columns[col]}) values\n"
                                   f"Minimum value: {mins_time[col]} \n"
                                   f"Maximum value: {maxs_time[col]} \n")

        with open(output_path, "r") as read_file:
            print(read_file.read())

    else:
        print(f"{file.name} is not read. {file.suffix} not supported")