import annoy
import numpy as np

"""
TEST CODE FOR USING ANN!
"""

class KNN():

    def __init__(self, data_points):
        self.data_list = data_points
        self.dimension = data_points.shape[1]
        self.vectors = data_points.astype('float32') 

   
    def build(self, number_of_trees=10):

        self.index = annoy.AnnoyIndex(self.dimension, metric='euclidean')

        for i, vec in enumerate(self.vectors):
            self.index.add_item(i, list(vec))

        self.index.build(number_of_trees)
        
    def query(self, vector, num_neighbors=10, distances=False):

        indices = self.index.get_nns_by_vector(vector=vector.tolist(), n=num_neighbors, include_distances=distances)                                           
        
        data_points = [tuple(self.data_list[i]) for i in indices]

        return data_points


if __name__ == "__main__":
    data = np.array([(i,j) for i,j in zip(range(10000),range(1000,-1,-1))])

    knn = KNN(data)

    #print(KNN.dimension)
    #print(KNN.vectors)

    tree_numbers = 1

    knn.build(tree_numbers)

    list_ = knn.query(np.array((100,500)), k=10)

    print(list_)


    