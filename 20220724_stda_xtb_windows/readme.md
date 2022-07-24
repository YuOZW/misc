## Cygwin
以下のライブラリが必要
- git
- make
- ruby
- mingw64-x86_64-gcc-core
- mingw64-x86_64-gcc-fortran

## OpenBLAS
https://github.com/xianyi/OpenBLAS
```
make CC=x86_64-w64-mingw32-gcc FC=x86_64-w64-mingw32-gfortran
mkdir ~/bin/OpenBLAS-0.3.17
make PREFIX=~/bin/OpenBLAS-0.3.17 install
```

## xtb4stda
https://github.com/grimme-lab/xtb4stda  

`MAKE`フォルダ内の`Makerules`と`xtb4stda.objs`を置き換え、ファイル内の`(username)`を自分のPC用に書き換えて`make`をタイプ
  
`xtb4stda.exe`のあるディレクトリを環境変数`PATH`に追加  
`.param_`から始まるファイルと`.xtb4stdarc`を含むディレクトリを環境変数`XTB4STDAHOME`に設定  

## stda
https://github.com/grimme-lab/stda  

`Makefile`を置き換え、ファイル内の`(username)`を自分のPC用に書き換えて`make`をタイプ  
`g_spec`フォルダ内でも同様に`Makefile`を置き換え、ファイル内の`(username)`を自分のPC用に書き換えてmake`をタイプ  
  
`stda.exe`と`g_spec.exe`のあるディレクトリを環境変数`PATH`に追加  
