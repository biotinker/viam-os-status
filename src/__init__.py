"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .osstats import OSSTATS

Registry.register_resource_creator(Sensor.SUBTYPE, OSSTATS.MODEL, ResourceCreatorRegistration(OSSTATS.new, OSSTATS.validate))
