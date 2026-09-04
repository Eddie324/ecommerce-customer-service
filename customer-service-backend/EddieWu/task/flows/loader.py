from pathlib import Path
from typing import Any

import yaml

from EddieWu.task.flows.flows import FlowList, FlowSlot, Flow
from EddieWu.task.flows.steps import FlowStep, CollectionFlowStep


class FlowLoader:

    def load_multi_yaml(self, paths: list[Path]) -> FlowList:
        """
        FlowList:既有user_flows中的流程又有system_flows中的流程
        Args:
            paths:

        Returns:

        """
        final_flows: list[Flow] = []
        final_slots: dict[str, FlowSlot] = {}
        for path in paths:
            single_flow_list = self._load_single_yaml(path)
            final_flows.extend(single_flow_list.flows)
            final_slots.update(single_flow_list.slots)
        return FlowList(flows=final_flows, slots=final_slots)

    def _load_single_yaml(self, path: Path) -> FlowList:
        """
        职责：加载单个YAML文件
        Args:
            path:

        Returns:

        """

        # 1. 利用pyyaml加载yaml文件转成字典对象
        with  open(path, 'r', encoding='utf-8') as f:
            yaml_dict: dict[str, Any] = yaml.safe_load(f.read())
        # 2. 加载slots
        loaded_slots = self._load_slots(yaml_dict.get('slots', {}))

        # 3. 加载flows
        loaded_flows = self._load_flows(yaml_dict['flows'], loaded_slots)

        # 4. 返回FlowList

        return FlowList(flows=loaded_flows, slots=loaded_slots)

    def _load_slots(self, slots_dict: dict[str, Any]) -> dict[str, FlowSlot]:
        """
        职责:加载槽位
        Args:
            slots_dict:

        Returns:

        """
        loaded_slots: dict[str, FlowSlot] = {}
        for slot_name, slot_dict in slots_dict.items():
            loaded_slots[slot_name] = FlowSlot(
                slot_name=slot_name,
                type=slot_dict['type'],
                label=slot_dict['label'],
                description=slot_dict['description']
            )

        return loaded_slots

    def _load_flows(self,
                    flow_dict: dict[str, Any],
                    loaded_slots: dict[str, FlowSlot]) -> list[Flow]:
        loaded_flow: list[Flow] = []

        for flow_id, flow_dict in flow_dict.items():
            steps = [FlowStep.from_dict(step_data) for step_data in flow_dict['steps']]
            flow = Flow(
                id=flow_id,
                name=flow_dict['name'],
                description=flow_dict['description'],
                steps=steps,
                slots=self._build_flow_slot(steps, loaded_slots)
            )
            loaded_flow.append(flow)

        return loaded_flow

    def _build_flow_slot(self,
                         steps: list[FlowStep],
                         loaded_slots: dict[str, FlowSlot]) -> dict[str, FlowSlot]:
        """
        职责：获取当前业务流程缺少的槽位信息，方便后续直接通过获取Flow,就可以拿到缺少的槽位信，llm可以知道业务流程到底缺少什么槽位信息
        Args:
            steps:
            loaded_slots:

        Returns:

        """

        final_flow_slots: dict[str, FlowSlot] = {}

        for step in steps:

            if not isinstance(step, CollectionFlowStep):
                continue

            slot_name = step.slot_name

            slot_definition = loaded_slots[slot_name]

            final_flow_slots[slot_name] = slot_definition

        return final_flow_slots


if __name__ == '__main__':
    flow_loader = FlowLoader()

    # flow_list = flow_loader.load_single_yaml(Path("user_flows.yml"))

    flow_list=flow_loader.load_multi_yaml([Path("system_flows.yml"),Path("user_flows.yml")])



    print(flow_list)
