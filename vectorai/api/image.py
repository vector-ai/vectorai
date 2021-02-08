import io
import base64
import requests
from typing import Dict, List
from .utils import retry, return_curl_or_response

class ViImageClient:
    """
    Search and Encoding of Images
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    @retry()
    def search_image(
        self,
        collection_name: str,
        image,
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
Search an image field with image using Vector Search

Vector similarity search with an image directly.

_note: image has to be stored somewhere and be provided as image_url, a url that stores the image_

For example: an image_url represents an image of a celebrity::

    "https://www.celebrity_images.com/brad_pitt.png"

    -> <Encode the image to vector> ->

    image vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}

Args:
	image_url:
		The image url of an image to encode into a vector
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
        if type(image) == str:
            if "http" in image:
                params = {
                    "username": self.username,
                    "api_key": self.api_key,
                    "collection_name": collection_name,
                    "image_url": image,
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
                    url="{}/collection/search_with_image".format(self.url),
                    json=parms
                )
                return return_curl_or_response(response, 'json', return_curl=return_curl)
        elif type(image) == bytes:
            params = {
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "image": image.decode(),
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
                url="{}/collection/search_with_image_upload".format(self.url),
                json=params
            )
            return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_image_by_upload(
        self,
        collection_name: str,
        image,
        fields: List,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector=False,
        include_count=True,
        asc=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Search an image field with uploaded image using Vector Search

Vector similarity search with an uploaded image directly.

_note: image has to be sent as a base64 encoded string_
    
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
	image:
		Image in local file path
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        with open(image, "rb") as fd:
            contents = fd.read()
        return self.search_image(
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
    def encode_image(self, collection_name: str, image, return_curl: bool=False, **kwargs):
        """
Encode image into a vector

_note: image has to be stored somewhere and be provided as image_url, a url that stores the image_

For example: an image_url represents an image of a celebrity::

    "https://www.celebrity_images.com/brad_pitt.png"

    -> <Encode the image to vector> ->

    image vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

Args:
	image:
		The image url of an image to encode into a vector
	collection_name:
		Name of Collection
"""
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "image_url": image,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/encode_image".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def encode_image_job(
        self, collection_name: str, image_field: str, refresh: bool = False, return_curl: bool=False, **kwargs
    ):
        """
Encode all images in a field into vectors

Within a collection encode the specified image field in every document into vectors.

_note: image has to be stored somewhere and be provided as image_url, a url that stores the image_

For example, an image_url field "celebrity_image" represents an image of a celebrity::

    document 1 image_url field: {"celebrity_image" : "https://www.celebrity_images.com/brad_pitt".png}

    document 2 image_url field: {"celebrity_image" : "https://www.celebrity_images.com/brad_pitt.png"}

    -> <Encode the images to vectors> ->

    document 1 image_url vector: {"celebrity_image_vector_": [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]}

    document 2 image_url vector: {"celebrity_image_vector_": [0.8364648222923279, 0.6280597448348999, 0.8112713694572449, 0.36105549335479736, 0.005313870031386614 ...]}

Args:
	image_field:
		The image field to encode into vectors
	refresh:
		Whether to refresh the whole collection and re-encode all to vectors
	collection_name:
		Name of Collection
"""
        params= {
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "image_field": image_field,
                "refresh": refresh,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/jobs/encode_image_field".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)
