#!/usr/bin/python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = ""

RETURN = ""

# pylint: disable=wrong-import-position
import traceback

from ansible.module_utils.yc import YC  # pylint: disable=E0611, E0401
from google.protobuf.json_format import MessageToDict
from grpc import StatusCode
from grpc._channel import _InactiveRpcError
from yandex.cloud.compute.v1.disk_service_pb2 import GetDiskRequest
from yandex.cloud.compute.v1.disk_service_pb2_grpc import DiskServiceStub

RESOURCE = ["clouds", "folders"]

def cloud_argument_spec():
    return dict(
        id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        type=dict(choices=RESOURCE, required=True),
    )


class YccCloud(YC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_info(self):
        response = dict()
        type = self.params.get("type")
        id = self.params.get("id", None)
        name = None
        cloud = None
        objects = None
        if id is None:
            name = self.params.get("name", None)
        if type == "clouds":
            objects = self._list_clouds_by(id=id, name=name)
        elif type == "folders":
            if id is None:
                cloud = self.params.get("cloud", None)
            objects = self._list_folders_by(id=id, cloud=cloud, name=name)
        if objects is None:
            response["msg"] = "Empty"
            return response
        response = objects
        return response


def main():
    argument_spec = cloud_argument_spec()
    module = YccCloud(argument_spec=argument_spec)
    response = dict()
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications

    try:
        if module.params.get("type"):
            response = module.get_info()
        else:
            raise Exception("Resource type should be provided.")

    except Exception as error:  # pylint: disable=broad-except
        if hasattr(error, "details"):
            response["msg"] = getattr(error, "details")()
            response["exception"] = traceback.format_exc()
        else:
            response["msg"] = "Error during runtime ocurred"
            response["exception"] = traceback.format_exc()
        module.fail_json(**response)

    module.exit_json(**response)


if __name__ == "__main__":
    main()
