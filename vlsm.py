import ipaddress

req = {'Engineering': 101, 'Sales': 51, 'Marketing': 13,
       'HR': 11, 'Servers': 6, 'WAN1': 2, 'WAN2': 2, 'WAN3': 2}

def prefix_for(n):
    bits = 2
    while 2 ** bits - 2 < n:
        bits += 1
    return 32 - bits

base = ipaddress.ip_network('192.168.10.0/24')
cursor = int(base.network_address)
plan = []
for name, need in sorted(req.items(), key=lambda x: -x[1]):
    net = ipaddress.ip_network((cursor, prefix_for(need)))
    if net.subnet_of(base) is False:
        raise SystemExit('Out of address space for ' + name)
    plan.append((name, net, need))
    cursor = int(net.broadcast_address) + 1

nets = [p[1] for p in plan]
assert not any(a.overlaps(b) for i, a in enumerate(nets) for b in nets[i + 1:])

allocated = sum(n.num_addresses for n in nets)
required = sum(req.values())
for name, net, need in plan:
    print(name, net, net.netmask, 'usable', net.num_addresses - 2, 'need', need)
print('Allocated', allocated, 'Required', required)
print('AUE %.2f%%' % (100 * required / allocated))
print('Remaining in base:', base.num_addresses - allocated)

print('A allocated', 256 * len(req), 'AUE %.2f%%' % (100 * required / (256 * len(req))))
print('B allocated', 128 * len(req), 'AUE %.2f%%' % (100 * required / (128 * len(req))))