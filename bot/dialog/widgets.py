from typing import Optional, Union

from aiogram_dialog.widgets.kbd import Multiselect, Radio
from aiogram_dialog import DialogManager
from aiogram import types


class MultiCounterSelect(Multiselect):
    """Multiselect widget with the ability to choose one option several times"""

    def get_checked(self, manager: DialogManager) -> dict[str, int]:
        return self.get_widget_data(manager, {})

    async def reset_checked(
        self,
        event,
        manager: DialogManager,
    ) -> None:
        self.set_widget_data(manager, {})

    async def set_checked(
        self,
        event,
        item_id: str,
        checked: bool,
        manager: DialogManager,
    ) -> None:
        data: dict = self.get_checked(manager)
        changed = False

        if item_id in data:
            data[item_id] = data[item_id] + 1
            changed = True
        else:
            if self.max_selected == 0 or self.max_selected > len(data):
                data[item_id] = 1
                changed = True
        if changed:
            self.set_widget_data(manager, data)
            await self._process_on_state_changed(event, item_id, manager)

    async def _render_button(
        self, pos: int, item, data: dict, manager: DialogManager
    ) -> types.InlineKeyboardButton:

        item_id = self.item_id_getter(item)
        click_count = self.get_checked(manager).get(str(item_id), 0)

        data = {
            "data": data,
            "item": item,
            "pos": pos + 1,
            "pos0": pos,
            "click_count": click_count,
        }

        return types.InlineKeyboardButton(
            text=await self.text.render_text(data, manager),
            callback_data=self._item_callback_data(item_id),
        )
