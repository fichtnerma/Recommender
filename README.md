# BibRec

Recommending Books à la Netflix.

## Dependencies

```
pip install pandas
pip install seaborn
```

## Build

```
cd bibrec/
# build containers
docker-compose up -d
```

## Evaluation API Strategy

- Daten wurden gefiltert
    - bücher und ratings mit invalider ISBN werden rausgefiltert
    - doppelte bücher werden rausgefiltert
    - ratings auf nicht vorhandene User oder Bücher werden rausgefiltert
    - Nur Explizite Ratings werden verwendet
- Evaluierungsparameter Age und Country sind required arguments
    - Parameter State ist optional, wird allerdings gleich behandelt
    - Parameter City wird nicht verwendet

### 1. User Daten (Age + Country + State)

Prediction von Büchern mit Random Forest mit Features Age und Country und State

### 2. User Daten (Age + Country + State) + UserId

Wird eine UserId mitgegeben, werden die bewerteten Bücher des Users herangezogen, um ähnliche Bücher über einen Content
Based Filtering (TF-IDF usw) Ansatz zu finden. Diese Bücher werden bei der Ergebnisliste der Random Forest Prediction
eingestreut (Hybrider Ansatz).

#### 3. User Daten (Age + Country + State) + ItemId

Ähnliche Bücher zu den bewerteten Büchern des Users werden zurückgegeben. Wenn keine ähnlichen Bücher gefunden werden,
werden most popular items zurückgegeben.

### 4. User Daten (Age + Country + State) + UserId + ItemId

?? Evtl. auch Hybrider Ansatz
