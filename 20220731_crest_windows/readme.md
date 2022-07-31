export FC=x86_64-w64-mingw32-gfortran CC=x86_64-w64-mingw32-gcc
meson setup _build --prefix=/home/(username)/bin/crest-2.12 -Dla_backend=openblas; meson install -C _build
