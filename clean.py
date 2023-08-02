import os
def run_clean(mydir):
  for f in os.listdir(mydir):
      if not f.endswith(".mp4"):
          continue
      os.remove(os.path.join(mydir, f))