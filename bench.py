import argparse
import re
import time

import requests


def is_valid_url(url):
    pattern = r"^https://[a-zA-Z0-9.-]+$"
    return re.match(pattern, url) is not None


def main():
    parser = argparse.ArgumentParser(
        description="HTTP server availability tester"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-H",
        "--hosts",
        help="Список хостов через запятую"
    )

    group.add_argument(
        "-F",
        "--file",
        help="Путь к файлу со списком хостов"
    )

    parser.add_argument(
        "-C",
        "--count",
        type=int,
        default=1,
        help="Количество запросов к каждому хосту"
    )

    parser.add_argument(
        "-O",
        "--output",
        help="Путь к файлу для сохранения результата"
    )

    args = parser.parse_args()

    if args.count <= 0:
        print("Ошибка: количество запросов должно быть больше 0")
        return

    # Получение списка хостов
    if args.hosts:
        hosts = args.hosts.split(",")

    else:
        try:
            with open(args.file, "r", encoding="utf-8") as file:
                hosts = [line.strip() for line in file if line.strip()]

        except FileNotFoundError:
            print(f"Ошибка: файл не найден: {args.file}")
            return

        except OSError as error:
            print(f"Ошибка при чтении файла: {error}")
            return

    results = []

    for host in hosts:
        host = host.strip()

        if not is_valid_url(host):
            results.append(
                f"Ошибка: неправильный формат адреса: {host}"
            )
            continue

        output = []
        output.append(f"Host: {host}")

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

        output.append(f"Success: {success}")
        output.append(f"Failed: {failed}")
        output.append(f"Errors: {errors}")

        if times:
            output.append(f"Min: {min(times):.3f}s")
            output.append(f"Max: {max(times):.3f}s")
            output.append(f"Avg: {sum(times) / len(times):.3f}s")

        else:
            output.append("Min: N/A")
            output.append("Max: N/A")
            output.append("Avg: N/A")

        results.append("\n".join(output))

    final_output = "\n\n".join(results)

    print(final_output)

    # Сохранение результата в файл
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(final_output + "\n")

            print(f"\nРезультат сохранён в файл: {args.output}")

        except OSError as error:
            print(f"Ошибка при сохранении файла: {error}")


if __name__ == "__main__":
    main()