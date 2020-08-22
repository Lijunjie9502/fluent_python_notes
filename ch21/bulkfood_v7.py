import ch21.model_v7 as model


class LineItem(model.Entity):  # ➊ LineItem 是 model.Entity 的子类
  description = model.NonBlank()
  weight = model.Quantity()
  price = model.Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price