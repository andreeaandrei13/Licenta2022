# Licenta2022

**Achizitia ti analiza datelor dependente de timp**

   Acest proiect are ca si scop realizarea unor reprezentari de tip Time-Series cu ajutorul limbajului de programare Python si a bazei de date InfluxDB.

   In cadrul proiectului se va regasi scrierea datelor din mai multe fisiere CSV in baza de date, realizarea reprezentarii pe harta a antenelor cu ajutorul 
unui fisier GEOJSON, care prezinta coordonatele geografice a acestra, dar si realizarea unor rapoarte care pot reprezenta situatii ipotetice. 
   Datele folosite sunt pentru o saptamana de înregistrari cu detaliile apelurilor din orasele Milano si provincial Trentino (Italia), astfel de fiecare data 
cand un utilizator angajeaza o interactiune de telecomunicatii, o stație radio de baza (RBS) este alocata de catre operator si ofera comunicatia prin retea. 
Toate aste date sunt stocată, iar urmatoarele activitati sunt prezentate in setul de date: SMS-uri primite, SMS-uri trimise, apeluri primite, apeluri efectuate,
activitate pe internet. Fiecare activitate pe internet este generată de fiecare data când un utilizator incepe o conexiune la internet sau incheie o conexiune la 
internet. 
  Setul de date folosit este cu sursa deschisa si se poate descarca de pe ZDATASET, unde se pot regasi si mai multe detalii despre acesta 
(https://zdataset.com/free-dataset/mobile-phone-activity-in-a-city/). 

***Pasii realizati in crearea proiectului:***

- Achizitia datelor
- Stocarea datelor
- Interogarea eficienta
- Vizualizarea
- Analiza
- Predictii

***Codul este si el structurat in urmatori pasi:***
    
- Importarea bibliotecilor necesate
- Realizarea conexiunii cu baza de date (InfluxDB)
- Scrierea datelor 
- Interogarea datelor
- Estimarea datelor
- Geolocatia
- Verificarea pentru rulare

  Codul a fost organizat si sub forma de notebook pentru a fi mai simpla reutilizarea acestuia.Notenook-ul se poate gasi in acest repositor, precum si codul 
propriu-zis, care a fost realizat cu ajutorul limbajului de programare Python si scris in VS Code. Pentru mai multe detalii teoretice legate de tema acestui proiect,
alegerea tehnologiilor cu care sa se implementeze proiectul, dar si pentru pasii necesari in crearea unui client in InfluxDB va indrum sa cititi PDF-ul care se 
regaseste in acest repozitor.
    
