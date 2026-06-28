import os
import json
import pytest

# FastAPI may not be installed in the execution environment. If it's missing,
# skip the entire test module rather than raising an import error.
fastapi = pytest.importorskip("fastapi")
from fastapi import FastAPI
from fastapi.testclient import TestClient
