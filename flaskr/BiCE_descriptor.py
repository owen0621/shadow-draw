import numpy as np
import cv2


def compute_BiCE_descriptor(patch):
    # Define parameters
    n_orientations = 4
    n_positions_perp = 18
    n_positions_tang = 6
    n_bins = n_orientations * n_positions_perp * n_positions_tang

    # Compute edge gradient magnitude and orientation
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    gradient_x = cv2.filter2D(patch, -1, sobel_x)
    gradient_y = cv2.filter2D(patch, -1, sobel_y)
    gradient_mag = np.sqrt(gradient_x**2 + gradient_y**2)
    gradient_orient = np.arctan2(gradient_y, gradient_x)

    # Compute histogram of edge positions and orientations
    histogram = np.zeros((n_positions_perp, n_positions_tang, n_orientations))
    for i in range(patch.shape[0]):
        for j in range(patch.shape[1]):
            orient_bin = (
                int((gradient_orient[i, j] / np.pi + 0.5) * n_orientations)
                % n_orientations
            )
            perp_bin = int((i / patch.shape[0]) * n_positions_perp)
            tang_bin = int((j / patch.shape[1]) * n_positions_tang)
            histogram[perp_bin, tang_bin, orient_bin] += gradient_mag[i, j]

    # Binarize histogram and concatenate into descriptor
    descriptor = np.zeros(n_bins)
    bin_cutoff = np.percentile(histogram, 80)
    for i in range(n_positions_perp):
        for j in range(n_positions_tang):
            for k in range(n_orientations):
                bin_index = (
                    i * n_positions_tang * n_orientations + j * n_orientations + k
                )
                if histogram[i, j, k] > bin_cutoff:
                    descriptor[bin_index] = 1

    return descriptor
