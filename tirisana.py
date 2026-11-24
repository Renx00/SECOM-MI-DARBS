"""Datu sagatavošana: nolasa dati/secom.data un dati/secom_labels.data
un saglabā sakārtotu tirs.csv. Oriģinālie faili netiek mainīti."""
from pathlib import Path
import pandas as pd

MAPE = Path(__file__).parent
DATI = MAPE / "dati" / "secom.data"
ETIKETES = MAPE / "dati" / "secom_labels.data"
IZEJA = MAPE / "tirs.csv"

# 1. Dati nav CSV, bet teksta faili ar atstarpēm bez kolonnu nosaukumiem, tāpēc tos nolasa ar atstarpi kā atdalītāju un kolonnām dod nosaukumus.
sensori = pd.read_csv(DATI, sep=r"\s+", header=None, na_values=["NaN"])
sensori.columns = [f"s{i}" for i in range(sensori.shape[1])]
etiketes = pd.read_csv(ETIKETES, sep=" ", header=None, names=["klase", "laiks"])
print("Rindu skaits sākumā:", len(sensori), "| sensoru kolonnu skaits:", sensori.shape[1])

# 2. Mērījumi un rezultāts ir divos atsevišķos failos, kur n-tā rinda atbilst n-tajam izstrādājumam, tāpēc tos apvieno pēc rindas numura.
assert len(sensori) == len(etiketes), "Failu rindu skaiti nesakrīt"
df = pd.concat([sensori, etiketes], axis=1).copy()

# 3. Etiķete ir -1 (derīgs) un 1 (brāķis), un modeļiem ērtāk ir 0/1, tāpēc brāķi atzīmē ar 1, derīgos ar 0.
df["brakis"] = (df["klase"] == 1).astype(int)

# 4. Laiks un vecā klase nav sensoru mērījumi, un modelim tos nedod, lai tas mācās no procesa signāliem, nevis no datuma vai atbildes kopijas.
df = df.drop(columns=["laiks", "klase"])

# 5. Dublikāti vienu un to pašu izstrādājumu skaitītu vairākkārt, tāpēc tiek atstāts tikai pirmais ieraksts.
df = df.drop_duplicates()

# 6. Dažiem sensoriem trūkst vairāk nekā 40 % vērtību, un tādu kolonnu aizpildīšana būtu izdomāšana, tāpēc tās izmet.
sensoru_kol = [k for k in df.columns if k != "brakis"]
daudz_truukst = [k for k in sensoru_kol if df[k].isna().mean() > 0.40]
df = df.drop(columns=daudz_truukst)

# 7. Daudzi sensori visā laikā rāda vienu un to pašu vērtību un nespēj atšķirt derīgo no brāķa, tāpēc tos izmet.
konstantas = [k for k in df.columns if k != "brakis" and df[k].nunique(dropna=True) <= 1]
df = df.drop(columns=konstantas)

# 8. Atlikušās retās NaN vērtības apzināti atstāj, lai mediānu aprēķinātu tikai no treniņa datiem modelis.py (citādi testa dati ietekmētu apmācību).
print("Rindu skaits beigās:", len(df), "| sensoru kolonnu skaits:", df.shape[1] - 1)
print("Izmestas kolonnas ar >40% trūkstošu:", len(daudz_truukst), "| konstantas:", len(konstantas))
print("Atlikušas trūkstošas vērtības:", int(df.isna().sum().sum()))
print("Brāķa īpatsvars:", round(df["brakis"].mean() * 100, 2), "%")
df.to_csv(IZEJA, index=False)
print("Saglabāts:", IZEJA.name)
