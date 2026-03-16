# -*- coding: utf-8 -*-
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

os.environ['TORCH_CUDA_ARCH_LIST'] = '8.9'

setup(name='gridding',
      version='2.1.0',
      ext_modules=[
          CUDAExtension('gridding', ['gridding_cuda.cpp', 'gridding.cu', 'gridding_reverse.cu'], 
                       extra_compile_args={
                           'nvcc': [
                               '-allow-unsupported-compiler',
                               '-Xcompiler', '/wd4068',
                               '-Xcompiler', '/wd4275',
                               '-Xcompiler', '/wd4819',
                               '-gencode', 'arch=compute_89,code=sm_89'
                           ]
                       }),
      ],
      cmdclass={'build_ext': BuildExtension})
