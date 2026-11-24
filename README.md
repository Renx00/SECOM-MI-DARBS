# Modelis no sistēmas datiem
Projekts izmanto SECOM datus no pusvadītāju ražošanas (590 sensoru signāli katram izstrādājumam) un prognozē,
vai izstrādājums izturēs gala testu (brakis = 0/1).
tirisana.py sagatavo datus, modelis.py apmāca nejaušo mežu un salīdzina precizitāti ar bāzes līniju.
Rezultātu skaidrojums ir failā rezultati.md.

# Palaišana
pip install pandas scikit-learn
python tirisana.py no dati/secom.data un dati/secom_labels.data izveido tirs.csv.
python modelis.py apmāca modeli un izvada precizitāti un bāzes līniju.

# Bibliotēkas
Python 3.9+, pandas, scikit-learn.
