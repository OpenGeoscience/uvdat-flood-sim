from setuptools import setup, find_packages

setup(
    name='uvdat_flood_sim',
    version='1.0.0',
    author='Anne Haley',
    author_email='anne.haley@kitware.com',
    description='Flood Simulation written in collaboration with August Posch at Northeastern University',
    url='https://github.com/OpenGeoscience/uvdat-flood-sim',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'requests',
        'rasterio',
        'pandas',
        'scikit-learn==1.3.0',
        'numpy<2',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
