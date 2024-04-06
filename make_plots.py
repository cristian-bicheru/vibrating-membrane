from membrane import CircularMembrane, RectangularMembrane
from visualization import plot_membrane_peak

for m in range(3):
    for n in range(3):
        mem = CircularMembrane(1, 1, m, n+1)
        mem.normalize(A=0.5)
        plot_membrane_peak(f"circular{m}{n+1}.png", mem)

for m in range(3):
    for n in range(3):
        mem = RectangularMembrane(1, 2, m+1, n+1, 1, A=0.5)
        plot_membrane_peak(f"rectangular{m+1}{n+1}.png", mem)