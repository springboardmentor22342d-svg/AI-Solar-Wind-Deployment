class VectorProcessor:
    def load_vector_layer(slef,path: str):
        raise NotImplementedError
    def find_nearest_feature(self,latitude,longitude):
        raise NotImplementedError
    def intersects(self,geometry):
        raise NotImplementedError
    def within_distance(self,geometry,distance):
        raise NotImplementedError