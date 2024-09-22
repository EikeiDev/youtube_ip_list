from ipaddress import ip_address, IPv4Address, summarize_address_range

type IPList = list[IPv4Address]


def read_ips(ipv4List: list[IPv4Address]):
    with open('ipv4_list.txt', mode='r', encoding='utf-8') as f:
        for ip in f.readlines():
            ip = ip.strip()
            try:
                ip = ip_address(ip)
                if isinstance(ip, IPv4Address):
                    ipv4List.append(ip)
            except ValueError:
                if ip != '':
                    print('%s is not a valid IPv4 address!' % ip)


def makeCIDRRangesList(ipList: list[IPv4Address], maskLastNBits=8):
    maskLen = 1 << maskLastNBits

    def getFirstLastIps(ip):
        isIPv4 = isinstance(ip, IPv4Address)
        mask = (1 << 32) - maskLen
        first = int(ip) & mask
        first = IPv4Address(first)
        return first, first + (maskLen - 1)

    CIDRRangesList = []

    firstip, lastip = getFirstLastIps(ipList[0])
    for ip in ipList:
        if ip <= lastip:
            continue

        if int(ip) - int(lastip) < maskLen:
            _, lastip = getFirstLastIps(ip)
            continue

        CIDRRangesList += summarize_address_range(firstip, lastip)
        firstip, lastip = getFirstLastIps(ip)

    CIDRRangesList += summarize_address_range(firstip, lastip)
    return CIDRRangesList


def main():
    ipv4List: list[IPv4Address] = []

    # Чтение IPv4-адресов из файла
    read_ips(ipv4List)

    # Создание списка CIDR диапазонов для IPv4
    cidr4 = makeCIDRRangesList(ipv4List)

    # Запись CIDR диапазонов для IPv4 в файл
    with open('cidr4.txt', mode='w', encoding='utf-8') as f:
        f.write('\n'.join(map(str, cidr4)) + '\n')


if __name__ == '__main__':
    main()
