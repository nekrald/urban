import numpy as np
import pandas as pd
from skimage.io import imread
import pickle
import tqdm
import scipy.misc

from sklearn.cluster import  FeatureAgglomeration, SpectralClustering

import constants


class WallpaperPhotoMaster(object):
    """
    some init magic here
    """
    def __init__(self,
                 path_to_csv='wallpapers_photo.csv',
                 path_to_dir='wallpapers_photo/',
                 path_to_pkl='names_cosine_wallpapers_photo_color.pkl',
                 path_to_color_pkl='wallpapers_photo_color_distances.pkl'):
        def _compute_clusters(cosines):
            np.random.seed(0)
            n_clusters, power = constants.N_CLUSTERS, constants.SIM_POWER
            clst = SpectralClustering(affinity='precomputed', n_clusters = n_clusters)
            #delta = np.mean(np.power(distances, power))
            #similarities = np.exp(-np.power(distances, power) / delta * 0.6)
            clst.fit(np.power(cosines, power))
            return n_clusters, clst.labels_

        self.data = pd.read_csv(path_to_csv)
        self.path = path_to_dir
        self.names, self.cosines = pickle.load(file=open(path_to_pkl, 'rb'))
        self.names = np.array(self.names)
        self.indices_by_name = {self.names[index] : index for index in range(len(self.names))}
        self.color_distances = pickle.load(file=open(path_to_color_pkl, 'rb'))

        self.n_clusters, self.labels = _compute_clusters(self.cosines)
        self.initial_names = np.array(['90051059', ' 90018324', '90020735',
                                       '90050967', '90050892', '90020704'])


    def __repr__(self):
        return "WallpaperMaster object"


    def get_initial_pictures(self):
        return self.initial_names, np.array([self.path + name + '.png' for name in self.initial_names])

    def get_next_pictures(self, name):
        cosines_now = self.cosines[self.indices_by_name[name]]
        need = np.argsort(cosines_now)[::-1][constants.RANKED_INDICES]
        names = self.names[need]
        return names, np.array([self.path + name + '.png' for name in names])

    def get_final_pictures(self, names):
        cosines_now = np.array([self.cosines[self.indices_by_name[name]] for name in names]).sum(axis=0)
        need = np.argsort(cosines_now)[::-1][:constants.NB_RANKED_PICTURES]
        names = self.names[need]
        return names, np.array([self.path + name + '.png' for name in names])
