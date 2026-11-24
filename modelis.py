"""Apmāca vienu scikit-learn modeli uz tirs.csv un salīdzina ar bāzes līniju."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score

df = pd.read_csv(Path(__file__).parent / "tirs.csv")
X = df.drop(columns=["brakis"])
y = df["brakis"]

# 80 % treniņam, 20 % testam; stratify saglabā retā brāķa proporciju abās daļās.
X_tren, X_tests, y_tren, y_tests = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Trūkstošās vērtības aizpilda ar mediānu, ko aprēķina tikai no treniņa datiem.
modelis = make_pipeline(SimpleImputer(strategy="median"),
                        RandomForestClassifier(n_estimators=200, random_state=42))
modelis.fit(X_tren, y_tren)
prognoze = modelis.predict(X_tests)

# Bāzes līnija: Nosauc biežāko klasi no treniņa datiem.
baze = DummyClassifier(strategy="most_frequent").fit(X_tren, y_tren)

acc_modelis = accuracy_score(y_tests, prognoze)
acc_baze = accuracy_score(y_tests, baze.predict(X_tests))

print(f"Modeļa precizitāte testā: {acc_modelis:.4f}")
print(f"Bāzes līnija (vienmēr biežākā atbilde): {acc_baze:.4f}")
print("Modelis pārspēj bāzes līniju." if acc_modelis > acc_baze
      else "Modelis NEPĀRSPĒJ bāzes līniju.")

# Papildus: precizitāte slēpj retos brāķus, tāpēc parāda arī to, cik brāķu modelis atrada.
print("Brāķu atrašana (recall):", round(recall_score(y_tests, prognoze), 4))
print("Kļūdu matrica [[TN, FP], [FN, TP]]:")
print(confusion_matrix(y_tests, prognoze))
