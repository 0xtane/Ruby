#!/usr/bin/env python
import pandas as pd
import numpy as np

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

from common import describe_data, test_env


def print_info(credit_info):
    print("credit information")
    print(credit_info.info())

    print("\ndf shape")
    print(credit_info.shape)

    print("\ndf columns")
    print(credit_info.columns)

    print("\ndf head + tail")
    print(credit_info.head())
    print(credit_info.tail())

    print("\nnum value stats")
    print(credit_info.describe())


def plot_clusters(X, y, figure, file):
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
              'tab:brown', 'tab:pink', 'tab:olive']
    markers = ['o', 'X', 's', 'D']
    color_idx = 0
    marker_idx = 0

    plt.figure(figure)

    for cluster in range(0, len(set(y))):
        plt.scatter(X[y == cluster, 0], X[y == cluster, 1],
                    s=5, c=colors[color_idx], marker=markers[marker_idx])
        color_idx = 0 if color_idx == (len(colors) - 1) else color_idx + 1
        marker_idx = 0 if marker_idx == (len(markers) - 1) else marker_idx + 1

    plt.title(figure)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(file, papertype='a4')

    plt.show()


def clustering(df):
    Sum_of_squared_distances = []

    K = range(1, 15)
    for k in K:
        km = KMeans(n_clusters=k, init='k-means++', random_state=0)
        km = km.fit(df)
        Sum_of_squared_distances.append(km.inertia_)

    plt.plot(K, Sum_of_squared_distances)
    plt.xlabel('n of clusters')
    plt.ylabel('WCSS')
    plt.grid()
    plt.title('elbow Method')
    plt.savefig('results/cc_wcss_plot.png', papertype='a4')
    plt.show()


if __name__ == '__main__':
    modules = ['numpy', 'pandas', 'sklearn']
    test_env.versions(modules)
    df = pd.read_csv('data/cc_general.csv')
    print_info(df)
    df = df.drop(columns="CUST_ID")
    df = df.fillna(df.mean())
    X = df.values
    cs = df.columns

    for c in cs:
        print("\nunique values for " + c + " is")
        print(df[c].unique())

    clustering(X)
    n_clusters = 8
    k_means = KMeans(n_clusters=n_clusters, init='k-means++', random_state=0)
    y_kmeans = k_means.fit_predict(X)
    X_tsne = TSNE(n_components=2, random_state=0).fit_transform(X)

    plot_clusters(X_tsne, np.full(X_tsne.shape[0], 0),
                  't-SNE visualisation without clusters', 'results/cc_tsne_no_clusters.png')

    plot_clusters(X_tsne, y_kmeans, 'k means clusters with TSNE',
                  'results/cc_tsne_X_clusters.png')
