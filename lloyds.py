import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import os

#essentially, KMeans now takes in a dataset, k, and centers and then from that we can get the snapshot
  #need to get the centers depending on the type of thing specified -- call kmeans within that function 
class KMeans():
  def __init__(self, data, k, centers):
    self.data = data
    self.k = k
    self.centers = centers
    self.assignment = [-1 for _ in range(len(data))]
    self.snaps = []
    
  def snap(self, centers, count):
    TEMPFILE = f'/static/{count}.png'

    os.makedirs(os.path.dirname(TEMPFILE), exist_ok=True)

    fig, ax = plt.subplots()
    ax.scatter(self.data[:, 0], self.data[:, 1], c=self.assignment)
    ax.scatter(centers[:,0], centers[:, 1], c='r')
    fig.savefig(TEMPFILE)
    plt.close()
    self.snaps.append(TEMPFILE)
    # self.snaps.append(im.fromarray(np.asarray(im.open(TEMPFILE))))

  def isunassigned(self, i):
    return self.assignment[i] == -1

  def initialize(self):
    return self.data[np.random.choice(len(self.data) - 1, size=self.k, replace=False)]

  def make_clusters(self, centers):
      for i in range(len(self.assignment)):
        for j in range(self.k):
          if self.isunassigned(i):
            self.assignment[i] = j
            dist = self.dist(centers[j], self.data[i])
          else:
            new_dist = self.dist(centers[j], self.data[i])
            if new_dist < dist:
              self.assignment[i] = j
              dist = new_dist
              
  def compute_centers(self):
    centers = []
    for i in range(self.k):
      cluster = []
      for j in range(len(self.assignment)):
        if self.assignment[j] == i:
          cluster.append(self.data[j])
      centers.append(np.mean(np.array(cluster), axis=0))

    return np.array(centers)
  
  def unassign(self):
    self.assignment = [-1 for _ in range(len(self.data))]

  def are_diff(self, centers, new_centers):
    for i in range(self.k):
      if self.dist(centers[i], new_centers[i]) != 0:
        return True
    return False

  def dist(self, x, y):
    # Euclidean distance
    return sum((x - y)**2) ** (1/2)

  def lloyds(self):
    # centers = self.initialize()
    count = 0
    self.make_clusters(self.centers)
    new_centers = self.compute_centers()
    self.snap(new_centers, count)
    while self.are_diff(self.centers, new_centers):
      count += 1
      self.unassign()
      self.centers = new_centers
      self.make_clusters(self.centers)
      new_centers = self.compute_centers()
      self.snap(new_centers, count)
    return

def random_centers(n, data):
  return data[np.random.choice(len(data) - 1, size=n, replace=False)]

def farthest_centers(n, data):
  #Randomly select the first center
  first_center_idx = np.random.choice(len(data))
  centers = [data[first_center_idx]]
  
  #select farthest away center after that 
  for _ in range(1, n):
    # Calculate distances from the existing centers
    distances = np.array([min(np.linalg.norm(data_point - center) for center in centers) for data_point in data])
    
    # Select the point with the maximum distance
    farthest_point_idx = np.argmax(distances)
    centers.append(data[farthest_point_idx])
      
  return centers

def kplusplus_centers(n, data):
  # Step 1: Randomly select the first centroid
    first_centroid_idx = np.random.choice(len(data))
    centroids = [data[first_centroid_idx]]

    # Step 2: Select remaining centroids
    for _ in range(1, n):
      # Calculate distances from each point to the nearest centroid
      distances = np.array([min(np.linalg.norm(data_point - centroid) for centroid in centroids) for data_point in data])
      
      # Step 3: Select the next centroid with a probability proportional to D^2
      probabilities = distances ** 2
      probabilities /= probabilities.sum()  # Normalize to get a probability distribution
      
      next_centroid_idx = np.random.choice(len(data), p=probabilities)
      centroids.append(data[next_centroid_idx])

    return np.array(centroids)

