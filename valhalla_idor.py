import requests
import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor

# 🎯 Banner estilo ferramenta
def banner():
    print(r"""
 __     __    _ _           _ _       
 \ \   / /_ _| | |__   __ _| | | ___  
  \ \ / / _` | | '_ \ / _` | | |/ _ \ 
   \ V / (_| | | | | | (_| | | | (_) |
    \_/ \__,_|_|_| |_|\__,_|_|_|\___/ 
                                     
 Valhalla IDOR Scanner 🔥
    """)

# 🔐 Hash da resposta
def get_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

# 🔍 Teste de ID
def test_id(args, i, baseline_hash):
    try:
        if args.method == "GET":
            response = requests.get(
                args.url.format(i),
                headers=args.headers,
                proxies=args.proxy,
                timeout=5
            )
        else:
            data = args.data.replace("{}", str(i))
            response = requests.post(
                args.url,
                headers=args.headers,
                data=data,
                proxies=args.proxy,
                timeout=5
            )

        content = response.text
        current_hash = get_hash(content)

        # 🔎 Diferença detectada
        if response.status_code == 200 and current_hash != baseline_hash:

            # 🔍 Filtro por palavras-chave
            if args.keyword:
                if args.keyword.lower() not in content.lower():
                    return None

            print(f"[!] IDOR? ID={i} | Status={response.status_code} | Size={len(content)}")
            return f"ID={i} | Size={len(content)}"

    except:
        pass

    return None


def main():
    banner()

    parser = argparse.ArgumentParser(description="Valhalla IDOR Scanner")

    parser.add_argument("-u", "--url", required=True, help="URL alvo (use {} no ID)")
    parser.add_argument("-m", "--method", default="GET", choices=["GET", "POST"])
    parser.add_argument("-d", "--data", help="Body para POST (use {} para ID)")
    parser.add_argument("-s", "--start", type=int, default=1)
    parser.add_argument("-e", "--end", type=int, default=100)
    parser.add_argument("-t", "--threads", type=int, default=20)
    parser.add_argument("-H", "--header", action="append")
    parser.add_argument("-k", "--keyword", help="Filtrar por palavra-chave")
    parser.add_argument("-p", "--proxy", help="Proxy (ex: http://127.0.0.1:8080)")
    parser.add_argument("-o", "--output", help="Salvar resultado")

    args = parser.parse_args()

    # 🔧 Headers
    args.headers = {}
    if args.header:
        for h in args.header:
            key, value = h.split(":", 1)
            args.headers[key.strip()] = value.strip()

    # 🔌 Proxy
    if args.proxy:
        args.proxy = {
            "http": args.proxy,
            "https": args.proxy
        }

    # 🔍 Baseline
    print("[+] Coletando baseline...")
    if args.method == "GET":
        baseline = requests.get(args.url.format(args.start), headers=args.headers)
    else:
        data = args.data.replace("{}", str(args.start))
        baseline = requests.post(args.url, headers=args.headers, data=data)

    baseline_hash = get_hash(baseline.text)

    print("[+] Iniciando scan...\n")

    results = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(test_id, args, i, baseline_hash)
            for i in range(args.start, args.end + 1)
        ]

        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    # 💾 Output
    if args.output:
        with open(args.output, "w") as f:
            for r in results:
                f.write(r + "\n")

        print(f"\n[+] Salvo em: {args.output}")

    print("\n[+] Scan finalizado 🔥")


if __name__ == "__main__":
    main()