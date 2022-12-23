# BibRec

Recommending Books à la Netflix.

## Build
```sh
# start the container and show logs
make run logs
```

## Documentation

### Jupyter Notebooks
- [Data Exploration](data-exploration.ipynb): Explore the Dataset
- [Data Normalization](data-normalization.ipynb): Showcase Data Normalization
- [Data Hot-Encoding](data-hot-encoding.ipynb): Export Hot-Encoded Dataset
- [Baseline Most Popular](baseline.ipynb): Showcase Baseline with Best Rated Books Algorithm
- [Random Forest Model](rf-model.ipynb): Evaluation of Random Forest Algorithm

### Scripts
- [Train RF Model FULL](bibrec/server/train-rf-model-full.py): Normalize, hot-encode and train with all data from scratch
- [Train RF Model Lightweight](bibrec/server/train-rf-model.py): Uses pre-hot-encoded files and trains with all data

### Evaluation API Strategy

- Daten wurden gefiltert
    - bücher und ratings mit invalider ISBN werden rausgefiltert
    - doppelte bücher werden rausgefiltert
    - ratings auf nicht vorhandene User oder Bücher werden rausgefiltert
    - Nur Explizite Ratings werden verwendet
- Evaluierungsparameter Age und Country sind required arguments
    - Parameter State ist optional, wird allerdings gleich behandelt
    - Parameter City wird nicht verwendet

#### 1. User Daten (Age + Country + State)

Prediction von Büchern mit Random Forest mit Features Age und Country und State

#### 2. User Daten (Age + Country + State) + UserId

Wird eine UserId mitgegeben, werden die bewerteten Bücher des Users herangezogen, um ähnliche Bücher über einen Content
Based Filtering (TF-IDF usw) Ansatz zu finden. Diese Bücher werden bei der Ergebnisliste der Random Forest Prediction
eingestreut (Hybrider Ansatz).

#### 3. User Daten (Age + Country + State) + ItemId

Ähnliche Bücher zu den bewerteten Büchern des Users werden zurückgegeben. Wenn keine ähnlichen Bücher gefunden werden,
werden most popular items zurückgegeben.

#### 4. User Daten (Age + Country + State) + UserId + ItemId

?? Evtl. auch Hybrider Ansatz
