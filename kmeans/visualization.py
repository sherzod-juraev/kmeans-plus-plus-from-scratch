import matplotlib.pyplot as plt
from numpy import ndarray


def plot_clusters(
        X: ndarray,
        centroids: ndarray,
        title: str = 'Kmeans'
):
    n_clusters = centroids.shape[0]
    for i in range(n_clusters):
        plt.scatter(X[:, 0],
                    X[:, 1],
                    label=f'Cluster {i}',
                    marker='s',
                    markersize=5)
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x',
                markersize=5,
                color='black',
                label='Centroids')
    plt.title(title)
    plt.legend('lower right')
    plt.grid()
    plt.show()