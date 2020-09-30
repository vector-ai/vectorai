"""This will store the embedding functions in a way that makes sense.
"""
from typing import List, Dict, Callable
from warnings import warn
import json
import gc
import shelve
import os
from pathlib import Path
from appdirs import *
from ..errors import APIError


class EmbedMixin:
    """Nested shelf class
    """

    def __init__(self, appname="vectorai_embed_functions", appauthor="onsearch"):
        """Saving the path of the vectorai
        """
        self.save_dir = user_cache_dir(appname, appauthor)

    def save_function(self, index_name: str, vector_field: str, embed_func: Callable):
        """This adds an embed function to the function.

        E.g.
        def embed_func(x):
            return transformer.encode(x)
        client.add_embed_function(index_name='test-index', vector_field='search_vector_', embed_func=embed_func)
        """
        embed_func_input = {vector_field: embed_func}
        inserted = False
        index_path = Path(os.path.join(self.save_dir, index_name))

        if not index_path.parent.exists():
            index_path.parent.mkdir()
        if not index_path.exists():
            index_path.mkdir()
        with shelve.open(str(index_path) + ".dat") as db:
            db[index_name] = embed_func

    def load_function(self, index_name: str, vector_field: str):
        """Load function from the database.
        """
        index_path = os.path.join(self.save_dir, index_name)
        with shelve.open(str(index_path) + ".dat") as db:
            func = db[vector_field]
        return func
