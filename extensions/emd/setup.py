from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'

setup(
    name='emd',
    ext_modules=[
        CUDAExtension('emd', [
            'emd.cpp',
            'emd_cuda.cu',
        ], extra_compile_args={
            'nvcc': [
                '-allow-unsupported-compiler',
                '-Xcompiler', '/wd4068',
                '-Xcompiler', '/wd4275',
                '-Xcompiler', '/wd4819',
                '-gencode', 'arch=compute_89,code=sm_89'
            ]
        }),
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
