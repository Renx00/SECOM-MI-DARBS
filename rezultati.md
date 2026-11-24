# Rezultāti

## 1. Kas ir šie dati un no kurienes tie nāk?
SECOM dati no UCI krātuves (CC BY 4.0). Tie ir 1567 izstrādājumi no pusvadītāju ražošanas, katram 590 sensoru mērījumi un gala testa rezultāts (derīgs vai brāķis).

## 2. Kas ar datiem bija nepareizi un ko izdarīju?
- Daudz trūkstošu vērtību: 32 sensorus ar vairāk nekā 40 % trūkstošu izmetu, atlikušās 8008 aizpildu ar mediānu (tikai no treniņa datiem).
- 116 sensori rādīja vienu un to pašu vērtību, tos izmetu.
- Dati bija divos failos bez kolonnu nosaukumiem, etiķete bija -1/1: apvienoju, nosaucu kolonnas, brāķi pārveidoju par 1.
- Dublikātu nebija.
- Rindas: 1567 sākumā, 1567 beigās. Sensoru kolonnas: 590 sākumā, 442 beigās.

## 3. Ko modelis prognozē un cik labi?
Modelis prognozē, vai izstrādājums būs brāķis. Precizitāte testā ir 0,9331, bāzes līnija (vienmēr "derīgs") arī 0,9331. **Modelis bāzes līniju nepārspēj.** Tas visus nosauca par derīgiem un neatrada nevienu no 21 brāķa (recall 0,0). Brāķu ir tikai 6,64 %, tāpēc augsta precizitāte neko nepasaka.

## 4. Ko darītu ar prognozi reālā sistēmā?
Ja modelis paredz brāķi, sistēma izstrādājumu atzīmē un tehniķis to papildus pārbauda pirms nākamā ražošanas posma. To automātiski izmest nedrīkstētu.

## 5. Kas notiek, ja modelis kļūdās?
- **Nepamatota trauksme:** tiek bezjēdzīgi tērēts tehniķa laiks un izstrādājums kavējas. 
- **Nepamanīta problēma:** brāķis tiek ražots tālāk un iespējams pat nonāk pie klienta. 
- Sliktāka ir nepamanīta problēma, jo tā var radīt vairāk lieku izmaksu nekā viena pārbaude. Mans modelis tieši tā kļūdījās visos 21 gadījumos.

## 6. Ko ar šo modeli NEDRĪKST darīt?
Nedrīkst izlaist gala testu izstrādājumiem, ko modelis nosauc par derīgiem, jo tas atrada 0 no 21 brāķa.

## Pašvērtējums
Izdevās izveidot visu ķēdi no neapstrādātiem datiem līdz modelim. Neizdevās panākt, lai modelis atrastu brāķus, jo to ir maz. 