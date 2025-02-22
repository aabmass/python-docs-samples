#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa


# This file is automatically generated. Please do not modify it directly.
# Find the relevant recipe file in the samples/recipes or samples/ingredients
# directory and apply your changes there.


# [START compute_hyperdisk_pool_create]
from __future__ import annotations

import sys
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    Waits for the extended (long-running) operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def create_hyperdisk_storage_pool(
    project_id: str,
    zone: str,
    storage_pool_name: str,
    storage_pool_type: str = "hyperdisk-balanced",
) -> compute_v1.StoragePool:
    """Creates a hyperdisk storage pool in the specified project and zone.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the storage pool will be created.
        storage_pool_name (str): The name of the storage pool.
        storage_pool_type (str, optional): The type of the storage pool. Defaults to "hyperdisk-balanced".
    Returns:
        compute_v1.StoragePool: The created storage pool.
    """

    pool = compute_v1.StoragePool()
    pool.name = storage_pool_name
    pool.zone = zone
    pool.storage_pool_type = (
        f"projects/{project_id}/zones/{zone}/storagePoolTypes/{storage_pool_type}"
    )
    pool.capacity_provisioning_type = "ADVANCED"
    pool.pool_provisioned_capacity_gb = 10240
    pool.performance_provisioning_type = "STANDARD"

    # Relevant if the storage pool type is hyperdisk-balanced.
    pool.pool_provisioned_iops = 10000
    pool.pool_provisioned_throughput = 1024

    pool_client = compute_v1.StoragePoolsClient()
    operation = pool_client.insert(
        project=project_id, zone=zone, storage_pool_resource=pool
    )
    wait_for_extended_operation(operation, "disk creation")

    new_pool = pool_client.get(project=project_id, zone=zone, storage_pool=pool.name)
    print(new_pool.pool_provisioned_iops)
    print(new_pool.pool_provisioned_throughput)
    print(new_pool.capacity_provisioning_type)
    # Example response:
    # 10000
    # 1024
    # ADVANCED

    return new_pool


# [END compute_hyperdisk_pool_create]
