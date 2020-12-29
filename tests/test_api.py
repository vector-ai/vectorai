import numpy as np
import random
import datetime

def test_get_collectin_list(test_client):
    response = test_client.list_collections()
    assert isinstance(response, list)


# #Write

def test_delete_collection(test_client, test_collection_name):
    response = test_client.delete_collection(test_collection_name)
    assert response.get('status') != 'error'


def test_create_collection(test_client, test_collection_name):
    test_client.create_collection(test_collection_name)


def test_create_collection_from_document(test_client, test_collection_name):
    test_client.delete_collection(test_collection_name)
    response = test_client.create_collection_from_document(test_collection_name, {
        'name': "iPhone 11 128GB Black",
        '_id': "IPA11B",
        'price': 1279,
        "category": [
            "sci-fi",
            "thriller",
            "comedy"
        ],
        "audio": "https://play.pokemonshowdown.com/audio/cries/meowth.mp3",
        "image": "https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg",
        'videos': {
            'frame_chunkvector_': np.random.random((1, 512)).astype('float32')[0].tolist(),
        },
        "characteristics": {
            "age": 32,
            "purchases": 10,
            "visits": 24
        },
    })

    assert response.get('status') != 'error'

def test_bulk_insert_and_encode(test_client, test_collection_name):
    response = test_client.bulk_insert_and_encode(test_collection_name, docs=[{
        'name': "iPhone 11 128GB Black",
        '_id': "IPA11B",
        'price': 1279,
        "category": [
            "sci-fi",
            "thriller",
            "comedy"
        ],
        "audio": "https://play.pokemonshowdown.com/audio/cries/meowth.mp3",
        "image": "https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg",
        'videos': {
            'frame_chunkvector_': np.random.random((1, 512)).astype('float32')[0].tolist(),
        },
        "characteristics": {
            "age": 32,
            "purchases": 10,
            "visits": 24
        },
    }], models={
        "name": "text",
    })

    print('temp',response)

    assert len(response['failed_document_ids']) >= 0


def test_bulk_insert(test_client, test_collection_name):
    response = test_client.bulk_insert(test_collection_name, [{
        'name': "iPhone 11 128GB Black",
        '_id': "IPA11B",
        'price': 1279,
        "category": [
            "sci-fi",
            "thriller",
            "comedy"
        ],
        "audio": "https://play.pokemonshowdown.com/audio/cries/meowth.mp3",
        "image": "https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg",
        'videos': {
            'frame_chunkvector_': np.random.random((1, 512)).astype('float32')[0].tolist(),
        },
        "characteristics": {
            "age": 32,
            "purchases": 10,
            "visits": 24
        },
    }])

    assert len(response['failed_document_ids']) >= 0

def test_insert(test_client, test_collection_name):
    response = test_client.insert(test_collection_name, {
        'name': "iPhone 11 128GB Black",
        '_id': "IPA11B",
        'price': 1279,
        "category": [
            "sci-fi",
            "thriller",
            "comedy"
        ],
        "audio": "https://play.pokemonshowdown.com/audio/cries/meowth.mp3",
        "image": "https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg",
        'videos': {
            'frame_chunkvector_': np.random.random((1, 512)).astype('float32')[0].tolist(),
        },
        "characteristics": {
            "age": 32,
            "purchases": 10,
            "visits": 24
        },
    })

    assert response.get('status') != 'error'

def test_edit_document(test_client, test_collection_name):
    test_client.edit_document(test_collection_name, edits={
                                         '_id': 'IPA11B', 'name': 'iphone'})


def test_publish_aggregation(test_client, test_collection_name):
    aggregation_query = {
        'groupby': [
            {"name": 'name', "field": "name",
             "agg": "category"},
        ],
        'metrics': [
            {"name": 'price',
             "field": 'price', "agg": "avg"}
        ]
    }
    response = test_client.publish_aggregation(
        test_collection_name, aggregation_query, f'aggregation_{test_collection_name}', f'aggregated_{test_collection_name}')

    assert response.get('status') != 'error'

def test_stop_aggregation(test_client, test_collection_name):
    response = test_client.stop_aggregation(
        f'aggregation_{test_collection_name}')

    assert response.get('status') == 'success'


def test_start_aggregation(test_client, test_collection_name):
    response = test_client.start_aggregation(
        f'aggregation_{test_collection_name}')
    assert response.get('status') == 'success'

def test_join_collections(test_create_collection_for_join,test_client):
    join_query = {
        "collection": 'person',
        "field|car_model": {
            "collection": 'car',
            "field|model": {},
        },
    }

    response = test_client.join_collections(join_query,'person_car_joined')

    assert isinstance(response.get('failed_document_ids'), list)


# Read

def test_collection_stats(test_client, test_collection_name):
    response = test_client.collection_stats(test_collection_name)

    assert isinstance(response['size_mb'], int)
    assert isinstance(response['number_of_documents'], int)
    assert isinstance(response['number_of_searches'], int)
    assert isinstance(response['number_of_id_lookups'], int)


def test_collection_schema(test_client, test_collection_name):
    response = test_client.collection_schema(test_collection_name)
    assert isinstance(response, dict)
    assert response.get('status') != 'error'

def test_id(test_client, test_collection_name):
    response = test_client.id(test_collection_name, 'IPA11B')
    assert isinstance(response, dict)
    assert response.get('status') != 'error'

def test_bulk_id(test_client, test_collection_name):
    response = test_client.bulk_id(
        test_collection_name, document_ids=['IPA11B'])
    assert isinstance(response['IPA11B'], dict)

def test_retrieve_documents(test_client, test_collection_name):
    response = test_client.retrieve_documents(test_collection_name)
    assert isinstance(response['cursor'], str)
    assert len(response['documents']) >= 0
    assert response['count'] >= 0

def test_random_documents(test_client, test_collection_name):
    response = test_client.random_documents(test_collection_name)
    assert len(response['documents']) >= 0

#Read

def test_id_lookup_joined(test_client, test_collection_name):
    join_query = {
        "collection": 'person',
        "field|car_model": {
            "collection": 'car',
            "field|model": {},
        },
    }
    response = test_client.id_lookup_joined(join_query, '1')
    assert isinstance(response, dict)
    assert response.get('status') != 'error'

def test_aggregate(test_client, test_collection_name):
    aggregation_query = {
        'groupby': [
            {'name': 'Name', 'field': 'name', 'agg': 'category'}
        ],
        'metrics': [
            {'name': 'Name', 'field': 'price', 'agg': 'avg'}
        ]
    }
    response = test_client.aggregate(test_collection_name, aggregation_query)
    assert len(response) >= 0

def test_facets(test_client, test_collection_name):
    response = test_client.facets(test_collection_name)
    assert len(response) >= 0
    assert isinstance(response, dict)

def test_filters(test_client, test_collection_name):
    filters = [{
        "filter_type": "contains",
        "field": "name",
        "condition": "==",
        "condition_value": "iphone"
    }]
    response = test_client.filters(test_collection_name, filters=filters)
    assert len(response['documents']) >= 0
    assert response['count'] >= 0

def test_job_status():
    pass

def test_list_jobs():
    pass

def test_bulk_missing_id(test_client, test_collection_name):
    response = test_client.bulk_missing_id(test_collection_name, ['random_id'])
    assert response[0] == 'random_id'


# Text

def test_encode_text_job(test_client, test_collection_name):
    pass

def test_search_text(test_client, test_collection_name):
    response = test_client.search_text(
        test_collection_name, 'iphone', fields=['name_vector_'])

    assert len(response['results']) >= 0

def test_encode_text(test_client, test_collection_name):
    response = test_client.encode_text(test_collection_name, 'iphone')
    assert len(response) > 0


# audio

def test_encode_audio(test_client, test_collection_name):
    response = test_client.encode_audio(
        test_collection_name, 'https://play.pokemonshowdown.com/audio/cries/meowth.mp3')

    assert len(response) >= 0


def test_encode_audio_job(test_client, test_collection_name):
    # response = test_client.encode_audio_job(test_collection_name,'audio')
    pass


def test_search_audio(test_client, test_collection_name):
    response = test_client.search_audio(
        test_collection_name, 'https://play.pokemonshowdown.com/audio/cries/meowth.mp3', fields=['audio_vector_'])

    assert len(response.get('results')) >= 0

#Array dict vectorizer

def test_encode_dictionary_field(test_client,test_collection_name):
    response = test_client.encode_dictionary_field(test_collection_name,dictionary_fields=['characteristics'])

    assert isinstance(response['failed_document_ids'], list)


def test_encode_dictionary(test_client, test_collection_name):
    response = test_client.encode_dictionary(test_collection_name, {
        "age": 32,
        "purchases": 10,
        "visits": 24
    }, 'characteristics_vector_')

    assert isinstance(response, list)


def test_search_with_dictionary(test_client, test_collection_name):
    response = test_client.search_with_dictionary(test_collection_name, {
        "age": 32,
        "purchases": 10,
        "visits": 24
    }, 'characteristics', ['characteristics_vector_'])

    assert len(response['results']) >= 0


def test_encode_array_field(test_client,test_collection_name):
    response = test_client.encode_array_field(test_collection_name,['category'])

    assert len(response.get('failed_document_ids'))>=0


def test_encode_array(test_client,test_collection_name):
    response = test_client.encode_array(test_collection_name,['thriller'],'category')

    assert isinstance(response, list)

def test_search_with_array(test_client, test_collection_name):
    response = test_client.search_with_array(
        test_collection_name, ['thriller'], 'category', ['category_vector_'])

    assert isinstance(response['results'], list)


# Image

def test_encode_image(test_client, test_collection_name):
    response = test_client.encode_image(
        test_collection_name, 'https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg')

    assert len(response) >= 0

def test_encode_image_job(test_client,test_collection_name):
    # response = test_client.encode_image_job(test_collection_name,'image')
    pass


def test_search_image(test_client, test_collection_name):
    response = test_client.search_image(
        test_collection_name, 'https://images-na.ssl-images-amazon.com/images/I/613SYKy-XPL._UX522_.jpg', ['image_vector_'])

    assert len(response['results']) >= 0


# Search

def test_search(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    response = test_client.search(
        test_collection_name, vector, ['name_vector_'])

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_hybrid_search(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    response = test_client.hybrid_search(
        test_collection_name, 'iphone', vector, fields=['name_vector_'],text_fields=['name_vector_'])

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_search_by_id(test_client, test_collection_name):
    response = test_client.search_by_id(
        test_collection_name, 'IPA11B', field='name_vector_')
    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_search_by_ids(test_client, test_collection_name):
    response = test_client.search_by_ids(test_collection_name, document_ids=[
                                         'IPA11B'], field='name_vector_')
    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_search_by_positive_negative_ids(test_client, test_collection_name):
    response = test_client.search_by_positive_negative_ids(
        collection_name=test_collection_name, positive_document_ids=['IPA11B'], negative_document_ids=['IPA11B'])

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_search_with_positive_negative_ids_as_history(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    response = test_client.search_with_positive_negative_ids_as_history(
        collection_name=test_collection_name, positive_document_ids=['IPA11B'], negative_document_ids=['IPA11B'], field='name_vector_', vector=vector)

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_advanced_search(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    multivector_query = {
        'text': {
            'vector': vector,
            'fields': ['name_vector_']
        }
    }
    response = test_client.advanced_search(
        test_collection_name, multivector_query=multivector_query)

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_advanced_hybrid_search(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    multivector_query = {
        'text': {
            'vector': vector,
            'fields': ['name_vector_']
        }
    }
    response = test_client.advanced_hybrid_search(
        test_collection_name, 'iphone', multivector_query, ['name_vector'])

    assert len(response['results']) >= 0

def test_advanced_search_by_id(test_client, test_collection_name):
    response = test_client.advanced_search_by_id(
        collection_name=test_collection_name, document_id='IPA11B', fields={'name_vector_': 1})

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_advanced_search_by_ids(test_client, test_collection_name):
    response = test_client.advanced_search_by_ids(
        collection_name=test_collection_name, document_ids={'IPA11B': 1}, fields={'name_vector_': 1})

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_advanced_search_by_positive_negative_ids(test_client, test_collection_name):
    response = test_client.advanced_search_by_positive_negative_ids(test_collection_name, positive_document_ids={
                                                                    'IPA11B': 1}, negative_document_ids={'IPA11B': 1}, fields={'name_vector_': 1})

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_advanced_search_with_positive_negative_ids_as_history(test_client, test_collection_name):
    vector = test_client.encode_text(test_collection_name, 'iphone')
    response = test_client.advanced_search_with_positive_negative_ids_as_history(
        test_collection_name, vector=vector, positive_document_ids={'IPA11B': 1}, negative_document_ids={'IPA11B': 1}, fields={'name_vector_': 1})

    assert len(response['results']) >= 0
    assert response['count'] >= 0

def test_chunk_search(test_client, test_collection_name):
    pass
    # vector = test_client.encode_text(test_collection_name, 'iphone')
    # response = test_client.chunk_search(
    #     test_collection_name, vector=vector, search_fields=['name_vector_'])

    # assert len(response['results']) >= 0
    # assert response['count'] >= 0


def test_delete_by_id(test_client,test_collection_name):
    response = test_client.delete_by_id(test_collection_name,'IPA11B')
    assert response.get('status') == 'success'