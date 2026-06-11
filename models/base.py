class BaseEntity:
    _global_id_counter = 1 

    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplementedError("howdy sparrow Subclasses must implement to_dict")

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError("howdy sparrow Subclasses must implement from_dict")

    def __str__(self):
        name_attr = getattr(self, 'name', None)
        title_attr = getattr(self, 'title', None)
        task_attr = getattr(self, 'title', None) 
        identifier = name_attr or title_attr or task_attr or "Unknown"
        return f"{self.__class__.__name__}: {identifier}"

    def __repr__(self):
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"