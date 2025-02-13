#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from fbpcs.private_computation.entity.private_computation_instance import (
    PrivateComputationGameType,
    PrivateComputationInstance,
    PrivateComputationRole,
)
from fbpcs.private_computation.entity.private_computation_status import (
    PrivateComputationInstanceStatus,
)
from fbpcs.private_computation.service.input_data_validation_stage_service import (
    InputDataValidationStageService,
)


class TestInputDataValidationStageService(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._pc_instance = PrivateComputationInstance(
            instance_id="123",
            role=PrivateComputationRole.PARTNER,
            instances=[],
            status=PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_STARTED,
            status_update_ts=1600000000,
            num_pid_containers=1,
            num_mpc_containers=1,
            num_files_per_mpc_container=1,
            game_type=PrivateComputationGameType.LIFT,
            input_path="456",
            output_dir="789",
        )

    @patch("fbpcp.service.storage.StorageService")
    async def test_run_async_changes_the_status_when_the_file_exists(
        self, mock_storage_service
    ) -> None:
        pc_instance = self._pc_instance
        mock_storage_service.file_exists.return_value = True
        stage_service = InputDataValidationStageService(mock_storage_service)

        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_STARTED,
        )

        await stage_service.run_async(pc_instance)
        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_COMPLETED,
        )

    @patch("fbpcp.service.storage.StorageService")
    async def test_run_async_fails_when_the_file_does_not_exist(
        self, mock_storage_service
    ) -> None:
        pc_instance = self._pc_instance
        mock_storage_service.file_exists.return_value = False
        stage_service = InputDataValidationStageService(mock_storage_service)

        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_STARTED,
        )

        await stage_service.run_async(pc_instance)
        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_FAILED,
        )

    @patch("fbpcp.service.storage.StorageService")
    async def test_run_async_fails_when_a_value_error_occurs(
        self, mock_storage_service
    ) -> None:
        pc_instance = self._pc_instance
        mock_storage_service.file_exists.side_effect = ValueError("test error")
        stage_service = InputDataValidationStageService(mock_storage_service)

        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_STARTED,
        )

        await stage_service.run_async(pc_instance)
        self.assertEqual(
            pc_instance.status,
            PrivateComputationInstanceStatus.INPUT_DATA_VALIDATION_FAILED,
        )
