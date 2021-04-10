<p align="center">
    <a href="https://getvectorai.com">
        <img src="https://getvectorai.com/assets/logo-with-text-v2.png" width="400"></img>
    </a>
</p>
<br>
<p align="center">
    <a href="https://github.com/vector-ai/vectorai">
        <img alt="Release" src="https://img.shields.io/github/v/tag/vector-ai/vectorai?label=release">
    </a>
    <a href="https://getvectorai.com">
        <img alt="Website" src="https://img.shields.io/website?up_message=online&label=website&url=https%3A%2F%2Fgetvectorai.com">
    </a>
    <a href="https://vector-ai.github.io/vectorai">
        <img alt="Documentation" src="https://img.shields.io/website?up_message=online&label=documentation&url=https%3A%2F%2Fvector-ai.github.io%2Fvectorai">
    </a>
    <a href="https://discord.gg/CbwUxyD">
        <img alt="Discord" src="https://img.shields.io/badge/discord-join-blue.svg">
    </a>
</p>

<hr>

<h3 align="center">
Vector AI is a framework designed to make the process of building production grade vector based applications as quickly and easily as possible. Create, store, manipulate, search and analyse vectors alongside json documents to power applications such as neural search, semantic search, personalised recommendations recommendations etc.
</h3>

- Visit our website and sign up for an api-key: https://getvectorai.com
- For Python Documentation: https://vector-ai.github.io/vectorai
- For REST API Documentation: https://api.vctr.ai/documentation
- Join our discord: https://discord.gg/CbwUxyD
- For a more gentle introduction comparing our features, read https://getvectorai.com/production-ready-search-in-5-minutes/

<hr>

## Features
- **Multimedia Data Vectorisation**: Image2Vec, Audio2Vec, etc (Any data can be turned into vectors through machine learning)
- **Document Orientated Store**: Store your vectors alongside documents without having to do a db lookup for metadata about the vectors.
- **Vector Similarity Search**: Enable searching of vectors and rich multimedia with vector similarity search. The backbone of many popular A.I use cases like reverse image search, recommendations, personalisation, etc.
- **Hybrid Search**: There are scenarios where vector search is not as effective as traditional search, e.g. searching for skus. Vector AI lets you combine vector search with all the features of traditional search such as filtering, fuzzy search, keyword matching to create an even more powerful search.
- **Multi-Model Weighted Search**: Our Vector search is highly customisable and you can peform searches with multiple vectors from multiple models and give them different weightings.
- **Vector Operations**: Flexible search with out of the box operations on vectors. e.g. mean, median, sum, etc.
- **Aggregation**: All the traditional aggregation you'd expect. e.g. group by mean, pivot tables, etc
- **Clustering**: Interpret your vectors and data by allocating them to buckets and get statistics about these different buckets based on data you provide.
- **Vector Analytics**: Get better understanding of your vectors by using out-of-the-box practical vector analytics, giving you better understanding of the quality of your vectors.

<hr>

## Quick Terminologies

- Models/Encoders (aka. Embedders) ~ Turns data into vectors e.g. Word2Vec turns words into vector
- Vector Similarity Search (aka. Nearest Neighbor Search, Distance Search)
- Collection (aka. Index, Table) ~ a collection is made up of multiple documents
- Documents (aka. Json, Item, Dictionary, Row) ~ a document can contain vectors, text and links to videos/images/audio.

<hr>

## QuickStart

Install via pip! Compatible with any OS.

```
pip install vectorai
```

If you require the nightly version due to on-going improvements, you can install the nightly version using: 
```
pip install vectorai-nightly
```

Note: while the nightly version will still pass automated tests, it may not be stable.

Check out our quickstart notebook on how to make a text/image/audio search engine in 5 minutes: [quickstart.ipynb](examples/quickstart.ipynb)

```
from vectorai import ViClient, request_api_key

api_key = request_api_key(username=<username>, email=<email>, description=<description>, referral_code="github_referred")

vi_client = ViClient(username=username, api_key=api_key)

from vectorai.models.deployed import ViText2Vec
text_encoder = ViText2Vec(username, api_key)

documents = [
    {
        '_id': 0,
        'color': 'red'
    },
    {
        '_id': 1,
        'color': 'blue'
    }
]

# Insert the data
vi_client.insert_documents('test-collection', documents, models={'color': text_encoder.encode})

# Search the data
vi_client.search('test-collection', text_encoder.encode('maroon'), 'color_vector_', page_size=2)

# Get Recommendations
vi_client.search_by_id('test-collection', '1', 'color_vector_', page_size=2)
```

<hr>

## Access Powerful Vector Analytics 

Vector AI has powerful visualisations to allow you to analyse your vectors as easily as possible - in 1 line of code.

```
vi_client.plot_dimensionality_reduced_vectors(documents, 
    point_label='title', 
    dim_reduction_field='_dr_ivis', 
    cluster_field='centroid_title', cluster_label='centroid_title')

```

![View Dimensionality-Reduced Vectors](https://getvectorai.com/assets/gif/dr_example.gif)

```
vi_client.plot_2d_cosine_similarity(
    documents,
    documents[0:2],
    vector_fields=['use_vector_'],
    label='name',
    anchor_document=documents[0]
)
```

Compare vectors and their search performance on your documents easily!
![1D plot cosine simlarity](https://getvectorai.com/assets/gif/2d_cosine_similarity.gif)

<hr>

## Why Vector AI compared to other Nearest Neighbor implementations?

- **Production Ready**: Our API is fully managed and can scale to power hundreds of millions of searches a day. Even at millions of searches it is blazing fast through edge caching, GPU utilisation and software optimisation so you never have to worry about scaling your infrastructure as your use case scales.
- **Simple to use. Quick to get started.**: One of our core design principles is that we focus on how people can get started on using Vector AI as quickly as possible, whilst ensuring there is still a tonne of functionality and customisability options.
- **Richer understanding of your vectors and their properties**: Our library is designed to allow people to do more than just obtain nearest neighbors, but to actually experiment, analyse, interpret and improve on them the moment the data added to the index.
- **Store vector data with ease**: The document-orientated nature for Vector AI allows users to label, filter search and understand their vectors as much as possible.
- **Real time access to data**: Vector AI data is accessible in real time, as soon as the data is inserted it is searchable straight away. No need to wait hours to build an index.
- **Framework agnostic**: We are never going to force a specific framework on Vector AI. If you have a framework of choice, you can use it - as long as your documents are JSON-serializable! 

<hr>

### Using VectorHub Models

[VectorHub](https://hub.vctr.ai) is Vector AI's main model repository. Models from VectorHub are built with scikit-learn interfaces and all have examples of Vector AI integration. If you are looking to experiment with new off-the-shelf models, we recommend giving VectorHub models a go - all of them have been tested on Colab and are able to be used in as little as 3 lines of code! 

### Schema Rules for documents (BYO Vectors and IDs)

Ensure that any vector fields contain a '\_vector\_' in its name and that any ID fields have the name '\_id'.

For example:
```
example_item = {
    '_id': 'James',
    'skills_vector_': [0.123, 0.456, 0.789, 0.987, 0.654, 0.321]
}
```

The following will not be recognised as ID columns or vector columns.

```
example_item = {
    'name_id': 'James',
    'skillsvector_': [0.123, 0.456, 0.789, 0.987, 0.654, 0.321]
}
```

<hr>

## How does this differ from the VectorAI API? 

The Python SDK is designed to provide a way for Pythonistas to unlock the power of VectorAI in as few lines as code as possible. It exposes all the elements of an API through our open-sourced automation tool and is the main way our data scientists and engineers interact with the VectorAI engine for quick prototyping before developers utilise API requests. 

**Note**: The VectorAI SDK is built on the development server which can sometimes cause errors. However, this is important to ensure that users are able to access the most cutting-edge features as required. If you run into such issues, we recommend creating a GitHub Issue if it is non-urgent, but feel free to ping the Discord channel for more urgent enquiries.

<hr>

## Building Products with Vector AI
Creating a multi-language AI fashion assistant: https://fashionfiesta.me | [Blog](https://getvectorai.com/how-we-built-a-vector-powered-outfit-recommender/)

![Demo](https://getvectorai.com/assets/gif/fashion-fiesta-demo.gif)

Do share with us any blogs or websites you create with Vector AI!
