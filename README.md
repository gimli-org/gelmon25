# A short-course on versatile processing and inversion of geoelectrical monitoring data
## Material for a [pyGIMLi][pg] short course at the 7<sup>th</sup> international workshop on geoelectrical monitoring ([GELMON 2025][gelmon])

**Instructors:**
Florian Wagner<sup>1</sup>,
Thomas Günther<sup>2 (3)</sup>,
Nico Skibbe<sup>3</sup>,
and
Nino Menzel<sup>1</sup>

> <sup>1</sup>
> Geophysical Imaging and Monitoring, RWTH Aachen University, Germany
> <br>
> <sup>2</sup>
> Institute for Geophysics and Geoinformatics, TU Bergakademie Freiberg, Germany
> <br>
> <sup>3</sup>
> LIAG Institute for Applied Geophysics, Hannover, Germany
> <br>

## About

The [7<sup>th</sup> international workshop on geoelectrical monitoring (GELMON 2025)][gelmon] will be held in Vienna February 17<sup>th</sup> - 20<sup>th</sup> 2025.
This will include a pyGIMLi workshop on open-source and versatile processing and time-lapse inversion of geoelectrical monitoring data.

> [!NOTE]  
> Please note that this repository currently serves as a placeholder. More information on the workshop content including slides and Jupyter Notebooks are currently being prepared and will be made available here in early 2025.

As preparation, you might want to have a look at the existing tutorials from SWUNG meetings and SEG webinars:
* [Transform 2021](https://github.com/gimli-org/transform2021): Geophysical modelling & inversion with pyGIMLi I
* [Transform 2022](https://github.com/gimli-org/transform2022): Geophysical modelling & inversion with pyGIMLi II
* [SEG Webinar 2024](https://github.com/gimli-org/SEGwebinar): pyGIMLi - Open-source Research & Teaching Software

all of them accompagnied with Youtube videos and Jupyter Notebooks.
Some of these tutorials already cover the TOPIC of ERT using the [ERT module](https://www.pygimli.org/pygimliapi/_generated/pygimli.physics.ert.html)
On the [pyGIMLi website](https://www.pygimli.org), there are quite a few [ERT examples](https://www.pygimli.org/_examples_auto/index.html#electrical-resistivity-tomography), of which, however only one is about timelapse ERT. There is another repository, https://github.com/gimli-org/timelapseERT to collect datasets and corresponding notebooks using the `TimelapseERT` class from the ERT module.

## Installation

We recommend installing a Python distribution locally.
In case of installation problems, one can alternatively use Google Colab.
The current `pyGIMLi` version is 1.5.3

### Local Python installation using conda

We recommend installing a Python distribution like [miniforge][miniforge].
- Install miniforge: https://github.com/conda-forge/miniforge#install
- follow the installation instructions on https://www.pygimli.org/installation.html
- open a terminal (on Windows: Powershell prompt)

```
conda create -n pg -c gimli -c conda-forge pygimli=1.5 jupyter
```

or download the file https://github.com/gimli-org/gelmon25/environment.yml

```
conda env create --file environment.yml
```

Activate the environment and call Jupyter Notebook:

```
conda activate pg
jupyter notebook
```

### Installation using pip

We also provide a pip installer so that you can install pygimli in an existing installation

```
pip install pygimli
```

### Google colab

After login in to Colab, just type 

```
!pip install pygimli
```

[gelmon]: https://www.geophysik.at/gelmon/
[pg]: https://www.pygimli.org
