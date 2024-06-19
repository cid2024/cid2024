
from torch.nn.functional import cosine_similarity

def vector_similarity (vector1, vector2):
    return cosine_similarity(vector1, vector2, dim=0).item()