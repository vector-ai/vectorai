import io
import base64
import requests
from typing import Dict, List
from .utils import retry, return_curl_or_response

class ViAudioClient:
    """
    Search and Encoding of Audios
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"
            
    @retry()
    def search_audio(
        self,
        collection_name: str,
        audio,
        fields: List,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Search an audio field with audio using Vector Search
Vector similarity search with an audio directly.

_note: audio has to be stored somewhere and be provided as audio_url, a url that stores the audio_

For example: an audio_url represents sounds that a pokemon make::

    "https://play.pokemonshowdown.com/audio/cries/pikachu.mp3"

    -> <Encode the audio to vector> ->

    audio vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}
    
Args:
	audio_url:
		The audio url of an audio to encode into a vector
	collection_name:
		Name of Collection
	search_fields:
		Vector fields to search through
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	page_size:
		Size of each page of results
	page:
		Page of the results
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	hundred_scale:
		Whether to scale up the metric by 100
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        if type(audio) == str:
            if "http" in audio:
                params = {
                    "username": self.username,
                    "api_key": self.api_key,
                    "collection_name": collection_name,
                    "audio_url": audio,
                    "search_fields": fields,
                    "metric": metric,
                    "min_score": min_score,
                    "page": page,
                    "page_size": page_size,
                    "include_vector": include_vector,
                    "include_count": include_count,
                    "asc": asc
                }
                params.update(kwargs)
                response = requests.post(
                    url="{}/collection/search_with_audio".format(self.url),
                    json=params
                )
                return return_curl_or_response(response, 'json', return_curl=return_curl)
        elif type(audio) == bytes:
            params = {
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "audio": audio.decode(),
                "search_fields": fields,
                "metric": metric,
                "min_score": min_score,
                "page": page,
                "page_size": page_size,
                "include_vector": include_vector,
                "include_count": include_count,
                "asc": asc
            }
            params.update(kwargs)
            response = requests.post(
                url="{}/collection/search_with_audio_upload".format(self.url),
                json=params
            )
            return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_audio_by_upload(
        self,
        collection_name: str,
        audio,
        fields: List,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Search an audio field with uploaded audio using Vector Search with an uploaded audio directly.

_note: audio has to be sent as a base64 encoded string_
    
Args:
	collection_name:
		Name of Collection
	search_fields:
		Vector fields to search against
	page_size:
		Size of each page of results
	page:
		Page of the results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	audio:
		Audio in local file path
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        with open(audio, "rb") as fd:
            contents = fd.read()
        return self.search_audio(
            base64.b64encode(io.BytesIO(contents).read()),
            collection_name,
            fields,
            metric,
            page,
            page_size,
            include_vector,
            include_count,
            asc,
            return_curl=return_curl,
            **kwargs
        )
    
    @retry()
    def encode_audio(self, collection_name: str, audio, return_curl: bool=False, **kwargs):
        """
Encode encode into a vector

_note: audio has to be stored somewhere and be provided as audio_url, a url that stores the audio_

For example: an audio_url represents sounds that a pokemon make::

    "https://play.pokemonshowdown.com/audio/cries/pikachu.mp3"

    -> <Encode the audio to vector> ->

    audio_url vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

Args:
	audio_url:
		The audio url of an audio to encode into a vector
	collection_name:
		Name of Collection
"""
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "audio_url": audio,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/encode_audio".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def encode_audio_job(
        self, collection_name: str, audio_field: str, refresh: bool = False, return_curl: bool=False, **kwargs
    ):
        """
Encode all audios in a field into vectors

Within a collection encode the specified audio field in every document into vectors.

_note: audio has to be stored somewhere and be provided as audio_url, a url that stores the audio_

For example, an audio_url field "pokemon_cries" represents sounds that a pokemon make::

    document 1 audio_url field: {"pokemon_cries" : "https://play.pokemonshowdown.com/audio/cries/pikachu.mp3"}

    document 2 audio_url field: {"pokemon_cries" : "https://play.pokemonshowdown.com/audio/cries/meowth.mp3"}

    -> <Encode the audios to vectors> ->

    document 1 audio_url vector: {"pokemon_cries_vector_": [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]}

    document 2 audio_url vector: {"pokemon_cries_vector_": [0.8364648222923279, 0.6280597448348999, 0.8112713694572449, 0.36105549335479736, 0.005313870031386614 ...]}

Args:
	audio_field:
		The audio field to encode into vectors
	refresh:
		Whether to refresh the whole collection and re-encode all to vectors
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "audio_field": audio_field,
            "refresh": refresh,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/jobs/encode_audio_field".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)
