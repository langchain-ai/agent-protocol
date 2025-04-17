# RunUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**command** | [**RunUpdateCommand**](RunUpdateCommand.md) |  | [optional] 

## Example

```python
from ap_client.models.run_update import RunUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of RunUpdate from a JSON string
run_update_instance = RunUpdate.from_json(json)
# print the JSON string representation of the object
print(RunUpdate.to_json())

# convert the object into a dict
run_update_dict = run_update_instance.to_dict()
# create an instance of RunUpdate from a dict
run_update_from_dict = RunUpdate.from_dict(run_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


