# cache-latency

From the repository root:

```bash
./sweep-se.sh
python3 scripts/plot_results.py cache-latency
```

See [experiment methods](../README.md) for variables, measurements, interpretation, and DRAM mapping caveats. Outputs go to `results/cache-latency/`, which is excluded from Git; generated plots go to `assets/plots/`.
