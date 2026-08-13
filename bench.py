import argparse
import time
import requests


def main():
    parser = argparse.ArgumentParser(
        description="HTTP server availability tester"
    )

    parser.add_argument(
        "-H",
        "--hosts",
        required=True,
        help="Список хостов через запятую"
    )

    parser.add_argument(
        "-C",
        "--count",
        type=int,
        default=1,
        help="Количество запросов к каждому хосту"
    )

    args = parser.parse_args()

    hosts = args.hosts.split(",")

    for host in hosts:
        print(f"\nHost: {host}")

        times = []
        success = 0
        failed = 0
        errors = 0

        for _ in range(args.count):
            try:
                start = time.perf_counter()

                response = requests.get(host, timeout=10)

                elapsed = time.perf_counter() - start
                times.append(elapsed)

                if 200 <= response.status_code < 400:
                    success += 1
                elif 400 <= response.status_code < 600:
                    failed += 1

            except requests.RequestException:
                errors += 1

        print(f"Success: {success}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")

        if times:
            print(f"Min: {min(times):.3f}s")
            print(f"Max: {max(times):.3f}s")
            print(f"Avg: {sum(times) / len(times):.3f}s")
        else:
            print("Min: N/A")
            print("Max: N/A")
            print("Avg: N/A")


if __name__ == "__main__":
    main()