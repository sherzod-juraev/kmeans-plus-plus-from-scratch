from numpy import empty, ndarray
from numpy.random import default_rng
from scipy.spatial.distance import cdist


class KmeansPP:
    """
    KMeans++ clustering initialization.

    This class implements the KMeans++ algorithm for initializing cluster centroids.
    The KMeans++ initialization improves the speed of convergence and reduces
    the chances of poor clustering compared to random initialization.

    Attributes:
        n_clusters (int): Number of clusters to initialize.
        rng (np.random.Generator): NumPy random number generator, seeded for reproducibility.
    """

    def __init__(self, n_clusters: int = 2, random_state: int | None = None, /):

        self.n_clusters = n_clusters
        self.rng = default_rng(random_state)

    def initialize_centroids(self, X: ndarray, /) -> ndarray:
        """
        Initialize centroids using the KMeans++ algorithm.

        Args:
            X (np.ndarray): Input data of shape (n_samples, n_features).

        Returns:
            np.ndarray: Initialized centroids of shape (n_clusters, n_features).

        Algorithm:
            1. Select the first centroid randomly from the data points.
            2. For each remaining centroid:
                a. Compute squared distances from each point to the nearest existing centroid.
                b. Compute probabilities proportional to these distances.
                c. Select a new centroid according to the computed probabilities.
        """

        n = X.shape[0]
        centroids = empty((self.n_clusters, X.shape[1]))
        first_ind = self.rng.integers(0, n)
        centroids[0] = X[first_ind].copy()

        for i in range(1, self.n_clusters):
            prob = self.__calculate_probability(X, centroids[:i, :])
            new_cen_ind = self.rng.choice(n, p=prob)
            centroids[i] = X[new_cen_ind].copy()

        return centroids


    def __calculate_probability(self, X: ndarray, centroids: ndarray, /) -> ndarray:
        """
        Compute probability of each sample to be selected as the next centroid.

        Args:
            X (np.ndarray): Input data of shape (n_samples, n_features).
            centroids (np.ndarray): Current centroids of shape (current_clusters, n_features).

        Returns:
            np.ndarray: Probabilities for each data point, summing to 1.

        Notes:
            - The probability for each point is proportional to the squared distance
              to its nearest existing centroid.
            - A small epsilon (1e-12) is added to prevent division by zero.
        """

        dist_sq = cdist(X, centroids, 'sqeuclidean')
        min_dist_sq = dist_sq.min(axis=1)
        prob = min_dist_sq / (min_dist_sq.sum() + 1e-12)
        return prob