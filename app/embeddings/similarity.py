import numpy as np

def cosine_similarity(vec1, vec2):

    """Function that provide the cosine similarity of two arrays
    
    Args:
        vec1, vec2: number arrays
    Returns:
        The value of the cosine similarity"""

    a = np.array(vec1)
    b = np.array(vec2)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))