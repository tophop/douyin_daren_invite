# -*- coding:utf-8 -*-

import xlwings as xw

def get_phone_list():
    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(r"G:\订单记录\20220210pdd.xlsx")
    st=xw.sheets[0]
    row_count=st.range('b1').expand('table').rows.count
    print(row_count)
    order_list=st.range(f'b1:b{row_count}').value
    return order_list

