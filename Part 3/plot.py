import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

CSV_FILE = 'edges_aggregated.csv'
TARGET_CHR = '8'

edges = []
with open(CSV_FILE) as f:
   reader = csv.DictReader(f)
   for row in reader:
       chrom_s, pos_s = row['Start'].split(':')
       chrom_e, pos_e = row['End'].split(':')
       # Normalize chromosome string
       chrom_s = chrom_s.replace('chr', '')
       chrom_e = chrom_e.replace('chr', '')
       if chrom_s == chrom_e == TARGET_CHR:
           start = int(pos_s)
           end = int(pos_e)
           edges.append((min(start, end), max(start, end)))


if not edges:
   print(f"No intrachromosomal edges found on chr{TARGET_CHR}")
else:
   # Determine plotting region
   starts = [s for s, e in edges]
   ends = [e for s, e in edges]
   region_start = min(starts)
   region_end = max(ends)


   # Arc height (constant) and center position for arcs
   height = (region_end - region_start) / 20
   center_y = height / 2



   fig, ax = plt.subplots(figsize=(10, 4))
   ax.set_xlim(region_start, region_end)
   ax.set_ylim(0, height * 1.2)
   ax.set_xlabel('Genomic position on chr8')
   ax.set_yticks([])


  
   ax.hlines(0, region_start, region_end, color='black', linewidth=2)


   fgfr1_pos = 38300000
   ax.axvline(fgfr1_pos, color='grey', linestyle='--')
   ax.text(fgfr1_pos, height * 1.1, 'FGFR1', ha='center', va='bottom')


   for start, end in edges:
       width = end - start
       mid = (start + end) / 2
       arc = Arc((mid, center_y), width, height, theta1=0, theta2=180, alpha=0.3)
       ax.add_patch(arc)


   ax.set_title('Aggregated SV Arcs Layered on chr8')
   plt.tight_layout()
   plt.show()
