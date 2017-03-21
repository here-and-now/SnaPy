from cx_Freeze import setup, Executable

setup(name = "reandurllib" ,
      version = "0.1" ,
      description = "" ,
      options={"build_exe": {"packages":["pygame"]}},
      executables = [Executable("Snake.py")])