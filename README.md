# render-app-backend
Python / Django REST Framework / Blender / Celery

## Install bpy package

### Install actual drivers & packages

#### TBB (Thearding Building Blocks) & Embree

install first TBB:

```bash
echo "deb http://cz.archive.ubuntu.com/ubuntu eoan main universe" | sudo tee -a  /etc/apt/sources.list
sudo apt update
sudo apt install libtbb-dev

sudo apt-get install aptitude
sudo aptitude install libboost-all-dev
```

and Embree

```bash
git clone https://github.com/embree/embree.git
```

#### OpenEXR (and others blender packages)

download actual version from: https://www.openexr.com/downloads.html

unpack tar.gz archive and install package like this:

```bash
cmake openexr-<your_version>
make
make install
```

### Build blender

get raw blender from repository:

```bash
git clone https://git.blender.org/blender.git
cd blender
git submodule update --init --recursive
git submodule foreach git checkout master
git submodule foreach git pull --rebase origin master
```

and run buildier:

```bash
./blender/build_files/build_environment/install_deps.sh
```
