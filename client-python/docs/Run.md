# Run


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**thread_id** | **str** | The ID of the thread to run. If not provided, creates a stateless run. &#39;thread_id&#39; is ignored unless Threads stage is implemented. | [optional] 
**agent_id** | **str** | The agent ID to run. If not provided will use the default agent for this service. &#39;agent_id&#39; is ignored unless Agents stage is implemented. | [optional] 
**input** | [**Input**](Input.md) |  | [optional] 
**messages** | [**List[Message]**](Message.md) | The messages to pass an input to the agent. | [optional] 
**metadata** | **object** | Metadata to assign to the run. | [optional] 
**config** | [**Config**](Config.md) |  | [optional] 
**webhook** | **str** | Webhook to call after run finishes. | [optional] 
**on_completion** | **str** | Whether to delete or keep the thread when run completes. Must be one of &#39;delete&#39; or &#39;keep&#39;. Defaults to &#39;delete&#39; when thread_id not provided, otherwise &#39;keep&#39;. | [optional] 
**on_disconnect** | **str** | The disconnect mode to use. Must be one of &#39;cancel&#39; or &#39;continue&#39;. | [optional] [default to 'cancel']
**if_not_exists** | **str** | How to handle missing thread. Must be either &#39;reject&#39; (raise error if missing), or &#39;create&#39; (create new thread). | [optional] [default to 'reject']
**stream_mode** | [**StreamMode1**](StreamMode1.md) |  | [optional] 
**run_id** | **str** | The ID of the run. | 
**created_at** | **datetime** | The time the run was created. | 
**updated_at** | **datetime** | The last time the run was updated. | 
**status** | [**RunStatus**](RunStatus.md) |  | 

## Example

```python
from ap_client.models.run import Run

# TODO update the JSON string below
json = "{}"
# create an instance of Run from a JSON string
run_instance = Run.from_json(json)
# print the JSON string representation of the object
print(Run.to_json())

# convert the object into a dict
run_dict = run_instance.to_dict()
# create an instance of Run from a dict
run_from_dict = Run.from_dict(run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


