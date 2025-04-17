# RunUpdateCommand


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**update** | [**Update**](Update.md) |  | [optional] 
**resume** | [**Resume**](Resume.md) |  | [optional] 
**goto** | [**Goto**](Goto.md) |  | [optional] 

## Example

```python
from ap_client.models.run_update_command import RunUpdateCommand

# TODO update the JSON string below
json = "{}"
# create an instance of RunUpdateCommand from a JSON string
run_update_command_instance = RunUpdateCommand.from_json(json)
# print the JSON string representation of the object
print(RunUpdateCommand.to_json())

# convert the object into a dict
run_update_command_dict = run_update_command_instance.to_dict()
# create an instance of RunUpdateCommand from a dict
run_update_command_from_dict = RunUpdateCommand.from_dict(run_update_command_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


