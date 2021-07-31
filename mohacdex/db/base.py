from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def class_to_dict(c):
    return [(k, v) for k, v in vars(c).items() if not k.startswith('_') and not callable(getattr(c, k))]

class Base:
    def __repr__(self) -> str:
        attrs = ', '.join(f"{k}={v}" for k, v in class_to_dict(self))
        return f"{self.__class__.__name__}<{attrs}>"

Base = declarative_base(cls=Base)