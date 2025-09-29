import os
import pandas as pd
from pathlib import Path

base_dir = r"D:\USJ_2025_2026\Ingenieria de Datos\Git\ingenieria_de_datos\Ejercicio1"
download_dir = os.path.join(base_dir, "downloads")
processed_dir = os.path.join(base_dir, "processed")
os.makedirs(processed_dir, exist_ok=True)

#cargar CSVs como (nombre, df)
frames = []
for csv_name in os.listdir(download_dir):
    if csv_name.lower().endswith(".csv"):
        path = os.path.join(download_dir, csv_name)
        df = pd.read_csv(path)
        name = Path(csv_name).stem
        frames.append((name, df))

#función para calcular duración media en minutos
def mean_trip_minutes(df: pd.DataFrame) -> float | None:
    if "tripduration" in df.columns:
        return (pd.to_numeric(df["tripduration"], errors="coerce") / 60).mean()

    col_alt = "01 - Rental Details Duration In Seconds Uncapped"
    if col_alt in df.columns:
        return (pd.to_numeric(df[col_alt], errors="coerce") / 60).mean()

    if {"started_at", "ended_at"}.issubset(df.columns):
        start = pd.to_datetime(df["started_at"], errors="coerce")
        end   = pd.to_datetime(df["ended_at"], errors="coerce")
        mins = (end - start).dt.total_seconds() / 60
        return mins[mins >= 0].mean()

    return None

#construir el DataFrame de resultados
results = []
for name, df in frames:
    mean_min = mean_trip_minutes(df)
    results.append({"dataset": name, "mean_duracion_min": mean_min})

results_df = pd.DataFrame(results).sort_values("dataset")

#guardar en Excel y CSV
excel_path = os.path.join(processed_dir, "mean_trip_time.xlsx")
csv_path   = os.path.join(processed_dir, "mean_trip_time.csv")

results_df.to_excel(excel_path, index=False)
results_df.to_csv(csv_path, index=False)

print("Guardado Excel:", excel_path)
print("Guardado CSV:", csv_path)

#gráfico
import matplotlib.pyplot as plt

results_df.plot(x="dataset", y="mean_duracion_min", marker="o", legend=False)
plt.xticks(rotation=45)
plt.ylabel("Duración media (min)")
plt.title("Evolución de la duración media por trimestre")
plt.tight_layout()
plt.show()
