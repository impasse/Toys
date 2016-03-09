#!/usr/bin/env python3
# -*-encoding=utf-8-*-
import json
import sys
from functools import reduce
from io import StringIO


'''
json demo:
[
  "ITEM000001",
  "ITEM000001",
  "ITEM000001",
  "ITEM000001",
  "ITEM000001",
  "ITEM000003-2",
  "ITEM000005",
  "ITEM000005",
  "ITEM000005"
]
'''


class Item:
    class Type:
        N = 0  # 无
        A = 1  # 满2减1
        B = 2  # 95折

    # 商品信息
    Goods = {
        'ITEM000001': {'name': '羽毛球', 'price': 1, 'unit': '个', 'type': Type.A},
        'ITEM000005': {'name': '可口可乐', 'price': 3, 'unit': '瓶', 'type': Type.A},
        'ITEM000003': {'name': '苹果', 'price': 5.5, 'unit': '斤', 'type': Type.B},
    }

    def __init__(self, id, count=1):
        if id in Item.Goods.keys():
            self.__dict__.update(id=id, count=count)
            self.__dict__.update(Item.Goods[id])
        else:
            raise RuntimeError('good not defined')

    @staticmethod
    def get_by_id(id):
        if len(id) == 10:
            return Item(id)
        else:
            return Item(id[0:10], int(id[11:]))

    def __str__(self):
        return str(self.__dict__)


class Middleware:
    def before(self, item):
        '''单条信息录入时'''
        return None, False

    def after(self):
        '''所有信息录入完成'''
        return None, 0

    def end(self):
        '''额外信息'''
        return None, 0


class SimpleMiddleware(Middleware):
    '''实现基础功能'''
    def __init__(self):
        self.total = 0
        self.bag = {}

    def before(self, item):
        self.total += item.price * item.count
        if self.bag.get(item.id):
            self.bag[item.id].count += 1
        else:
            self.bag[item.id] = item
        return None, True

    def after(self):
        return '\n'.join(
            map(lambda item: '名称：{0}，数量：{1}{2}，单价：{3:.2f}(元)，小计：{4:.2f}(元)'.format(item.name, item.count, item.unit,
                                                                                   item.price,
                                                                                   item.count * item.price),
                self.bag.values())), self.total


def after(self):
    return None, self.total


class TwoToThree(Middleware):
    '''满2减1'''
    def __init__(self):
        self.bag = {}

    def before(self, item):
        if item.type == Item.Type.A:
            if self.bag.get(item.id):
                self.bag[item.id].count += 1
            else:
                self.bag[item.id] = item
            return None, True
        else:
            return None, False

    def after(self):
        total = 0

        def single(item):
            nonlocal total
            total += item.price * item.count
            if item.count > 2:
                item.discount_count = item.count // 3
            else:
                item.discount_count = 0
            return '名称：{0}，数量：{1}{2}，单价：{3:.2f}(元)，小计：{4:.2f}(元)'.format(item.name,
                                                                         item.count, item.unit,
                                                                         item.price,
                                                                         (item.count - item.discount_count) *
                                                                         item.price)

        return "\n".join(map(single, self.bag.values())), total

    def end(self):
        if len(self.bag) == 0:
            return Middleware.after(self)
        else:
            return '买二赠一商品：\n' + '\n'.join(
                map(lambda i: '名称：' + i.name + ',数量:' + str(i.discount_count) + i.unit, self.bag.values())), reduce(
                lambda a, b: a + b, [
                    i.discount_count * i.price for i in self.bag.values()], 0)


class Pecent95(Middleware):
    '''95折'''
    def __init__(self):
        self.bag = {}
        self.discount = 0

    def before(self, item):
        if item.type == Item.Type.B:
            if self.bag.get(item.id):
                self.bag[item.id].count += 1
            else:
                self.bag[item.id] = item
            return None, True
        return None, False

    def after(self):
        total = 0

        def single(item):
            nonlocal total
            item.discount = item.price / 20
            self.discount += item.discount * item.count
            total += item.price * item.count
            return '名称：{0}，数量：{1}{2}，单价：{3:.2f}(元)，小计：{4:.2f}(元)，节省{5:.2f}(元）'.format(item.name,
                                                                                      item.count,
                                                                                      item.unit,
                                                                                      item.price,
                                                                                      item.count *
                                                                                      (item.price - item.discount),
                                                                                      item.discount *
                                                                                      item.count)

        return "\n".join(map(single, self.bag.values())), total

    def end(self):
        return None, self.discount


def main(obj):
    '''主函数,middleware执行流程'''
    def print_to_buffer(arg):
        if arg is not None and arg != '':
            print(arg, file=output)

    middlewares = [TwoToThree(), Pecent95(), SimpleMiddleware()]
    output = StringIO()
    total = 0
    discount = 0

    print_to_buffer('***<没钱赚商店>购物清单***')
    items = [Item.get_by_id(i) for i in obj]
    for i in range(len(items)):
        for m in middlewares:
            tmp, stop = m.before(items[i])
            print_to_buffer(tmp)
            if stop:
                break
    for m in middlewares:
        tmp, p = m.after()
        print_to_buffer(tmp)
        total += p
    print_to_buffer('----------------------')
    for m in middlewares:
        tmp, p = m.end()
        print_to_buffer(tmp)
        discount += p
    if discount != 0:
        print_to_buffer('----------------------')
    print_to_buffer('总计:{0:.2f}(元)'.format(total - discount))
    if discount is not 0:
        print_to_buffer('节省:{0:.2f}(元)'.format(discount))
    print_to_buffer('**********************')
    print(output.getvalue())


if __name__ == '__main__':
    '''usage: this.py xxx.json'''
    with open(sys.argv[1]) as f:
        main(json.load(f))
