import pandas as pd
from sqlalchemy import create_engine

file_path = r"C:\Users\wsher\OneDrive\Documents\api-project\data.xlsx"

df = pd.read_excel(file_path, engine="openpyxl")

# clean columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# fix timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# create sqlite DB
engine = create_engine("sqlite:///api_data.db")

# load into DB
df.to_sql("requests", engine, if_exists="replace", index=False)

print("DATABASE LOADED:", df.shape)