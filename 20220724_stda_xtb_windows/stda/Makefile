
PROG    = stda

FC = x86_64-w64-mingw32-gfortran
  
LINKER = $(FC) -static -fopenmp -I"C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\include"
LIBS = "C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\lib\libopenblas.a" "C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\lib\libopenblas.dll.a"
  
FFLAGS = -O3 -fopenmp -I"C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\include" -ffixed-line-length-80

#################################################
OBJS=\
     stdacommon.o stringmod.o main.o pckao.o \
     header.o intpack.o velo.o  \
     onetri.o prmat.o readl.o block.o\
     stda.o stda-rw.o sutda.o sfstda.o srpapack.o intslvm.o io.o\
     linal.o readbasa.o readbasmold.o printvec.o normalize.o\
     apbtrafo.o sosor.o readxtb.o linear_response.o molden.o print_nto.o
#################################################

%.o: %.f90
	@echo "making $@ from $<"
	$(FC) $(FFLAGS) -c $< -o $@
%.o: %.f
	@echo "making $@ from $<"
	$(FC) $(FFLAGS) -c $< -o $@

$(PROG):     $(OBJS) 
		@echo  "Loading $(PROG) ... "
		@$(LINKER) $(OBJS) $(LIBS) -o $(PROG)

clean:
	rm -f *.o *.mod $(PROG)
