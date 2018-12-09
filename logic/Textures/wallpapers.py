import numpy as np
import pandas as pd
from skimage.io import imread
import pickle
import tqdm
import scipy.misc

from sklearn.cluster import  FeatureAgglomeration, SpectralClustering

import constants
import sys
import os

FILE_DIR_WALLPAPERS = os.path.dirname(os.path.realpath(__file__))

class WallpaperMaster(object):
    """
    some init magic here
    """
    def __init__(self,
                 path_to_csv=os.path.join(FILE_DIR_WALLPAPERS, 'wallpapers.csv'),
                 path_to_dir=os.path.join(FILE_DIR_WALLPAPERS, 'wallpapers/'),
                 path_to_pkl=os.path.join(FILE_DIR_WALLPAPERS, 'names_distances_wallpapers_gray.pkl'),
                 path_to_color_pkl=os.path.join(FILE_DIR_WALLPAPERS, 'wallpapers_color_distances.pkl')):
        def _compute_clusters(distances):
            np.random.seed(0)
            n_clusters, power = constants.N_CLUSTERS, constants.POWER
            clst = SpectralClustering(affinity='precomputed', n_clusters = n_clusters)
            delta = np.mean(np.power(distances, power))
            similarities = np.exp(-np.power(distances, power) / delta * 0.6)
            clst.fit(similarities)
            return n_clusters, clst.labels_

        self.data = pd.read_csv(path_to_csv)
        self.path = path_to_dir
        self.names, self.distances = pickle.load(file=open(path_to_pkl, 'rb'))
        self.names = np.array(self.names)
        self.indices_by_name = {self.names[index] : index for index in range(len(self.names))}
        self.color_distances = pickle.load(file=open(path_to_color_pkl, 'rb'))

        self.n_clusters, self.labels = _compute_clusters(self.distances)


    def __repr__(self):
        return "WallpaperMaster object"


    def get_pictures_by_color_id(self, color_id):
        """
        color_id is an index of the color from the list: constants.COLORS
        """
        names, links = [], []
        relevant_color_distances = self.color_distances[color_id]
        for cluster_index in range(self.n_clusters):
            mask = (self.labels == cluster_index)
            distances_now = relevant_color_distances[mask]
            need = np.argsort(distances_now)[0]
            names.append(self.names[mask][need])
            links.append(self.path + self.names[mask][need] + '.png')
        return np.array(names), np.array(links)


    def get_ranked_pictures(self, color_id, name, color_weight=5.0):
        index = self.indices_by_name[name]
        total_distances = np.zeros(self.names.shape[0])
        total_distances += np.log(self.distances[index])
        total_distances += np.log(self.color_distances[color_id])\
                            * color_weight
        names = self.names[np.argsort(total_distances)[0:constants.NB_RANKED_PICTURES]]
        links = np.array([self.path + name + '.png' for name in names])
        return names, links
