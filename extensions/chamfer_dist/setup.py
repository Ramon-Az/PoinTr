# -*- coding: utf-8 -*-
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

os.environ['TORCH_CUDA_ARCH_LIST'] = '12.0'

setup(name='chamfer',
      version='2.0.0',
      ext_modules=[
          CUDAExtension('chamfer', [
              'chamfer_cuda.cpp',
              'chamfer.cu',
          ], extra_compile_args={
              'nvcc': [
                  '-allow-unsupported-compiler',
                  '-std=c++17',
                  '-Xcompiler', '/wd4068',
                  '-Xcompiler', '/wd4275',
                  '-Xcompiler', '/wd4819',
                  '-gencode', 'arch=compute_89,code=sm_120'
              ],
              'cxx': ['/std:c++17', '/Zc:preprocessor', '/W0']
          }),
      ],
      cmdclass={'build_ext': BuildExtension})
