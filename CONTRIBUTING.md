# Contributing to Agent Protocol

👋 Hi there! Thank you for being interested in contributing to Agent Protocol.
As an open source project in a rapidly developing field, we are extremely open
to contributions, whether it be in the form of a new feature, improved infra, or better documentation.

To contribute to this project, please follow a ["fork and pull request"](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow. Please do not try to push directly to this repo unless you are a maintainer.

## 🗺️ Contributing Guidelines

Whenever a change is made to the protocol, please make sure to update the OpenAPI spec in the `openapi.json` file. This file is used to generate the API documentation, and is the single source of truth for the protocol.

Please run `make gen-server` in the `tooling` directory to re-generate the contents of the `server` directory. This will re-generate the Python server stubs from the OpenAPI spec.
