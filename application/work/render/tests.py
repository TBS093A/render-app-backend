from django.test import TestCase

# import pytest
from channels.testing import HttpCommunicator
from work.render.consumers import (
    RenderSingleImageConsumer,
    RenderSingleSetConsumer,
    RenderAllConsumer,
)


# @pytest.mark.asyncio
# async def testSocket_1():
#     pass
