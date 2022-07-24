
PROG    = g_spec

OSTYPE=LINUXI
#--------------------------------------------------------------------------

#-------------------------------------------------------------------------

FC = x86_64-w64-mingw32-gfortran
  
LINKER = $(FC) -static -fopenmp -I"C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\include"
LIBS = "C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\lib\libopenblas.a" "C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\lib\libopenblas.dll.a"
  
FFLAGS = -O3 -fopenmp -I"C:\cygwin64\home\(username)\bin\OpenBLAS-0.3.17\include" -ffixed-line-length-80

#################################################
OBJS=\
     g_spec.o 
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
	rm -f *.o $(PROG)
