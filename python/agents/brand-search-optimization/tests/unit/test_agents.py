# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Agent initialization tests."""

from google.adk.apps import App
from google.adk.runners import InMemoryRunner

from brand_search_optimization import root_agent


def test_inmemory_runner_uses_app_wrapper() -> None:
    app = App(name="brand_search_optimization", root_agent=root_agent)
    runner = InMemoryRunner(app=app)
    assert runner.app is not None
    assert runner.app.name == "brand_search_optimization"
