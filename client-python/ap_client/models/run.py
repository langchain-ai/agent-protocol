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
from typing_extensions import Annotated
from ap_client.models.config import Config
from ap_client.models.input import Input
from ap_client.models.message import Message
from ap_client.models.stream_mode import StreamMode
from typing import Set
from typing_extensions import Self


class Run(BaseModel):
    """
    Run
    """  # noqa: E501

    thread_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the thread to run. If not provided, creates a stateless run. 'thread_id' is ignored unless Threads stage is implemented.",
    )
    agent_id: Optional[StrictStr] = Field(
        default=None,
        description="The agent ID to run. If not provided will use the default agent for this service. 'agent_id' is ignored unless Agents stage is implemented.",
    )
    input: Optional[Input] = None
    messages: Optional[List[Message]] = Field(
        default=None, description="The messages to pass an input to the agent."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata to assign to the run."
    )
    config: Optional[Config] = None
    webhook: Optional[
        Annotated[str, Field(min_length=1, strict=True, max_length=65536)]
    ] = Field(default=None, description="Webhook to call after run finishes.")
    stream_mode: Optional[StreamMode] = None
    on_completion: Optional[StrictStr] = Field(
        default=None,
        description="Whether to delete or keep the thread when run completes. Must be one of 'delete' or 'keep'. Defaults to 'delete' when thread_id not provided, otherwise 'keep'.",
    )
    on_disconnect: Optional[StrictStr] = Field(
        default="cancel",
        description="The disconnect mode to use. Must be one of 'cancel' or 'continue'.",
    )
    if_not_exists: Optional[StrictStr] = Field(
        default="reject",
        description="How to handle missing thread. Must be either 'reject' (raise error if missing), or 'create' (create new thread).",
    )
    run_id: StrictStr = Field(description="The ID of the run.")
    created_at: datetime = Field(description="The time the run was created.")
    updated_at: datetime = Field(description="The last time the run was updated.")
    __properties: ClassVar[List[str]] = [
        "thread_id",
        "agent_id",
        "input",
        "messages",
        "metadata",
        "config",
        "webhook",
        "stream_mode",
        "on_completion",
        "on_disconnect",
        "if_not_exists",
        "run_id",
        "created_at",
        "updated_at",
    ]

    @field_validator("on_completion")
    def on_completion_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["delete", "keep"]):
            raise ValueError("must be one of enum values ('delete', 'keep')")
        return value

    @field_validator("on_disconnect")
    def on_disconnect_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["cancel", "continue"]):
            raise ValueError("must be one of enum values ('cancel', 'continue')")
        return value

    @field_validator("if_not_exists")
    def if_not_exists_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["create", "reject"]):
            raise ValueError("must be one of enum values ('create', 'reject')")
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
        # override the default output from pydantic by calling `to_dict()` of input
        if self.input:
            _dict["input"] = self.input.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in messages (list)
        _items = []
        if self.messages:
            for _item_messages in self.messages:
                if _item_messages:
                    _items.append(_item_messages.to_dict())
            _dict["messages"] = _items
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict["config"] = self.config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of stream_mode
        if self.stream_mode:
            _dict["stream_mode"] = self.stream_mode.to_dict()
        # set to None if input (nullable) is None
        # and model_fields_set contains the field
        if self.input is None and "input" in self.model_fields_set:
            _dict["input"] = None

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
                "thread_id": obj.get("thread_id"),
                "agent_id": obj.get("agent_id"),
                "input": Input.from_dict(obj["input"])
                if obj.get("input") is not None
                else None,
                "messages": [Message.from_dict(_item) for _item in obj["messages"]]
                if obj.get("messages") is not None
                else None,
                "metadata": obj.get("metadata"),
                "config": Config.from_dict(obj["config"])
                if obj.get("config") is not None
                else None,
                "webhook": obj.get("webhook"),
                "stream_mode": StreamMode.from_dict(obj["stream_mode"])
                if obj.get("stream_mode") is not None
                else None,
                "on_completion": obj.get("on_completion"),
                "on_disconnect": obj.get("on_disconnect")
                if obj.get("on_disconnect") is not None
                else "cancel",
                "if_not_exists": obj.get("if_not_exists")
                if obj.get("if_not_exists") is not None
                else "reject",
                "run_id": obj.get("run_id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
            }
        )
        return _obj
