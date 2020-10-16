
Vector AI - Essentials
^^^^^^^^^^^^^^^^^^^^^^

Vector AI is built to store vectors alongside documents (text/audio/images/videos). 
It is designed to be a light-weight library to create, manipulate, search and analyse vectors to power machine 
learning applications such as semantic search, recommendations, etc.

Important Terminologies
=======================
- **Vectors** (aka. embeddings, 1D arrays)

- **Models/Encoders** (aka. Embedders) Turns data into vectors e.g. Word2Vec turns words into vectors

- **Vector Similarity Search** (aka. Nearest Neighbor Search, Distance Search)

- **Collection** (aka. Index, Table) ~ a collection is made up of multiple documents

- **Documents** (aka. Json, Item, Dictionary, Row) ~ a document can contain vector + other important information


.. code-block:: RST
    e.g.
    {
        "_id" : "1", 
        "description_vector__ ": [...], 
        "description" : "This is a great idea"
    }

Some important information: for predefined vectors use the suffix "_vector_" in the name like "description_vector_", for ids to do quick key value lookup use the name "_id"

Documents in Vector AI
========================

Documents (dictionaries) consists of fields (dictionary keys) and values.

1. Vector AI is document orientated (dictionaries/jsons) which means you can have nested fields. This means that you have documents such as:

    .. code-block:: RST

        document_example = {
            "car": {
                "wheels":
                    {
                        "number": 4
                    }
            }
        }

then running vi_client.get_field("car.wheels.number") will return 4

2. When uploading documents into VectorAi, it will infer the schema from the first document being inserted.

You are able to navigate the documents within the fields by using the functions below, allowing you to navigate through 
nested documents if the fields are separated by .'s.

.. code-block:: python

    vi_client.set_field(field, doc, value)
    vi_client.get_field(field, doc)
    vi_client.set_field_across_documents(field, docs, values)
    vi_client.get_field_across_documents(field, docs)

Models With Vector AI
========================

Vector AI has deployed models that we've handpicked and tuned to work nicely out of the box on most problems. 
These models, however, may be changed over time. When they do we make sure that 
previous models are still deployed and can be used.
To prototype something quickly we highly recommend using these deployed models.


**If you are working on a problem that requires highly customised or finetuned models, reach out to us 
for enterprise services where we can fine tune these models for your use case or feel free to build your own.**

Currently, our deployed models are:
    * ViText2Vec - our text to vector model
    * ViImage2Vec - our image to vector model
    * ViAudio2Vec - our audio to vector model
    * dimensionality_reduction_job - perform dimensionality reduction on your vectors
    * clustering_job - perform clustering on your vectors
    * advanced_cluster_job - perform clustering with advanced options on your vectors
