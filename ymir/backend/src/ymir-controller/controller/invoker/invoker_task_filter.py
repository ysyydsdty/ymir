from typing import Dict

from common_utils.percent_log_util import LogState
from controller.invoker.invoker_cmd_filter import FilterBranchInvoker
from controller.invoker.invoker_cmd_merge import MergeInvoker
from controller.invoker.invoker_task_base import TaskBaseInvoker
from controller.utils import invoker_call, utils, tasks_util
from id_definition.error_codes import CTLResponseCode
from proto import backend_pb2


class TaskFilterInvoker(TaskBaseInvoker):
    @classmethod
    def task_invoke(cls, sandbox_root: str, repo_root: str, assets_config: Dict[str, str], working_dir: str,
                    task_monitor_file: str, request: backend_pb2.GeneralReq) -> backend_pb2.GeneralResp:
        # Use sub_task_id 0 as end of task.
        filter_request = request.req_create_task.filter

        if not filter_request.in_dataset_ids:
            return utils.make_general_response(CTLResponseCode.ARG_VALIDATION_FAILED, "invalid_data_ids")

        in_dataset_ids = list(filter_request.in_dataset_ids)
        sub_task_id_1 = utils.sub_task_id(request.task_id, 1)
        merge_response = invoker_call.make_invoker_cmd_call(invoker=MergeInvoker,
                                                            sandbox_root=sandbox_root,
                                                            req_type=backend_pb2.CMD_MERGE,
                                                            user_id=request.user_id,
                                                            repo_id=request.repo_id,
                                                            task_id=sub_task_id_1,
                                                            his_task_id=in_dataset_ids[0],
                                                            dst_task_id=request.task_id,
                                                            in_dataset_ids=in_dataset_ids,
                                                            merge_strategy=request.merge_strategy)
        if merge_response.code != CTLResponseCode.CTR_OK:
            tasks_util.write_task_progress(monitor_file=task_monitor_file,
                                           tid=request.task_id,
                                           percent=1.0,
                                           state=LogState.ERROR,
                                           msg=merge_response.message)
            return merge_response

        sub_task_id_0 = utils.sub_task_id(request.task_id, 0)
        filter_response = invoker_call.make_invoker_cmd_call(invoker=FilterBranchInvoker,
                                                             sandbox_root=sandbox_root,
                                                             req_type=backend_pb2.CMD_FILTER,
                                                             user_id=request.user_id,
                                                             repo_id=request.repo_id,
                                                             task_id=sub_task_id_0,
                                                             his_task_id=sub_task_id_1,
                                                             dst_task_id=request.task_id,
                                                             in_dataset_ids=[request.task_id],
                                                             in_class_ids=filter_request.in_class_ids,
                                                             ex_class_ids=filter_request.ex_class_ids)

        if filter_response.code == CTLResponseCode.CTR_OK:
            tasks_util.write_task_progress(monitor_file=task_monitor_file,
                                           tid=request.task_id,
                                           percent=1.0,
                                           state=LogState.DONE)
        else:
            tasks_util.write_task_progress(monitor_file=task_monitor_file,
                                           tid=request.task_id,
                                           percent=1.0,
                                           state=LogState.ERROR,
                                           msg=filter_response.message)

        return filter_response
