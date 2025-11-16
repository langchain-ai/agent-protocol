# ap_client.RunsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_and_stream_run**](RunsApi.md#create_and_stream_run) | **POST** /runs/stream | Create Run, Stream Output
[**create_and_wait_run**](RunsApi.md#create_and_wait_run) | **POST** /runs/wait | Create Run, Wait for Output
[**resume_and_stream_run**](RunsApi.md#resume_and_stream_run) | **PATCH** /runs/resume/stream | Resume Run and Stream Output
[**resume_and_wait_run**](RunsApi.md#resume_and_wait_run) | **PATCH** /runs/resume/wait | Resume Run and Wait
[**resume_run**](RunsApi.md#resume_run) | **PATCH** /runs/resume | Resume Run (start execution from interrupted thread)


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

# **resume_and_stream_run**
> str resume_and_stream_run(run_resume_stream)

Resume Run and Stream Output

Resume a thread that is in an interrupted (suspended) state and stream its output. Convenience equivalent to PATCH /runs/resume followed by GET /runs/{run_id}/stream.

### Example


```python
import ap_client
from ap_client.models.run_resume_stream import RunResumeStream
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
    run_resume_stream = ap_client.RunResumeStream() # RunResumeStream | 

    try:
        # Resume Run and Stream Output
        api_response = api_instance.resume_and_stream_run(run_resume_stream)
        print("The response of RunsApi->resume_and_stream_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RunsApi->resume_and_stream_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_resume_stream** | [**RunResumeStream**](RunResumeStream.md)|  | 

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

# **resume_and_wait_run**
> RunWaitResponse resume_and_wait_run(run_resume)

Resume Run and Wait

Resume a thread that is in an interrupted state and wait for its completion. Equivalent to PATCH /runs/resume followed by GET /runs/{run_id}/wait.

### Example


```python
import ap_client
from ap_client.models.run_resume import RunResume
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
    run_resume = ap_client.RunResume() # RunResume | 

    try:
        # Resume Run and Wait
        api_response = api_instance.resume_and_wait_run(run_resume)
        print("The response of RunsApi->resume_and_wait_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RunsApi->resume_and_wait_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_resume** | [**RunResume**](RunResume.md)|  | 

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

# **resume_run**
> Run resume_run(run_resume)

Resume Run (start execution from interrupted thread)

Resume a thread that is in an interrupted (suspended) state. Thread ID is required. Returns the updated Run object (typically queued or in_progress).

### Example


```python
import ap_client
from ap_client.models.run import Run
from ap_client.models.run_resume import RunResume
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
    run_resume = ap_client.RunResume() # RunResume | 

    try:
        # Resume Run (start execution from interrupted thread)
        api_response = api_instance.resume_run(run_resume)
        print("The response of RunsApi->resume_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RunsApi->resume_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_resume** | [**RunResume**](RunResume.md)|  | 

### Return type

[**Run**](Run.md)

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

