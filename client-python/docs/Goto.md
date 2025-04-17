# Goto

Name of the node(s) to navigate to next or node(s) to be executed with a provided input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | **str** | The node to send the message to. | 
**input** | **object** | The message to send. | 

## Example

```python
from ap_client.models.goto import Goto

# TODO update the JSON string below
json = "{}"
# create an instance of Goto from a JSON string
goto_instance = Goto.from_json(json)
# print the JSON string representation of the object
print(Goto.to_json())

# convert the object into a dict
goto_dict = goto_instance.to_dict()
# create an instance of Goto from a dict
goto_from_dict = Goto.from_dict(goto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


