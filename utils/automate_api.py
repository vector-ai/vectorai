if __name__=="__main__":
    import os
    from openapi_to_sdk.sdk_automation import PythonSDKBuilder

    url = "https://vectorai-production-api.azurewebsites.net"
    sdk = PythonSDKBuilder(
        url=url,
        inherited_properties=['username', 'api_key', 'url'],
        decorators=[
            'retry()',
            "return_curl_or_response('json')"],
        override_param_defaults=dict(
            min_score=None,
            cursor=None,
            url=url,
            sort_by_created_at_date=False,
        ),
        internal_functions=[
            "list_collections",
            "create_collection",
            "search",
            "delete_collection",
            "create_collection_from_document"
        ],
    )
    sdk.to_python_file(
        class_name="_ViAPIClient",
        filename='vectorai/api/api.py',
        import_strings=['import requests', 'from vectorai.api.utils import retry, return_curl_or_response'],
        include_response_parsing=False,
    )

    from vectorai.api.api import _ViAPIClient
    vi = _ViAPIClient(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'], url=url)
    print(vi._list_collections())

