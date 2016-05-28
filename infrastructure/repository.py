

class Repository(object):
    def __init__(self, unit, session):
        self.entities = []
        self.unit = unit
        self.session = session

    def find(self, _id):
        pass

    def add(self, entity):
        if not isinstance(entity, self.unit):
            raise TypeError('{} repository can not add {} object'.format(self.unit.__name__, entity.__class__.__name__))
        self.session.add(entity)
        self.session.commit()

    def remove(self, entity):
        if not isinstance(entity, self.unit):
            raise TypeError('{} repository can not del {} object'.format(self.unit.__name__, entity.__class__.__name__))
        self.session.delete(entity)
        self.session.commit()
