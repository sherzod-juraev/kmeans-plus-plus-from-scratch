import matplotlib.pyplot as plt
from numpy import ndarray
from sklearn.decomposition import PCA


def plot_clusters(
        X: ndarray,
        centroids: ndarray,
        pca_mdoel : PCA,
        normalization_model,
        title: str = 'Kmeans'
):

    X_nor = normalization_model.transform(X)
    X = pca_mdoel.transform(X_nor)
    print(X)
    plt.scatter(X[:, 0],
                X[:, 1],
                marker='s')
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x',
                color='black')
    plt.title(title)
    plt.grid()
    plt.show()