# Resume

Name of the node(s) to navigate to next or node(s) to be executed with a provided input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from ap_client.models.resume import Resume

# TODO update the JSON string below
json = "{}"
# create an instance of Resume from a JSON string
resume_instance = Resume.from_json(json)
# print the JSON string representation of the object
print(Resume.to_json())

# convert the object into a dict
resume_dict = resume_instance.to_dict()
# create an instance of Resume from a dict
resume_from_dict = Resume.from_dict(resume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


