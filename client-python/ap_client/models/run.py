# coding: utf-8

"""
Agent Protocol

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 0.1.6
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from ap_client.models.run_status import RunStatus
from typing import Set
from typing_extensions import Self


class Run(BaseModel):
    """
    Run
    """  # noqa: E501

    run_id: StrictStr = Field(description="The ID of the run.")
    thread_id: StrictStr = Field(description="The ID of the thread.")
    agent_id: Optional[StrictStr] = Field(
        default=None, description="The agent that was used for this run."
    )
    created_at: datetime = Field(description="The time the run was created.")
    updated_at: datetime = Field(description="The last time the run was updated.")
    status: RunStatus = Field(description="The status of the run.")
    metadata: Dict[str, Any] = Field(description="The run metadata.")
    kwargs: Dict[str, Any]
    multitask_strategy: StrictStr = Field(
        description="Strategy to handle concurrent runs on the same thread."
    )
    __properties: ClassVar[List[str]] = [
        "run_id",
        "thread_id",
        "agent_id",
        "created_at",
        "updated_at",
        "status",
        "metadata",
        "kwargs",
        "multitask_strategy",
    ]

    @field_validator("multitask_strategy")
    def multitask_strategy_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(["reject", "rollback", "interrupt", "enqueue"]):
            raise ValueError(
                "must be one of enum values ('reject', 'rollback', 'interrupt', 'enqueue')"
            )
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Run from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Run from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "run_id": obj.get("run_id"),
                "thread_id": obj.get("thread_id"),
                "agent_id": obj.get("agent_id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "status": obj.get("status"),
                "metadata": obj.get("metadata"),
                "kwargs": obj.get("kwargs"),
                "multitask_strategy": obj.get("multitask_strategy"),
            }
        )
        return _obj
