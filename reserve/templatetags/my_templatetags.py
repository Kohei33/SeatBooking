from django import template
import datetime

register = template.Library()


@register.simple_tag
def access_dict(some_dict: dict, index1: int, index2: datetime):
    """
    辞書の要素のうち、インデックスで指定した要素を返す
    :param some_dict: 要素を取得したい辞書
    :param index1: 取得したい辞書のインデックス(1次元目)
    :param index2: 取得したい辞書のインデックス(2次元目)
    :return: 指定したインデックスに格納されているリストの要素
    """
    try:
        result = some_dict[index1][index2]

        if result:
            return "○"
        else:
            return "×"
    except:
        return ""