# RunResume

Payload for resuming a run from an interrupted thread. Requires an existing thread; does not create new threads.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**thread_id** | **str** | The ID of the thread to resume. Must refer to an existing thread. | 
**agent_id** | **str** | The agent ID to run. If not provided will use the agent associated with this thread (or the default agent for this service). &#39;agent_id&#39; is ignored unless Agents stage is implemented. | [optional] 
**input** | [**Input**](Input.md) |  | [optional] 
**messages** | [**List[Message]**](Message.md) | The messages to pass an input to the agent. | [optional] 
**metadata** | **object** | Metadata to assign to the run. | [optional] 
**config** | [**Config**](Config.md) |  | [optional] 
**webhook** | **str** | Webhook to call after run finishes. | [optional] 
**on_completion** | **str** | Whether to delete or keep the thread when run completes. Must be one of &#39;delete&#39; or &#39;keep&#39;. Defaults to &#39;keep&#39;. | [optional] 
**on_disconnect** | **str** | The disconnect mode to use. Must be one of &#39;cancel&#39; or &#39;continue&#39;. | [optional] [default to 'cancel']

## Example

```python
from ap_client.models.run_resume import RunResume

# TODO update the JSON string below
json = "{}"
# create an instance of RunResume from a JSON string
run_resume_instance = RunResume.from_json(json)
# print the JSON string representation of the object
print(RunResume.to_json())

# convert the object into a dict
run_resume_dict = run_resume_instance.to_dict()
# create an instance of RunResume from a dict
run_resume_from_dict = RunResume.from_dict(run_resume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


