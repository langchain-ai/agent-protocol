# ap_client.RunsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_and_stream_run**](RunsApi.md#create_and_stream_run) | **POST** /runs/stream | Create Run, Stream Output
[**create_and_wait_run**](RunsApi.md#create_and_wait_run) | **POST** /runs/wait | Create Run, Wait for Output


# **create_and_stream_run**
> str create_and_stream_run(run_stream)

Create Run, Stream Output

Create a run in a new thread, stream the output.

### Example


```python
import ap_client
from ap_client.models.run_stream import RunStream
from ap_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ap_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with ap_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ap_client.RunsApi(api_client)
    run_stream = ap_client.RunStream() # RunStream | 

    try:
        # Create Run, Stream Output
        api_response = api_instance.create_and_stream_run(run_stream)
        print("The response of RunsApi->create_and_stream_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RunsApi->create_and_stream_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_stream** | [**RunStream**](RunStream.md)|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Not Found |  -  |
**409** | Conflict |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_and_wait_run**
> RunWaitResponse create_and_wait_run(run_create)

Create Run, Wait for Output

Create a run in a new thread. Wait for the final output and then return it.

### Example


```python
import ap_client
from ap_client.models.run_create import RunCreate
from ap_client.models.run_wait_response import RunWaitResponse
from ap_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ap_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with ap_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ap_client.RunsApi(api_client)
    run_create = ap_client.RunCreate() # RunCreate | 

    try:
        # Create Run, Wait for Output
        api_response = api_instance.create_and_wait_run(run_create)
        print("The response of RunsApi->create_and_wait_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RunsApi->create_and_wait_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_create** | [**RunCreate**](RunCreate.md)|  | 

### Return type

[**RunWaitResponse**](RunWaitResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Not Found |  -  |
**409** | Conflict |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

