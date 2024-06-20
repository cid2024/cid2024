from torch.nn.functional import cosine_similarity

import torch


def vector_similarity(vector1: torch.Tensor, vector2: torch.Tensor) -> float:
    return cosine_similarity(vector1, vector2, dim=0).item()
