# CloudBees Feature Management provider for OpenFeature

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![a](https://img.shields.io/badge/slack-%40cncf%2Fopenfeature-brightgreen?style=flat&logo=slack)](https://cloud-native.slack.com/archives/C0344AANLA1)
[![OpenFeature Specification](https://img.shields.io/static/v1?label=OpenFeature%20Specification&message=v0.3.0&color=red)](https://github.com/open-feature/spec/tree/v0.3.0)
[![OpenFeature SDK](https://img.shields.io/static/v1?label=OpenFeature%20SDK&message=v1.0.0&color=green)](https://github.com/open-feature/python-sdk/)
[![CloudBees Rox SDK](https://img.shields.io/static/v1?label=Rox%20SDK&message=v5.0.10&color=green)](https://pypi.org/project/rox/)

This is the [CloudBees](https://www.cloudbees.com/products/feature-management) provider implementation for [OpenFeature](https://openfeature.dev/) for the [Python SDK](https://github.com/open-feature/python-sdk).

OpenFeature provides a vendor-agnostic abstraction layer on Feature Flag management.

This provider allows the use of CloudBees Feature Management as a backend for Feature Flag configurations.

## Requirements
- python 3.8 or higher

## Installation

### Add it to your build

```bash
pip install cloudbees-openfeature-provider-python
```

### Confirm peer dependencies are installed
```bash
pip install openfeature-sdk
```


### Configuration

Follow the instructions on the [Python SDK project](https://github.com/open-feature/python-sdk) for how to use the Python SDK.

You can configure the CloudBees provider by doing the following:

```python
from openfeature import api
from cloudbees.provider import CloudbeesProvider

appKey = 'INSERT_APP_KEY_HERE'
provider = CloudbeesProvider(appKey)
api.set_provider(provider)
client = api.get_client()
value = client.get_boolean_value("enabled-new-feature", False)
```