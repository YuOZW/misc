import cryspy.scripts.cryspy
import pyxtal

class my_pyxtal(pyxtal.pyxtal):
   def __init__(
      self,
      molecular=True, # modified
      ):
      super().__init__(molecular=molecular)

   def from_random(
      self,
      dim = 3,
      group=None,
      species=None,
      numIons=None,
      factor=1.1,
      conventional = True,
      tm = None,
      ):
      super().from_random(
         dim = dim,
         group=group,
         species=species,
         numIons=numIons,
         factor=factor,
         conventional = conventional,
         tm = tm,
         use_hall = True, # modified
         )

if __name__ == '__main__':
   pyxtal.pyxtal = my_pyxtal
   cryspy.scripts.cryspy.main()