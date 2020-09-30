"""Various utilites for analytics
"""
from typing import List, Dict, Any, Tuple
from ..read import ViReadClient


class ViAnalyticsUtils(ViReadClient):
    def sort_documents_by_value(self, documents: List[Dict[str, Any]], sort_by: str, reverse=False):
        """
        Sort documents based on a specific value

        Args:
            documents:
                list of documents.
            sort_by:
                the field by which to sort
        
        Example:
            >>> from vectorai.analytics import ViAnalyticsUtils
            >>> ViAnalyticsUtils.sort_documents_by_values(documents, sort_by='random_field.here')
        """

        docs = sorted(
            documents,
            key=lambda i: self.get_field(sort_by, i),
            reverse=reverse,
        )
        return docs


class MeanDict:
    """
    A special kind of dictionary that lets you take the average of floats as you add them to a dictionary.
    
    Example:
        >>> from vectorai.analytics.utils import MeanDict
        >>> mean_dict = MeanDict()
        >>> mean_dict['a'] = 12
        >>> mean_dict['a'] = 24
        >>> print(mean_dict['a'])
        18
    """

    def __init__(self):
        self._dict = {}
        self._counter = {}

    def __setitem__(self, k: str, item: float):
        """
        What number to add to an item in the meandict.

        Args:
            k:
                Key for mean dict
            item:
                the item value for the key.
        
        Example:
            >>> from vectorai.analytics.utils import MeanDict
            >>> mean_dict = MeanDict()
            >>> mean_dict['a'] = 12
            >>> mean_dict['a'] = 24
            >>> print(mean_dict['a'])
        """
        if k not in self._dict.keys():
            self._dict[k] = item
            self._counter[k] = 1
        else:
            total = self._dict[k] * self._counter[k]
            self._counter[k] = self._counter[k] + 1
            self._dict[k] = (total + item) / self._counter[k]

    def __getitem__(self, k):
        """
        Return the value from the meandict
        Args:
            k:
                Key for mean dict

        Example:
            >>> from vectorai.analytics.utils import MeanDict
            >>> mean_dict = MeanDict()
            >>> mean_dict['a'] = 12
            >>> mean_dict['a'] = 24
            >>> print(mean_dict['a'])
        """
        return self._dict[k]

    def get_x_y(self) -> Tuple[List, List]:
        """
        Return the keys and values as 2 lists.

        Example:
            >>> from vectorai.analytics.utils import MeanDict
            >>> mean_dict = MeanDict()
            >>> mean_dict['a'] = 12
            >>> mean_dict['a'] = 24
            >>> mean_dict.get_x_y()
            ['a'], [18]
        """
        return_dict = {
            k: v for k, v in sorted(self._dict.items(), key=lambda item: item[1])
        }
        return list(return_dict.keys()), list(return_dict.values())
