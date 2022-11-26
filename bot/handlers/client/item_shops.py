'''Item shops client-side handlers'''

import operator

from aiogram_dialog import Window, Dialog

from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import ItemShopsSG
from dialog.data_getters import get_item_shops_data

item_shops_window = Window(
    Const('Магазины в которых есть товар:'),
    ScrollingGroup(
        Select(
            Format('{item[0]} ({item[3]} штук/и) {item[1]}'),
            'itemdetailshopssel',
            operator.itemgetter(2),
            'item_shops',
            ),
        width=2,
        height=4,
        id='itemdetailshops',
    ),
    Cancel(Const('Назад')),
    state=ItemShopsSG.item_shops,
    getter=get_item_shops_data
    )

item_shops_dialog = Dialog(item_shops_window)