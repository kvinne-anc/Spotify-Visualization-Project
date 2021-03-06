"""
Input: Takes TrackId from a database which is populated based on the training set
Output: Returns 50 TrackIds that relates to the original TrackId
"""

import logging
from fastapi import APIRouter
import joblib
import pandas as pd


FILENAME = "./app/api/BW_Spotify_Final.joblib"
csv_url = "./app/api/BW_Spotify_Final.csv"

log = logging.getLogger(__name__)
router = APIRouter()


@router.get('/predict/{id}')
async def predict(id: str):
    """
    Takes a trackID string as input and returns a list
    of similar trackIDs
    ### Request Body
    - `Track ID`: String
    example: id =
    '4lsYP6koQW8qqCUrSh6mse',
    '32Lg670koSWkUZQ4ExgMzD',
    '4r9ofEH67ddYsgA6OPBZn5',
    '2v2g5e1hjTquEc03yu1sOg',
    '5bpx60gYQoDDJcP7vBygPB',
    '07j5RLJHwsm4cUb3GGoW3w',
    '684YrlUmbSh6qKvBJaquVE',
    '7iMI1Z3h8H5UdKeA3rBqlP',
    '5oltEh65341tsMWHpWT0h5',
    '6W2iNy14pJ4DW30yCY4bop',
    '1kKLWkqyZEnrOd5tBYYCUn',
    '1kKLWkqyZEnrOd5tBYYCUn',
    '7pv80uUHfocFqfTytu1MVi',
    '1kKLWkqyZEnrOd5tBYYCUn',
    '1kKLWkqyZEnrOd5tBYYCUn',
    '45dAw6GXEsogcDF3NUgj3O',
    '2UH4rbT5WrO2sDCanZI0vX',
    ### Response
    - `Suggested track IDs`: a list of trackIDs that are similar to the user's trackID
    """

    # Import the prediction model
    knn = joblib.load(FILENAME)
    df = pd.read_csv(csv_url)

    # Comes from the colab file containing the prediction model
    def predict_model(track_id, new_df, knn):
        """
        It takes the user's track id and trained dataframe and the joblib model.
        It returns a list of 50 track ids that are similar to the user's track id
        """
        obs = new_df.index[new_df['id'] == track_id]
        series = new_df.iloc[obs, 5:].to_numpy()

        neighbors = knn.kneighbors(series)
        new_obs = neighbors[1][0][6:56]
        return list(new_df.loc[new_obs, 'id'])

    tracks = predict_model(track_id= id, new_df=df, knn=knn)

    return {
         'Suggested track IDs': tracks
         }
