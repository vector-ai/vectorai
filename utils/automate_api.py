if __name__=="__main__":
    import os
    from openapi_to_sdk.sdk_automation import PythonSDKBuilder
    sdk = PythonSDKBuilder(
        url='https://vecdb-aueast-api.azurewebsites.net',
        inherited_properties=['username', 'api_key'],
        decorators=[
            'retry()', 
            "return_curl_or_response('json')"],
        override_param_defaults={'min_score': None, 'cursor': None, 'sort': True},
        internal_functions=[
            "list_collections",
            "create_collection",
            "search",
            "delete_collection",
            "edit_document",
            "create_collection_from_document"
        ],
    )
    sdk.to_python_file(
        class_name="ViAPIClient", 
        filename='vectorai/api/api.py',
        import_strings=['import requests', 'from vectorai.api.utils import retry, return_curl_or_response'], 
        include_response_parsing=False,
    )

    from vectorai.api import ViAPIClient
    vi = ViAPIClient(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    print(vi._list_collections())
