""" Generate gifs of the circular and rectangular membranes

"""
from membrane import CircularMembrane, RectangularMembrane
from visualization import animate_membrane

for m in range(3):
    for n in range(3):
        mem = CircularMembrane(1, 1, m, n+1)
        mem.normalize(A=0.5)
        animate_membrane(
            f"circular{m}{n+1}.gif", mem,
            periods=1,
            runtime=2,
            video_size=(800,800),
            video_dpi=128
        )

for m in range(3):
    for n in range(3):
        mem = RectangularMembrane(1, 2, m+1, n+1, 1, A=0.5)
        animate_membrane(
            f"rectangular{m+1}{n+1}.gif", mem,
            periods=1,
            runtime=2,
            video_size=(1600,1600),
            video_dpi=400
        )