from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        "_cgobigger",
        ["_cgobigger/bind.cpp"],
        # Example: passing in the version to the compiled code
        include_dirs = ['_cgobigger/',
                        '/opt/homebrew/Cellar/boost/1.76.0/include'],
    ),
]

setup(
    name="gobigger",
    version=__version__,
    author="zhangming",
    author_email="zhangming@sensetime.com",
    url="https://github.com/opendilab/GoBigger",
    description="GoBigger based on c++",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    packages=[
        'gobigger',
        'gobigger.server',
        'gobigger.utils',
        'gobigger.agents',
        'gobigger.bin',
        'gobigger.render',
    ],
    install_requires=[
        'easydict',
        'gym>=0.15.3',  # pypy incompatible
        'pygame>=2.0.0',
        'pytest>=5.0.0',
        'opencv-python',
        'numpy>=1.10, <= 1.19',
        'pybind11>=2.6.0',
    ]
)
