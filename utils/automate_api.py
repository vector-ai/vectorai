from openapi_to_sdk.sdk_automation import PythonSDKBuilder
sdk = PythonSDKBuilder(
    url="https://api.vctr.ai",
    inherited_properties=['username', 'api_key'],
    decorators=['retry()'],
)
sdk.to_python_file(
    class_name="ViAPIClient", 
    filename='vectorai/api/api.py',
    import_strings=['import requests', 'from vectorai.api.utils import retry'], 
    internal_functions=[
        "list_collections",
        "create_collection",
        "search"
    ]
)
