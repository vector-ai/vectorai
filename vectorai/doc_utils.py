"""Document-Specific Utilities
"""
from typing import List, Dict, Any
from .errors import MissingFieldError

class DocUtilsMixin:
    @classmethod
    def get_field(self, field: str, doc: Dict):
        """
            For nested dictionaries, tries to access a field.
            e.g. 
            field = kfc.item
            This should return "chickens" based on doc below.
            {
                "kfc": {
                    "item": "chickens"
                }
            }

            Args:
                field:
                    Field of a document.
                doc: 
                    document

            Example:
                >>> from vectorai.client import ViClient
                >>> vi_client = ViClient(username, api_key, vectorai_url)
                >>> sample_document = {'kfc': {'item': 'chicken'}}
                >>> vi_client.get_field('kfc.item', sample_document) == 'chickens'
        """
        d = doc
        for f in field.split("."):
            try:
                d = d[f]
            except KeyError:
                try:
                    return doc[field]
                except KeyError:
                    raise MissingFieldError("Document is missing " + field)
            except TypeError:
                if self._is_string_integer(f):
                    # Get the Get the chunk document out.
                    d = d[int(f)]
                else:
                    raise MissingFieldError("Document is missing " + f + ' of ' + field)
        return d
    
    @classmethod
    def _is_string_integer(cls, x):
        """Test if a string is numeric
        """
        try:
            int(x)
            return True
        except:
            return False


    @classmethod
    def get_fields(self, fields: List[str], doc: Dict) -> List[Any]:
        """
            For nested dictionaries, tries to access a field.
            e.g. 
            field = kfc.item
            This should return "chickens" based on doc below.
            {
                "kfc": {
                    "item": "chickens"
                }
            }

            Args:
                fields:
                    List of fields of a document.
                doc: 
                    document

            Example:
                >>> from vectorai.client import ViClient
                >>> vi_client = ViClient(username, api_key, vectorai_url)
                >>> sample_document = {'kfc': {'item': 'chicken'}}
                >>> vi_client.get_field('kfc.item', sample_document) == 'chickens'
        """
        return [self.get_field(f, doc) for f in fields]

    def get_field_across_documents(self, field: str, docs: List[Dict]):
        """
            For nested dictionaries, tries to access a field.
            e.g. 
            field = kfc.item
            This should return "chickens" based on doc below.
            {
                "kfc": {
                    "item": "chickens"
                }
            }

            Args:
                fields:
                    List of fields of a document.
                doc: 
                    document

            Example:
                >>> from vectorai.client import ViClient
                >>> vi_client = ViClient(username, api_key, vectorai_url)
                >>> documents = vi_client.create_sample_documents(10)
                >>> vi_client.get_field_across_documents('size.cm', documents)
                # returns 10 values in the nested dictionary
        """
        return [self.get_field(field, doc) for doc in docs]

    @staticmethod
    def set_field(
        field: str, doc: Dict, value: Any, handle_if_missing=True
    ):
        """
        For nested dictionaries, tries to write to the respective field.
        If you toggle off handle_if_misisng, then it will output errors if the field is 
        not found.
        e.g.
        field = kfc.item
        value = "fried wings"
        This should then create the following entries if they dont exist:
        {
            "kfc": {
                "item": "fried wings"
            }
        }

        Args:
            field:
                Field of the document to write.
            doc: 
                Python dictionary
            value:
                Value to write

        Example:

            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> sample_document = {'kfc': {'item': ''}}
            >>> vi_client.set_field('kfc.item', sample_document, 'chickens')
        """
        fields = field.split(".")
        # Assign a pointer.
        d = doc
        for i, f in enumerate(fields):
            # Assign the value if this is the last entry e.g. stores.fastfood.kfc.item will be item 
            if i == len(fields) - 1:
                d[f] = value
            else:
                if f in d.keys():
                    d = d[f]
                else:
                    d.update({f: {}})
    
    def set_field_across_documents(
        self, field: str, values: List[Any], docs: List[Dict]
    ):
        """
        For multiple documents, set the right fields.
        e.g.
        field = kfc.item
        value = "fried wings"
        This should then create the following entries if they dont exist:
        {
            "kfc": {
                "item": "fried wings"
            }
        }

        Args:
            field:
                Field of the document to write.
            doc: 
                Python dictionary
            value:
                Value to write

        Example:

            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> sample_document = {'kfc': {'item': ''}}
            >>> vi_client.set_fields('kfc.item', sample_document, 'chickens')
        """
        assert len(values) == len(docs), "Assert that the number of values " + \
            "equates to the number of documents"
        for i, value in enumerate(values):
            self.set_field(field, docs[i], value)

    @staticmethod
    def is_field(field: str, doc: Dict) -> bool:
        """
        For nested dictionaries, tries to access a field.
        e.g. 
        field = kfc.item
        This should return "chickens" based on doc below.
        {
            "kfc": {
                "item": "chickens"
            }
        }

        Args:
            collection_name:
                Name of collection.
            job_id: 
                ID of the job.
            job_name:
                Name of the job.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> sample_document = {'kfc': {'item': 'chicken'}}
            >>> vi_client.is_field('kfc.item', sample_document) == True
        """
        d = doc
        for f in field.split("."):
            try:
                d = d[f]
            except:
                return False
        return True
