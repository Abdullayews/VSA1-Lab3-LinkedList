import csv
import os
import platform
import statistics
import sys
import time

from pharmacy_queue import PharmacyQueue
from bus_stop import BusStop

SIZES = [100, 1000, 10000]
REPEATS = 5
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test_results")


def timed(fn):
    t = time.perf_counter()
    fn()
    return (time.perf_counter() - t) * 1000.0


def median_ms(fn_setup, fn_run):
    vals = []
    for _ in range(REPEATS):
        ctx = fn_setup()
        vals.append(timed(lambda: fn_run(ctx)))
    return statistics.median(vals)


def bench_pharmacy():
    rows = []
    for n in SIZES:
        add = median_ms(PharmacyQueue,
                        lambda q: [q.addCustomer(f"Customer{i}", "Parol") for i in range(n)])

        def setup():
            q = PharmacyQueue()
            for i in range(n):
                q.addCustomer(f"Customer{i}", "Parol")
            return q

        serve = median_ms(setup, lambda q: [q.serveCustomer() for _ in range(n)])
        rows.append([n, round(add, 4), round(serve, 4)])
    return rows


def bench_busstop():
    rows = []
    for n in SIZES:
        def add_all(stop):
            for i in range(n):
                stop.addPassenger(f"P{i}", 70 if i % 4 == 0 else 30)

        add = median_ms(BusStop, add_all)

        def setup():
            stop = BusStop()
            for i in range(n):
                stop.addPassenger(f"P{i}", 70 if i % 4 == 0 else 30)
            return stop

        board = median_ms(setup, lambda stop: [stop.boardPassenger() for _ in range(n)])
        rows.append([n, round(add, 4), round(board, 4)])
    return rows


def save(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("\n" + name)
    print(" | ".join(header))
    for r in rows:
        print(" | ".join(str(x) for x in r))


def plot(name, title, xlabel, ylabel, header, rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.font_manager as fm
        for fp in ["/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            if os.path.exists(fp):
                fm.fontManager.addfont(fp)
        import matplotlib.pyplot as plt
        plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Noto Sans SC"]
        plt.rcParams["axes.unicode_minus"] = False
    except ImportError:
        print("matplotlib tapılmadı: pip install matplotlib")
        return
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    colors = ["#6B9DAD", "#C49B72", "#7BA68A", "#B87472"]
    xs = [r[0] for r in rows]
    for i in range(1, len(header)):
        ax.plot(xs, [r[i] for r in rows], marker="o", linewidth=2,
                label=header[i], color=colors[i - 1 % len(colors)])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.savefig(os.path.join(OUT, name), dpi=200, facecolor="white")
    plt.close(fig)


def main():
    print("Sistem məlumatları (avtomatik):")
    print("OS:", platform.platform())
    print("CPU:", platform.processor() or platform.machine())
    print("Python:", sys.version.split()[0], platform.python_implementation())
    print("CPU cores:", os.cpu_count())
    print("RAM, GPU, Computer Model, Storage, Power Mode: manual doldurun")

    h1 = ["Element sayı", "Add (ms)", "Serve (ms)"]
    r1 = bench_pharmacy()
    save("task1_pharmacy.csv", h1, r1)
    plot("task1_graph.png", "Aptek növbəsi (FIFO Queue)",
         "Element sayı", "İcra müddəti (ms)", h1, r1)

    h2 = ["Element sayı", "Add (ms)", "Board (ms)"]
    r2 = bench_busstop()
    save("task2_busstop.csv", h2, r2)
    plot("task2_graph.png", "Avtobus dayanacağı (prioritetli növbə)",
         "Element sayı", "İcra müddəti (ms)", h2, r2)


if __name__ == "__main__":
    main()
