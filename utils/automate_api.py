if __name__=="__main__":
    import os
    from vectorai.api import ViAPIClient
    from openapi_to_sdk.sdk_automation import PythonSDKBuilder
    sdk = PythonSDKBuilder(
        url="https://api.vctr.ai",
        inherited_properties=['username', 'api_key'],
        decorators=[
            'retry()', 
            "return_curl_or_response('json')"],
    )
    sdk.to_python_file(
        class_name="ViAPIClient", 
        filename='vectorai/api/api.py',
        import_strings=['import requests', 'from vectorai.api.utils import retry, return_curl_or_response'], 
        internal_functions=[
            "list_collections",
            "create_collection",
            "search"
        ],
        include_response_parsing=False
    )
    vi = ViAPIClient(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    print(vi._list_collections())