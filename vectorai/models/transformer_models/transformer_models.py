"""Transformers integration with Vi.

Design Decisions: 
- Due to the constantly changing nature of the transformers library, we try to write code 
where we think the transformers package will change the least. 
For example - we avoid use of their AutoModel as that had changed in v3.
"""
import tensorflow as tf
from tensorflow.keras import Model
from typing import Union, List, Dict
from transformers import *
from appdirs import *
from ..base import ViText2Vec
from ...client import ViClient
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import MeanAbsoluteError
from tensorflow.keras.losses import MeanSquaredError

try:
    MODEL_CLASSES = {
        "bert": (BertModel, BertTokenizer, BertConfig, "bert-base-cased"),
        "xlnet": (XLNetModel, XLNetTokenizer, XLNetConfig, "xlnet-base-cased"),
        "xlm": (XLMModel, XLMTokenizer, XLMConfig, "xlm-mlm-en-2048"),
        "roberta": (RobertaModel, RobertaTokenizer, RobertaConfig, "roberta-base"),
        "distilbert": (
            DistilBertModel,
            DistilBertTokenizer,
            DistilBertConfig,
            "distilbert-base-cased",
        ),
        "distilroberta": (
            RobertaModel,
            RobertaTokenizer,
            RobertaConfig,
            "distilroberta-base",
        ),
    }
except:
    pass

try:
    TF_MODEL_CLASSES = {
        "bert": (TFBertModel, BertTokenizer, BertConfig, "bert-base-cased"),
        "xlnet": (TFXLNetModel, XLNetTokenizer, XLNetConfig, "xlnet-base-cased"),
        "xlm": (TFXLMModel, XLMTokenizer, XLMConfig, "xlm-mlm-en-2048"),
        "roberta": (TFRobertaModel, RobertaTokenizer, RobertaConfig, "roberta-base"),
        "distilbert": (
            TFDistilBertModel,
            DistilBertTokenizer,
            DistilBertConfig,
            "distilbert-base-cased",
        ),
        "distilroberta": (
            TFRobertaModel,
            RobertaTokenizer,
            RobertaConfig,
            "distilroberta-base",
        ),
    }
    TF_CLASSIFICATION_MODELS = {
        "bert": (TFBertForSequenceClassification),
        "xlnet": (TFXLNetForSequenceClassification),
        "xlm": (TFXLMForSequenceClassification),
        "roberta": (TFRobertaForSequenceClassification),
        "distilbert": (TFDistilBertForSequenceClassification),
        "distilroberta": (TFRobertaForSequenceClassification),
    }
except:
    pass


class Transformer2Vec(ViText2Vec):
    def __init__(
        self, model_type: str, pretrained_model_name=None, return_tensors: str = "tf", max_len=512
    ):
        """
            Load a transformer model for quick encoding.

            Args:
                model_type:
                    Model type to use. These can be bert, xlnet, xlm, roberta, distilbert or distilroberta.

            Example::
                >>> from vectorai.models import Transformer2Vec
                >>> transformer_model = Transformer2Vec('distilbert')

        """
        self.model_type = model_type
        if return_tensors not in ("torch", "tf"):
            raise ValueError("return_tensor needs to be either 'torch' or 'tf'.")
        self.return_tensors = return_tensors
        if return_tensors == "torch":
            raise NotImplementedError("Pytorch support not implemented yet.")
            (
                self.model_class,
                self.tokenizer_class,
                self.config_class,
                pretrained_default,
            ) = MODEL_CLASSES[model_type]
        elif return_tensors == "tf":
            (
                self.model_class,
                self.tokenizer_class,
                self.config_class,
                pretrained_default,
            ) = TF_MODEL_CLASSES[model_type]

        if pretrained_model_name is None:
            self.pretrained_model_name = pretrained_default

        self.config = self.config_class.from_pretrained(self.pretrained_model_name)
        # self.config.output_hidden_states = True
        self.pretrained_model = self.model_class.from_pretrained(
            self.pretrained_model_name
        )
        self.tokenizer = self.tokenizer_class.from_pretrained(
            self.pretrained_model_name
        )
        self._name = None
        self._classification_save_dir = None
        self.max_len = max_len

    @property
    def __name__(self):
        if self._name is None:
            return self.model_type + '_text'
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value

    def load_classification_model(self, classification_save_dir: str=None):
        """
        Load the classification model.

        Args:
            classification_save_dir:
                Directory from which which the model was saved. This is important
                as the model weights and config are all saved here.

        Example::
            >>> from vectorai.models import Transformer2Vec
            >>> transformer_model.load_classification_model()
        """
        print("Loading in trained model.")
        if classification_save_dir is None:
            assert hasattr(
                self, "classification_save_dir"
            ), "Missing classification save directory."
        else:
            self.classification_save_dir = classification_save_dir
        self.pretrained_model = self.model_class.from_pretrained(
            self.classification_save_dir
        )


    def encode_text(
        self,
        document: Dict = None,
        document_fields: List[str] = None,
        text: str = None,
        max_len: int=None
    ):
        """
            Encodes a text or a document when given a document field..

            Args:
                document:
                    Any Python Dictionary
                document_fields: 
                    THe key of a python dictionary
                text:
                    A string instance

            Example::
                >>> from vectorai.models import Transformer2Vec
                >>> transformer_model = Transformer2Vec("Distilbert")
                >>> transformer_model.encode_text(text="Hi!")
                >>> sample_doc = {'name': 'bert'}
                >>> transformer_model.encode_text(sample_doc, 'name')
        """
        if text is not None:
            assert document is None

        if document is not None:
            assert text is None, "You must fill in either text or document."
            assert isinstance(
                document_fields, list
            ), "Document fields should be a list."
            text = ''
            for f in document_fields:
                text = text.join(self.get_field(f, document))

        if isinstance(text, str):
            inputs = self.tokenizer.encode_plus(
                text, return_tensors="tf", truncation=True
            )
            # Take first input from output because the rest are not related to the output vector
            output = self.pretrained_model(inputs)[0]
            encoding = tf.reduce_mean(output, axis=1)
            return encoding.numpy().flatten().tolist()
        if isinstance(text, list):
            inputs = [self.tokenizer.encode_plus(x, return_tensors="tf", max_length=max_len, truncation=True) for x in text]
            output = [self.pretrained_model(input_)[0] for input_ in inputs]
            encoding = [tf.reduce_mean(output_, axis=1) for output_ in output]
            return [encoding_.numpy().flatten().tolist() for encoding_ in encoding]

    def _encode_for_classification(self, x: List[str], max_len: int=512, padding_int: int=0):
        """
        Encoding for classification. Padding is done manually as it is eroneous in Transformers.

        Args:
            x:
                Input into encode_plus
            max_len:
                Maximum length of the text
            padding_int:
                THe number that this pads up to.

        """
        vector = self.tokenizer.encode_plus(
            x, padding=True, max_length=max_len, truncation=True
        )["input_ids"]
        if len(vector) < max_len:
            vector += [padding_int] * (max_len - len(vector))
        return vector

    def run_finetuning_for_classification(
        self,
        documents: List[Dict],
        x_fields: List[str],
        y_fields: List[str],
        optimizer=None,
        loss=None,
        metric=None,
        batch_size: int = 16,
        test_size=0.2,
        epochs: int = 2,
        return_type="tf"
    ):
        """
            Run a simple classification finetuning pipeline.

            Args:
                documents:
                    A list of python dictionaries. 
                x_fields: 
                    The fields that define the x variables. These are concatenated. 
                y_fields:
                    The fields that define the y variables. If 1 , this is a classification problem 
                    but if there are multiple - this becomes a multi-label or multi-regression problem.
                optimizer:
                    Tensorflow Keras Optimizer 
                Loss: 
                    Tensorflow Keras Loss
                Metric:
                    Tensorflow Keras Metrics
                Batch Size:
                    Batch Size for the model
                Test Size:
                    The proportion of the test dataset
                Epochs:
                    The number of epochs to run finetuning on 
                Return Type:
                    Currently only supports Tensorflow return type and not Pytorch.

            Example::
                >>> from vectorai.models import Transformer2Vec
                >>> transformer_model = Transformer2Vec("distilbert")
                >>> sample_docs = [{'name': 'bert', 'age": 10}, {'name': 'elmo', 'age': 15}]
                >>> x_fields = ['name']
                >>> y_fields = ['age']
                >>> transformer_model.run_finetuning_for_classification(documents=sample_docs, x_fields=x_fields, y_fields=y_fields)
                >>> model_dir = # THe above step will output a directory. This can be changed by altering transformer_model.classification_save_dir
                >>> transformer_model.load_classification_model(model_dir)
        
        """
        self.init_tpu()
        if hasattr(self, "tpu_strategy"):
            with self.tpu_strategy.scope():
                self._run_finetuning_for_classification(
                    documents=documents,
                    x_fields=x_fields,
                    y_fields=y_fields,
                    optimizer=optimizer,
                    loss=loss,
                    metric=metric,
                    batch_size=batch_size,
                    test_size=test_size,
                    epochs=epochs,
                    return_type=return_type,
                )
        else:
            self._run_finetuning_for_classification(
                documents=documents,
                x_fields=x_fields,
                y_fields=y_fields,
                optimizer=optimizer,
                loss=loss,
                metric=metric,
                batch_size=batch_size,
                test_size=test_size,
                epochs=epochs,
                return_type=return_type,
            )

    @property
    def classification_save_dir(self):
        # Saving the model
        temp_fn = f"vectorai-trained-{self.pretrained_model_name}"
        if self._classification_save_dir is None:
            self._classification_save_dir = (
                user_cache_dir("transformers", "vectorai") + "/" + temp_fn
            )
        return self._classification_save_dir

    @classification_save_dir.setter
    def classification_save_dir(self, classification_save_dir: str):
        """
            Set the save directory for the classification model.

            Args:
                classification_save_dir:
                    Directory to save the classification model.
                
            Example::
                >>> from vectorai.models import Transformer2Vec
                >>> transformer_model = Transformer2Vec("distilbert")
                >>> transformer_model.classification_save_dir = "."
        """
        self._classification_save_dir = classification_save_dir
        print(f"Changed classification save directory to {classification_save_dir}")

    def _run_finetuning_for_classification(
        self,
        documents: List[Dict],
        x_fields: List[str],
        y_fields: List[str],
        optimizer=None,
        loss=None,
        metric=None,
        batch_size: int = 16,
        test_size=0.2,
        epochs: int = 2,
        return_type="tf",
    ):
        """
        Run a simple classification finetuning pipeline.

            Args:
                documents:
                    A list of python dictionaries. 
                x_fields: 
                    The fields that define the x variables. These are concatenated. 
                y_fields:
                    The fields that define the y variables. If 1 , this is a classification problem 
                    but if there are multiple - this becomes a multi-label or multi-regression problem.
                optimizer:
                    Tensorflow Keras Optimizer 
                Loss: 
                    Tensorflow Keras Loss
                Metric:
                    Tensorflow Keras Metrics
                Batch Size:
                    Batch Size for the model
                Test Size:
                    The proportion of the test dataset
                Epochs:
                    The number of epochs to run finetuning on 
                Return Type:
                    Currently only supports Tensorflow return type and not Pytorch.

            Example::
                >>> from vectorai.models import Transformer2Vec
                >>> transformer_model = Transformer2Vec("distilbert")
                >>> sample_docs = [{'name': 'bert', 'age": 10}, {'name': 'elmo', 'age': 15}]
                >>> x_fields = ['name']
                >>> y_fields = ['age']
                >>> transformer_model.run_finetuning_for_classification(documents=sample_docs, x_fields=x_fields, y_fields=y_fields)
                >>> model_dir = # THe above step will output a directory. This can be changed by altering transformer_model.classification_save_dir
                >>> transformer_model.load_classification_model(model_dir)
        """
        if optimizer is None:
            optimizer = Adam()
        if loss is None:
            loss = MeanSquaredError()
        if metric is None:
            metric = MeanAbsoluteError
        
        if return_type == "tf":
            classification_model = TF_CLASSIFICATION_MODELS[self.model_type]
            self.config.num_labels = len(y_fields)
            self.classification_model = classification_model.from_pretrained(
                self.pretrained_model_name, config=self.config
            )
            self.classification_model.compile(optimizer=optimizer, loss=loss)

            X = [
                ''.join(self.get_fields(
                    x_fields, document
                ))
                for document in documents
            ]
            y = [self.get_fields(y_fields, document) for document in documents]
            tokens = [self._encode_for_classification(x) for x in X]
            tokens_train, tokens_valid, y_train, y_valid = train_test_split(
                tokens, y, test_size=test_size
            )
            train_dataset = tf.data.Dataset.from_tensor_slices((tokens_train, y_train))
            valid_dataset = tf.data.Dataset.from_tensor_slices((tokens_valid, y_valid))
            history = self.classification_model.fit(
                train_dataset,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=valid_dataset
            )
            
            self.classification_model.save_pretrained(self.classification_save_dir)
            print(f"Saved model. This can be found in {self.classification_save_dir}")
        else:
            raise NotImplementedError("Have not implemented Pytorch yet.")
