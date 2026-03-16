import os
import torch.utils.data as data
import numpy as np
import open3d as o3d
from .build import DATASETS
from utils.logger import print_log


@DATASETS.register_module()
class Arqueo(data.Dataset):
    def __init__(self, config):
        self.parcial_path  = config.PARCIAL_POINTS_PATH
        self.completo_path = config.COMPLETO_POINTS_PATH
        self.npoints       = config.N_POINTS
        self.subset        = config.subset
        self.file_list     = self._get_file_list()

    def _get_file_list(self):
        pasta_parcial = self.parcial_path % self.subset
        arquivos = sorted([
            f for f in os.listdir(pasta_parcial) if f.endswith('.pcd')
        ])
        print_log(f'Arqueo dataset [{self.subset}]: {len(arquivos)} amostras', logger='ARQUEO')
        return arquivos

    def _carregar_pcd(self, caminho):
        pcd = o3d.io.read_point_cloud(caminho)
        pontos = np.asarray(pcd.points, dtype=np.float32)
        # Garante exatamente N_POINTS pontos
        if len(pontos) >= self.npoints:
            idx = np.random.choice(len(pontos), self.npoints, replace=False)
        else:
            idx = np.random.choice(len(pontos), self.npoints, replace=True)
        return pontos[idx]

    def __getitem__(self, idx):
        nome = self.file_list[idx]
        parcial  = self._carregar_pcd(os.path.join(self.parcial_path  % self.subset, nome))
        completo = self._carregar_pcd(os.path.join(self.completo_path % self.subset, nome))

        # Augmentação simples no treino: espelhamento aleatório no eixo X
        if self.subset == 'train' and np.random.rand() > 0.5:
            parcial[:, 0]  *= -1
            completo[:, 0] *= -1

        import torch
        return 'urna', nome, (torch.tensor(parcial), torch.tensor(completo))

    def __len__(self):
        return len(self.file_list)
