"""
TSRD Radar Signal Dataset Loader
Turing Synthetic Radar Dataset - Radar Pulse Deinterleaving

数据格式:
- data: (N_pulses, 5) float32, features: [ToA, Freq, PW, AoA, Amp]
- labels: (N_pulses, 1) int8, emitter class labels (0 to N_emitters-1)
- metadata: receiver and transmitter configuration info

使用方法:
    from data_loader import TSRDLoader
    loader = TSRDLoader('/path/to/data')
    data, labels = loader.load_sample('archive/train/train_0.h5')
"""

import h5py
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional

DATA_ROOT = Path('/opt/data/workspace/雷达信号分选')
FEATURE_NAMES = ['ToA', 'Freq', 'PW', 'AoA', 'Amp']  # 5 features
FEATURE_UNITS = ['us', 'MHz', 'us', 'deg', 'dB']


class TSRDLoader:
    """TSRD 数据加载器"""
    
    def __init__(self, root: str = None):
        self.root = Path(root) if root else DATA_ROOT
    
    def load_sample(self, relative_path: str) -> Tuple[np.ndarray, np.ndarray, dict]:
        """
        加载单个样本
        
        Returns:
            data: (N, 5) float32 PDW features
            labels: (N, 1) int8 emitter labels  
            metadata: dict with sample metadata
        """
        fpath = self.root / relative_path
        with h5py.File(fpath, 'r') as f:
            data = f['data'][:]
            labels = f['labels'][:].flatten()
            metadata = self._load_metadata(f)
        return data, labels, metadata
    
    def _load_metadata(self, h5_file) -> dict:
        """加载元数据"""
        meta = h5_file['metadata']
        return {
            'feature_names': [n.decode() for n in meta['feature_names'][:]],
            'n_pulses': len(h5_file['data'][:]),
            'n_emitters': len(np.unique(h5_file['labels'][:])),
        }
    
    def list_samples(self, category: str) -> List[str]:
        """列出某个类别的所有样本文件"""
        patterns = {
            'archive_train': 'archive/train/*.h5',
            'archive_val': 'archive/validation/*.h5', 
            'archive_test': 'archive/test/*.h5',
            'scan_train': 'scan/train_scan/*.h5',
            'scan_val': 'scan/val_scan/*.h5',
            'scan_test': 'scan/test_scan/*.h5',
            'stare_train': 'stare/train_stare/*.h5',
            'stare_val': 'stare/val_stare/*.h5',
            'stare_test': 'stare/test_stare/*.h5',
        }
        import glob
        pattern = patterns.get(category, category)
        return sorted(glob.glob(str(self.root / pattern)))
    
    def get_stats(self, relative_path: str) -> Dict:
        """获取样本统计信息"""
        data, labels, meta = self.load_sample(relative_path)
        unique, counts = np.unique(labels, return_counts=True)
        return {
            'n_pulses': len(labels),
            'n_emitters': len(unique),
            'emitter_ids': unique.tolist(),
            'pulses_per_emitter': dict(zip(unique.tolist(), counts.tolist())),
            'imbalance_ratio': counts.max() / counts.min() if len(counts) > 1 else 0,
            'feature_stats': {
                name: {
                    'min': data[:, i].min(),
                    'max': data[:, i].max(),
                    'mean': data[:, i].mean(),
                    'std': data[:, i].std(),
                }
                for i, name in enumerate(FEATURE_NAMES)
            }
        }


if __name__ == '__main__':
    loader = TSRDLoader()
    
    # Example usage
    print("TSRD Data Loader 示例")
    print("=" * 50)
    
    # List available categories
    categories = ['archive_train', 'archive_test', 'scan_train', 'stare_train']
    for cat in categories:
        samples = loader.list_samples(cat)
        print(f"{cat}: {len(samples)} samples")
    
    # Load one sample and print stats
    print("\n加载 archive/test/test_0.h5:")
    stats = loader.get_stats('archive/test/test_0.h5')
    print(f"  脉冲数: {stats['n_pulses']}")
    print(f"  发射器数: {stats['n_emitters']}")
    print(f"  不平衡度: {stats['imbalance_ratio']:.1f}x")
