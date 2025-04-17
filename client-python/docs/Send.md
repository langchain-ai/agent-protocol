# Send

A message or packet to send to a specific node in the graph.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | **str** | The node to send the message to. | 
**input** | **object** | The message to send. | 

## Example

```python
from ap_client.models.send import Send

# TODO update the JSON string below
json = "{}"
# create an instance of Send from a JSON string
send_instance = Send.from_json(json)
# print the JSON string representation of the object
print(Send.to_json())

# convert the object into a dict
send_dict = send_instance.to_dict()
# create an instance of Send from a dict
send_from_dict = Send.from_dict(send_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


