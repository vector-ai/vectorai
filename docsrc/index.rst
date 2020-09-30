.. vectorai documentation master file, created by
   sphinx-quickstart on Sat Sep 12 14:33:11 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Vector AI's documentation!
====================================

.. image:: https://getvectorai.com/assets/logo-with-text.png
  :width: 600
  :alt: Vector AI

Vector AI aims to store vectors alongside documents (text/audio/images/videos).
It is designed to be a light-weight library to create/manipulate/search and analyse the 
underlying vectors to power machine learning applications such as semantic
search, recommendations, etc.

- Our REST API documentation can be found here: https://api.vctr.ai/documentation   
- Our discord can be found here: https://discord.gg/CbwUxyD

Features: 

   - **Multimedia Data Vectorisation**: Image2Vec, Audio2Vec, etc (Any data can be turned into vectors through machine learning) 
   - **Vector Similarity Search**: Enable searching of vectors and rich multimedia with vector similarity search. The backbone of many popular A.I use cases like reverse image search, recommendations, personalisation, etc. 
   - **Vector Operations**: Flexible search with out of the box operations on vectors. e.g. mean, median, sum, etc. 
   - **Aggregation**: All the traditional aggregation you'd expect. e.g. group by mean, pivot tables, etc 
   - **Clustering**: Interpret your vectors and data by allocating them to buckets and get statistics about these different buckets based on data you provide. 
   - **Vector Analytics**: Get better understanding of your vectors by using out-of-the-box practical vector analytics, giving you better understanding of the quality of your vectors.

Why Vector AI compared to other Nearest Neighbor implementations?
-------------------------------------------------------------------

-  **Production Ready**: Our API is fully managed and can scale to power
   hundreds of millions of searches a day. Even at millions of searches
   it is blazing fast through edge caching, gpus and software
   optisation. So you never have to worry about scaling your
   infastructure as your use case scales.
-  **Richer understanding of your vectors and their properties**: Our
   library is designed to allow people to not just designed to obtain
   nearest neighbors but to actually use in production-ready search
   systems - allowing users to analyse, iterate, improve and
   productionise their vectors the moment they are added to the index.
-  **Simple to use. Quick to get started.**: One of our core design
   principles is that we focus a lot on how people can get started on
   using Vector AI as quickly as possible, while having a tonne of
   functionality and customisability options.
-  **Framework agnostic**: We are never going to force a specific
   framework on Vector AI. If you have a framework of choice, you can use
   it - as long as your documents are JSON-serializable!
-  **Store vector data with ease**: The document-orientated nature for
   Vector AI allows users to label, filter search and understand their
   vectors as much as possible. We think that other libraries that
   simply provide a nearest-neighbor implementation do not have as rich
   functionality.


How to install
###############

To install vectorai, run the following

.. code-block:: RST

    pip install vectorai


To install from source, clone the repository and then run

.. code-block:: RST

    cd vectorai 
    pip install -e . 

Schema
########

We have a very simple schema to follow to allow you to optimise functionality with vector search:

.. list-table:: Schema Rules
   :widths: 25 75
   :header-rows: 1

   * - Field
     - Purpose

   * - _id
     - ID of the document. These need to be unique for the document.

   * - _vector_
     - These are required to label the vectors for vector search.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   intro
   quickstart

.. toctree::
   :caption: Guides
   
   industry_ecommerce
   vector_analytics_example
   custom_encodings_example

.. toctree::
   :caption: Case Studies
   
   industry_nba_players

.. toctree::
   :caption: Frequently Asked Questions

   FAQ


.. toctree::
    :maxdepth: 2
    :caption: Documentation
    
    client
    read
    write
    cluster
    array_dict_vectorizer
    dimensionality_reduction
    vector_search
    image
    text
    audio
    analytics


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
