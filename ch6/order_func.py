"""示例 6-1"""


from abc import ABC, abstractmethod
from collections import namedtuple


Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
  def __init__(self, product, quantity, price):
    self.product = product
    self.quantity = quantity
    self.price = price

  def total(self):
    return self.price * self.quantity


class Order:  # 上下文
  def __init__(self, customer, cart, promotation=None):
    self.customer = customer
    self.cart = list(cart)
    self.promotation = promotation

  def total(self):
    if not hasattr(self, '__total'):
      self.__total = sum(item.total() for item in self.cart)
    return self.__total

  def due(self):
    if self.promotation is None:
      discount = 0
    else:
      discount = self.promotation(self)
    return self.total() - discount
  
  def __repr__(self):
    fmt = '<Order total: {:.2f} due:{:.2f}>'
    return fmt.format(self.total(), self.due())


def fidelity_promo(order):  # 第一个具体策略
  """为积分为 1000 或以上的顾客提供 5% 的折扣"""
  return order.total() * 0.05 if order.customer.fidelity > 1000 else 0


def bulk_item_promo(order):  # 第二个策略
  """单个商品为 20 个或以上时，提供 10% 折扣"""
  discount = 0
  for item in order.cart:
    if item.quantity >= 20:
      discount += item.total() * 0.1
  return discount


def large_order_promo(order):  # 第三个策略
  """订单中的不同商品达到10个或以上时提供7%折扣"""
  distinct_items = {item.product for item in order.cart}
  return order.total() * 0.07 if len(distinct_items) >= 10 else 0


promos = [fidelity_promo, bulk_item_promo, large_order_promo]


def best_promo(order):
  """选择可用的最佳策略
  """
  return max(promo(order) for promo in promos)


promos_auto = [globals()[name] for name in globals()
        if name.endswith('_promo')
        and name != 'best_promo']


def best_promo_auto(order):
  """例6-7 使用自动遍历所得的列表"""
  return max(promo(order) for promo in promos_auto)