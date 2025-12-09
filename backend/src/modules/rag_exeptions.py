
class ModuleLoadingFailure(Exception):
    def __init__(self, module):
        self.module = module
    def __str__(self):
        return f'Failed to load {self.module.__name__}'

class DimensionMismatch(Exception):
  def __init__(self, emb_dimension, ind_dimension):
    self.emb_dimension = emb_dimension
    self.ind_dimension = ind_dimension

  def __str__(self):
    return f"Несовпадение размерностей. " \
            f"Размерность эмбеддинов: {self.emb_dimension}" \
            f"Размерность индекса: {self.ind_dimension}"