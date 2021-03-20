"""Miscellaneous functions for the client.
"""
import numpy as np
import pandas as pd
import itertools
import inspect
import types
import random
import warnings
from typing import List, Any, Dict, Union
from functools import wraps, partial

class UtilsMixin:
    """Various utilties
    """
    def generate_vector(self, vector_length: int, num_of_constant_values: int=0):
        """
        Generate a random vector based on length

        Args:
            vector_length:
                Length of a vector.
            num_of_constant_values
                The number of constant values in a vector. This is to help make the
                vectors more similar

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.generate_vector(vector_length=20)
        """
        return np.random.rand(vector_length - num_of_constant_values).tolist() + [0.5] * num_of_constant_values

    @staticmethod
    def results_to_df(data):
        """
        Used for converting json responses of search results, etc
        Args:
            data:
                data returned from search, retrieve_documents, etc
        """
        if "results" in data:
            return pd.DataFrame(data["results"])
        elif "documents" in data:
            return pd.DataFrame(data["documents"])
        elif type(data) == dict:
            return pd.DataFrame([data])
        elif type(data) == list:
            return pd.DataFrame(data)
        else:
            print("missing field")

    def clean_results(self, results):
        if 'results' in results:
            return results['results']
        elif 'documents' in results:
            return results['documents']
        return results

    def results_pretty(self, results: Union[Dict, List], field: str):
        """
        Make results pretty in a Pandas Dataframe.
        Args:
            results:
                JSON of results
            field:
                Field to prettify results.

        Example:
            >>> result = vi_client.search(collection_name, text_encoder.encode('No more tissue paper'),
                field='OriginalTweet_vector_', page_size=5)
            >>> vi_client.results_pretty(result, 'OriginalTweet')
        """
        pd.set_option('display.max_colwidth', 10000)
        if 'results' in results.keys():
            results = results['results']
        return pd.DataFrame({self.get_field(field, x) for x in results}, columns=[field])

    @staticmethod
    def flatten_list(list_of_lists: List[List]):
        """
        Flatten a nested list

        Args:
            list_of_lists:
                A list of lists to flatten to make into 1 list.

        Example:
            >>> from vectorai.client import ViClient
            >>> ViClient.flatten_list([[0, 1], [2, 3]])
        """
        return list(itertools.chain.from_iterable(list_of_lists))

    @staticmethod
    def rename(object: Any, value: str):
        """
            Rename an object.
            Args:
                object:
                    Any Python instance/variable
                value:
                    Name of new instance

            Example:
                >>> from vectorai.client import ViClient
                >>> ViClient.rename(model, 'new_name')
        """
        object.__name__ = value

    @staticmethod
    def set_name(object: Any, value: str):
        """
            Rename an object.
            Args:
                object:
                    Any Python object

            Example:
                >>> from vectorai.client import ViClient
                >>> ViClient.set_name(model, 'new_name')
        """
        object.__name__ = value

    @staticmethod
    def get_name(object):
        """
            Get the name attribute of an object.
            Args:
                object:
                    Any Python object
            Returns:
                object name:
                    Name of object

            Example:
                >>> get_name(try_it)
        """
        return object.__name__

    @staticmethod
    def is_in_ipython():
        """
        Determines if current code is executed within an ipython session.
        """
        is_in_ipython = False
        # Check if the runtime is within an interactive environment, i.e., ipython.
        try:
            from IPython import get_ipython  # pylint: disable=import-error
            if get_ipython():
                is_in_ipython = True
        except ImportError:
            pass  # If dependencies are not available, then not interactive for sure.
        return is_in_ipython

    def is_in_notebook(self) -> bool:
        """
        Determines if current code is executed from an ipython notebook.
        """
        is_in_notebook = False
        if self.is_in_ipython():
            # The import and usage must be valid under the execution path.
            from IPython import get_ipython
            if 'IPKernelApp' in get_ipython().config:
                is_in_notebook = True
        return is_in_notebook

    def progress_bar(self, documents: List, total: int=None, show_progress_bar=True):
        """
        Returns a progress bar. depending on if notebook is available or not.

        Args:
            documents:
                A list of documents (Python dictionaries)

            Total:
                Length of documents/size of update

        Returns:
            Tqdm Progress Bar

        Example:
            for i in UtilsMixin.progress_bar(documents):
                ...
        """
        if not show_progress_bar:
            return documents

        if total is None:
            total = len(documents)

        if self.is_in_notebook():
            from tqdm.notebook import tqdm
            return tqdm(documents, total=total)
        else:
            try:
                from tqdm import tqdm
                return tqdm(documents, total=total)
            except:
                return documents

    @classmethod
    def create_sample_document(self, document_id: str=None, include_chunks=False):
        """
        Create sample document.
        Args:
            Document_id: the index of the document
        """
        rand_index = np.random.randint(0, 30)
        if include_chunks:
            sample_document =  {
                'color': [random.choice(['red', 'blue', 'orange', 'green'])],
                'number': [random.choice(list(range(10)))],
                'country': random.choice(['Italy', 'Australia', 'Denmark', 'Brazil', 'France']),
                'color_vector_': np.random.rand(1, 30).tolist()[0],
                'color_2_vector_': np.random.rand(1, 30).tolist()[0],
                'size': {
                    'feet': list(range(1, 31))[rand_index],
                    'cm': (np.array(range(30)) * 30.48).tolist()[rand_index]
                },
                'chunk':[
                    {
                        'color_chunkvector_': np.random.rand(1, 30).tolist()[0],
                        'color': random.choice(['red', 'blue', 'orange', 'green'])
                    },
                    {
                        'color_2_chunkvector_': np.random.rand(1, 30).tolist()[0],
                        'color': random.choice(['red', 'blue', 'orange', 'green'])
                    }
                ]
            }
        else:
            sample_document =  {
                'color': [random.choice(['red', 'blue', 'orange', 'green'])],
                'number': [random.choice(list(range(10)))],
                'country': random.choice(['Italy', 'Australia', 'Denmark', 'Brazil', 'France']),
                'color_vector_': np.random.rand(1, 30).tolist()[0],
                'color_2_vector_': np.random.rand(1, 30).tolist()[0],
                'size': {
                    'feet': list(range(1, 31))[rand_index],
                    'cm': (np.array(range(30)) * 30.48).tolist()[rand_index]
                }
            }
        if document_id is not None:
            sample_document.update({'_id': str(document_id)})
        return sample_document

    @classmethod
    def create_sample_documents(self, num_of_documents: int, include_chunks=False):
        """
        Create sample documents.
        Args:
            num_of_documents:
                Create sample documents.
        """
        return [self.create_sample_document(i, include_chunks=include_chunks) for i in range(num_of_documents)]

    @staticmethod
    def convert_concat_list_to_html(list_input):
        string = ''
        for x in list_input:
            string += '<div class="column">' + x + '</div>'
        return string

    def render_chunk(self, row, render_func):
        concat_images = [render_func(x) for x in row]
        return UtilsMixin.convert_concat_list_to_html(concat_images)

    def render_image_chunk(self, row, image_width=120):
        render_image_chunks = partial(self.render_image_in_html, image_width=image_width)
        return self.render_chunk(row, render_image_chunks)

    def render_audio_chunk(self, row):
        return self.render_chunk(row, self.render_audio_in_html)

    def show_df(self, df: pd.DataFrame,
    image_fields: List[str]=[], audio_fields: List[str]=[], chunk_image_fields: List[str]=[],
    chunk_audio_fields: List[str]=[], image_width: int=60,
    include_vector: bool=False, return_html: bool=False):
        """
            Shows a dataframe with the images and audio included inside the dataframe.
            Args:
                df:
                    Pandas DataFrame
                image_fields:
                    List of fields with the images
                audio_fields:
                    List of fields for the audio
                nrows:
                    Number of rows to preview
                image_width:
                    The width of the images
                include_vector:
                    If True, includes the vector fields
        """
        render_image_with_width = partial(self.render_image_in_html, image_width=image_width)
        formatters = {image:render_image_with_width for image in image_fields}
        formatters.update({audio: self.render_audio_in_html for audio in audio_fields})
        formatters.update({chunk_image: self.render_image_chunk for chunk_image in chunk_image_fields})
        formatters.update({chunk_audio: self.render_audio_chunk for chunk_audio in chunk_audio_fields})
        if not include_vector:
            cols = [x for x in list(df.columns) if '_vector_' not in x]
            df = df[cols]
        try:
            if return_html:
                return df.to_html(escape=False, formatters=formatters)
            from IPython.core.display import HTML
            return HTML(df.to_html(escape=False ,formatters=formatters))
        except ImportError:
            return df

    def render_image_in_html(self, path, image_width) -> str:
        return '<img src="'+ path + f'" width="{image_width}" >'

    def render_audio_in_html(self, path) -> str:
        return f"<audio controls><source src='{x}' type='audio/{self.get_audio_format(x)}'></audio>"

    def show_styler(self, df,
    image_fields: List[str]=[], audio_fields: List[str]=[], image_width: int=60,
    return_as_html=False):
        """
            Shows a dataframe with the images and audio included inside the dataframe.
            Args:
                df:
                    Pandas DataFrame
                image_fields:
                    List of fields with the images
                audio_fields:
                    List of fields for the audio
                nrows:
                    Number of rows to preview
                image_width:
                    The width of the images
        """
        render_image_with_width = partial(self.render_image_in_html, image_width=image_width)
        formatters = {image:render_image_with_width for image in image_fields}
        formatters.update({audio: self.render_audio_in_html for audio in audio_fields})

        try:
            if return_as_html:
                return df.format(formatters).render()
            return df.format(formatters)
        except ImportError:
            return df

    def get_audio_format(self, string):
        if '.wav' in string:
            return 'wav'
        if '.mp3' in string:
            return 'mpeg'
        if '.ogg' in string:
            return 'ogg'
        warnings.warn("Unable to detect audio format. Must be either wav/mpeg/ogg.")
        return ''

    def unnest_json(self, json_data, schema):
        unnested_json = {}
        for k in schema:
            unnested_json[k] = self.get_field_across_documents(k, json_data)
        return unnested_json

    def show_json(self, json: dict, selected_fields: List[str]=None, image_fields: List[str]=[],
        audio_fields: List[str]=[], chunk_image_fields: List[str]=[], chunk_audio_fields: List[str]=[],
        nrows: int=None, image_width: int=60, include_vector=False):
        """
            Shows the JSON with the audio and images inside a dataframe for quicker analysis.
            Args:
                json:
                    Dictionary
                selected_fields:
                    List of fields to see in the dictionary
                image_fields:
                    List of fields with the images
                audio_fields:
                    List of fields for the audio
                chunk_image_fields:
                    List of image fields that should be chunked
                chunk_audio_fields:
                    List of audio fields that should be chunked
                nrows:
                    Number of rows to preview
                image_width:
                    The width of the images
                include_vector:
                    Include the vector fields when showing JSON
        """
        if selected_fields is None:
            json = self.unnest_json(self.clean_results(json), schema=image_fields + audio_fields)
        else:
            json = self.unnest_json(self.clean_results(json), schema=image_fields + audio_fields + selected_fields)
        if nrows is not None:
            json = json[:nrows]
        if selected_fields is None and len(image_fields) == 0 and len(audio_fields) == 0:
            return self.show_df(pd.DataFrame(json), image_fields=image_fields, audio_fields=audio_fields,
            chunk_image_fields=chunk_image_fields, chunk_audio_fields=chunk_audio_fields,
            image_width=image_width, include_vector=include_vector)
        return self.show_df(pd.DataFrame(json),
            image_fields=image_fields, audio_fields=audio_fields,
            chunk_image_fields=chunk_image_fields, chunk_audio_fields=chunk_audio_fields,
            image_width=image_width, include_vector=include_vector)

    def show_chunk_json(self, json: dict, selected_fields: List[str]=None, image_fields: List[str]=[],
    audio_fields: List[str]=[], nrows: int=5, image_width: int=60, include_vector=False):
        """Show results if the documents are chunked.
        For images, concatenates the chunk images into the same numpy array
        For text, puts them one after the other with smaller index.
        No Audio chunking for now.
        """
        raise NotImplementedError

def get_random_int(low=0, high=9999):
    """
        Return a random int from 0 to 9999
        Args:
            low:
                Lower boundary
            High:
                Higher boundary
    """
    return random.randint(low, high)

def decorate_functions_by_argument(function_decorator, argument):
    """
        Decorate a function with an argument
        Args:
            function_decorator:
                A decorator function in Python
            argument:
                The Python argument that has to be altered
        Returns:
            A decorator
    """
    def decorator(cls):
        for name, obj in inspect.getmembers(cls):
            if isinstance(obj, (types.MethodType, types.FunctionType)):
                if obj.__name__ == "__init__":
                    continue
                if argument in inspect.signature(obj).parameters.keys():
                    try:
                        obj = obj.__func__  # unwrap Python 2 unbound method
                    except AttributeError:
                        pass  # not needed in Python 3
                    setattr(cls, name, function_decorator(obj, getattr(cls, argument)))
        return cls
    return decorator

def get_stack_level() -> int:
    """
        Return the stack level in Python.
    """
    return len(inspect.stack(0))

def set_default_collection(func, collection_name):
    """
        Set the default collection in functions
        Args:
            Func:
                The function which contains the collection_name argument
            Collection Name:
                The name of the collection
        Returns:
            Decorated function for default collection
    """
    @wraps(func)
    def wrapper(*args, **kw):
        # Set a stack level so this only effects highest level functions
        # and not internal functions that use collection_name
        if 'collection_name' in inspect.getfullargspec(func).args \
            and getattr(args[0], 'decorator_called') is False:
                setattr(args[0], 'decorator_called', True)
                setattr(args[0], 'decorator_call_stack_level',
                get_stack_level())
                num_of_args = len(inspect.getfullargspec(func).args)
                collection_name = getattr(args[0], 'collection_name')
                if collection_name in kw.keys():
                    collection_name = kw.pop('collection_name')
                # from functools import partial
                # new_func = partial(func, collection_name=collection_name)
                # print(args)
                # res = new_func(*args, **kw)
                # try:
                res = func(args[0], collection_name=collection_name, *args[1:], **kw)
                # except TypeError:
                #     res = func(args[0], collection_name=collection_name, *args[1:], **kw)
            # res = func(args[0], collection_name, *args[1:], **kw)
            # res = func(args[0], kw['collection_name'], *args[1:])
            # except:
            #     if len(args) == len(getfullargspec(func).args):
            #         res = func(*args)
            #     else:
            #         try:
            #             res = func(*args, **kw)
            #         except TypeError:
            #             kw.pop('collection_name')
            #             res = func(*args, **kw)
        else:
            try:
                res = func(*args, **kw)
            except TypeError:
                collection_name = getattr(args[0], 'collection_name')
                res = func(args[0], collection_name, *args[1:], **kw)

        if get_stack_level() == getattr(args[0], 'decorator_call_stack_level') and \
            getattr(args[0], 'decorator_called'):
            setattr(args[0], 'decorator_called', False)
        return res
    return wrapper
