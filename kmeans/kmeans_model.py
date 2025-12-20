from .kmeans_pp import KmeansPP
from .options import NormalizationOptions, KmeansInitOptions
from numpy import ndarray, allclose
from numpy.random import default_rng
from scipy.spatial.distance import cdist
from fastapi import HTTPException
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA


class Kmeans:
    """
    KMeans clustering algorithm with support for KMeans++ and random initialization.

    Parameters
    ----------
    n_clusters : int
        Number of clusters to form.
    max_iter : int
        Maximum number of iterations of the KMeans algorithm.
    tol : float
        Convergence tolerance. If the change in centroids is less than this value, algorithm stops.
    init : KmeansInitOptions
        Method for initialization: KMEANS_PP (KMeans++) or RANDOM (random choice of initial centroids).
    random_state : int | None
        Seed for random number generator to ensure reproducibility.

    Attributes
    ----------
    centroids : ndarray | None
        Coordinates of cluster centers after fitting.
    labels_ : ndarray | None
        Labels of each point after fitting.
    """

    def __init__(self,
                 n_clusters: int = 2,
                 max_iter: int = 100,
                 tol: float = 1e-4,
                 init: KmeansInitOptions = KmeansInitOptions.KMEANS_PP,
                 random_state: int | None = None,
                 pca_n_components: int = 2,
                 normalization: NormalizationOptions = NormalizationOptions.Z_SCORE,
                 /):

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.init = init
        self.centroids = None
        self.random_state = random_state
        self.labels_ = None
        self.pca_n_components = pca_n_components
        self.normalization = normalization

    def __initialize_centroids(self, X: ndarray, /):
        """
        Initialize centroids for KMeans algorithm.

        Depending on `self.init`, centroids are initialized either using:
        - KMeans++ (via KmeansPP class)
        - Random choice from the dataset

        Parameters
        ----------
        X : ndarray
            Input data of shape (n_samples, n_features)
        """

        if self.init == KmeansInitOptions.KMEANS_PP:
            self.centroids = KmeansPP(self.n_clusters, self.random_state).initialize_centroids(X)
        else:
            n_samples, m_features = X.shape[0], X.shape[1]
            rng = default_rng(self.random_state)
            ind = rng.choice(n_samples, size=self.n_clusters, replace=False)
            self.centroids = X[ind].copy()

    def __calculate_distance(self, X: ndarray, /) -> ndarray:
        """
        Compute the closest centroid for each sample.

        Parameters
        ----------
        X : ndarray
            Data points, shape (n_samples, n_features)

        Returns
        -------
        cluster_labels : ndarray
            Index of the nearest centroid for each sample, shape (n_samples,)

        Notes
        -----
        Uses squared Euclidean distance (same metric as KMeans++ initialization).
        """

        dist_sq = cdist(X, self.centroids, 'sqeuclidean')
        cluster_labels = dist_sq.argmin(axis=1)
        return cluster_labels

    def __update_centroids(self, X: ndarray, /):
        """
        Update cluster centroids based on current assignments.

        Parameters
        ----------
        X : ndarray
            Input data, shape (n_samples, n_features)

        Notes
        -----
        - For each cluster, centroid is updated to the mean of assigned points.
        - If a cluster has no points, its previous centroid is kept.
        - Requires `self.labels_` to be already computed.
        """

        for i in range(self.n_clusters):
            centroid = X[self.labels_ == i]
            if len(centroid) > 0:
                self.centroids[i] = centroid.mean(axis=0)

    def fit(self, X: ndarray, /):
        """
        Compute KMeans clustering.

        Parameters
        ----------
        X : ndarray
            Data points to cluster, shape (n_samples, n_features)

        Returns
        -------
        self : Kmeans
            Fitted KMeans object with updated centroids and labels.

        Notes
        -----
        - Stops early if centroids change less than `self.tol`.
        - Runs up to `self.max_iter` iterations.
        - After fitting, `self.labels_` contains cluster labels.
        """
        if self.normalization == NormalizationOptions.Z_SCORE:
            self.normalization = StandardScaler()
        else:
            self.normalization = MinMaxScaler()
        X = self.normalization.fit_transform(X)
        self.pca = PCA(n_components=self.pca_n_components)
        X = self.pca.fit_transform(X)
        self.__initialize_centroids(X)
        for i in range(self.max_iter):
            self.labels_ = self.__calculate_distance(X)
            old_centroids = self.centroids.copy()
            self.__update_centroids(X)
            if allclose(old_centroids, self.centroids, atol=self.tol):
                break
        return self

    def predict(self, X: ndarray, /) -> ndarray:
        """
        Predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : ndarray
            Data points to assign, shape (n_samples, n_features)

        Returns
        -------
        cluster_labels : ndarray
            Index of the nearest cluster for each sample.

        Raises
        ------
        ValueError
            If the model has not been fitted yet (`self.centroids` is None).
        """

        if self.centroids is None:
            raise HTTPException(
                status_code=400,
                detail="Model is not fitted yet. Call `fit` first."
            )
        X = self.normalization.transform(X)
        X = self.pca.transform(X)
        cluster_labels = self.__calculate_distance(X)
        return cluster_labels