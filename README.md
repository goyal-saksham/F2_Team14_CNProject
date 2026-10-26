# Comparative Analysis of Classful vs. Classless IPv4 Addressing Efficiency for Subnetting in a Simulated Enterprise Network

**Course:** BCSE308P, Computer Networks (Project)
**Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology
**Tools:** Cisco Packet Tracer, Python 3

| Team member | Registration no. |
|---|---|
| Sahaj Madan | 24BCT0099 |
| Saksham Goyal | 24BCE0306 |

---

## 1. Overview

A fixed IPv4 block can be divided in different ways, and the choice decides how many addresses are wasted, how many routes routers must carry, and how easily the network can grow. This project builds **one enterprise network** (3 routers, 5 department LANs, 3 WAN links) in Cisco Packet Tracer and addresses it **three ways**, keeping the topology and host requirements identical:

| Scenario | Addressing | Parent block | Routing |
|---|---|---|---|
| **A** | Pure classful: one Class C (/24) per segment | 192.168.x.0/24 (8 networks) | RIPv1 |
| **B** | Classful with FLSM: equal /25 subnets everywhere | 172.16.0.0/16 | RIPv1 |
| **C** | Classless VLSM/CIDR: prefix sized to each segment | 192.168.10.0/24 | RIPv2 (no auto-summary), plus an OSPF variant |

The scenarios are compared on address utilization, routing behavior, failure recovery and growth.

## 2. Enterprise requirements

| Segment | Router | Hosts | Required addresses (hosts + gateway) |
|---|---|---|---|
| Engineering | R1 | 100 | 101 |
| Servers | R1 | 5 | 6 |
| Sales | R2 | 50 | 51 |
| Marketing | R2 | 12 | 13 |
| HR | R3 | 10 | 11 |
| WAN1 (R1-R2) | link | 2 routers | 2 |
| WAN2 (R2-R3) | link | 2 routers | 2 |
| WAN3 (R1-R3) | link | 2 routers | 2 |
| **Total** | | | **188** |

## 3. Topology

Three Cisco 2911 routers form a triangle through serial links (R1 is HQ, R2 and R3 are branches). Each LAN has a Cisco 2960 switch with 2 test PCs, and the Servers LAN also has a file server.

| Link | Connection |
|---|---|
| Engineering LAN | R1 Gi0/0 |
| Servers LAN | R1 Gi0/1 |
| Sales LAN | R2 Gi0/0 |
| Marketing LAN | R2 Gi0/1 |
| HR LAN | R3 Gi0/0 |
| WAN1 | R1 S0/0/0 (DCE) to R2 S0/0/0 |
| WAN2 | R2 S0/0/1 (DCE) to R3 S0/0/1 |
| WAN3 | R1 S0/0/1 (DCE) to R3 S0/0/0 |

The base topology is in `base.pkt` and the screenshot is `Evidence/1. base_topology.png`.

## 4. Address plans

### Scenario C: VLSM (192.168.10.0/24)

| Segment | Prefix | Network | Usable range | Gateway |
|---|---|---|---|---|
| Engineering | /25 | 192.168.10.0 | .1 - .126 | .1 |
| Sales | /26 | 192.168.10.128 | .129 - .190 | .129 |
| Marketing | /28 | 192.168.10.192 | .193 - .206 | .193 |
| HR | /28 | 192.168.10.208 | .209 - .222 | .209 |
| Servers | /29 | 192.168.10.224 | .225 - .230 | .225 |
| WAN1 | /30 | 192.168.10.232 | .233 - .234 | - |
| WAN2 | /30 | 192.168.10.236 | .237 - .238 | - |
| WAN3 | /30 | 192.168.10.240 | .241 - .242 | - |

The reserved space is 192.168.10.244 - .255 (12 addresses).

### Scenario B: FLSM (172.16.0.0/16 split into /25)

Engineering 172.16.0.0/25, Sales 172.16.0.128/25, Marketing 172.16.1.0/25, HR 172.16.1.128/25, Servers 172.16.2.0/25, WAN1 172.16.2.128/25, WAN2 172.16.3.0/25, WAN3 172.16.3.128/25.

### Scenario A: pure classful

Engineering 192.168.1.0/24, Sales 192.168.2.0/24, Marketing 192.168.3.0/24, HR 192.168.4.0/24, Servers 192.168.5.0/24, WAN1 192.168.11.0/24, WAN2 192.168.12.0/24, WAN3 192.168.13.0/24.

## 5. Results

### 5.1 Address efficiency

Address Utilization Efficiency (AUE) = required addresses / allocated addresses x 100.

| Metric | A: Classful | B: Classful FLSM | C: Classless VLSM |
|---|---|---|---|
| Addresses allocated | 2048 | 1024 | 244 |
| Addresses required | 188 | 188 | 188 |
| **AUE** | **9.18%** | **18.36%** | **77.05%** |
| Wastage | 1860 | 836 | 56 |
| Space saved vs A | - | 50.0% | 88.1% |
| Space saved vs B | - | - | 76.2% |

### 5.2 Convergence after a WAN failure

The R1-R3 link (WAN3) was shut during a continuous ping from an Engineering PC to an HR PC. The values are lost pings before recovery, after removing the first-ping ARP timeout. One lost ping is roughly one second.

| Configuration | Trial 1 | Trial 2 | Trial 3 | Average | Range |
|---|---|---|---|---|---|
| A: Classful, RIPv1 | 2 | 14 | 15 | 10.3 | 2 to 15 |
| B: Classful FLSM, RIPv1 | 17 | 8 | 5 | 10.0 | 5 to 17 |
| C: Classless VLSM, RIPv2 | 5 | 11 | 11 | 9.0 | 5 to 11 |
| C: Classless VLSM, OSPF | 1 | 1 | 2 | 1.3 | 1 to 2 |

The same table is in `Evidence/Configuration.docx`.

### 5.3 Key findings

- **VLSM uses far less space.** Scenario C allocates 244 addresses against 2048 for pure classful and 1024 for FLSM, for the same 188-address requirement.
- **RIPv1 cannot carry VLSM.** With the Scenario C addresses under RIPv1, R1's table lost the Sales, Marketing and HR routes (5 `C` and `R` entries remained against 8 under RIPv2), as `BRK1_R1_route_broken` shows. RIPv2 or OSPF is required.
- **Addressing does not change convergence speed.** A, B and C-RIPv2 all average about 9 to 10 lost pings, because they share RIP's 30-second update timer. The routing protocol matters: OSPF recovered in about 1 to 2 lost pings.
- **Reading `show ip route`.** Packet Tracer counts the local `L` /32 entries in the header. R1 in Scenario C reports 12 subnets and 6 masks, which is 8 real subnets with 5 different prefix lengths plus 4 local /32 entries.

## 6. Repository contents

```
CN Project/
├── README.md
├── base.pkt                  Cabled topology, no addressing
├── A_classful.pkt            Scenario A: pure classful + RIPv1
├── B_flsm.pkt                Scenario B: classful FLSM + RIPv1
├── C_vlsm.pkt                Scenario C: VLSM + RIPv2 (with DHCP)
├── C_vlsm_ospf.pkt           Scenario C: OSPF variant
├── C_break1.pkt              Break test 1: VLSM under RIPv1
├── C_break2.pkt              Break test 2: discontiguous network, auto-summary
├── A_isp.pkt                 Scenario A with an ISP router (edge summarization)
├── C_isp.pkt                 Scenario C with an ISP router (edge summarization)
├── vlsm.py                   Python VLSM allocator and efficiency calculator
├── CN_Project_Presentation.pptx
└── Evidence/                 Numbered screenshots and the convergence table
```

### Evidence index

| Numbers | Content |
|---|---|
| 1 | Base topology |
| 2 - 7 | Scenario A: topology, interfaces, routing tables, protocols, ping, tracert |
| 8 - 13 | Scenario B: the same set |
| 14 - 22 | Scenario C: topology, interfaces, routes, RIP config, pings, DHCP |
| 23 - 24 | OSPF neighbors and routes |
| 25 - 28 | Break test 1: RIPv1 with VLSM, broken and fixed |
| 29 - 32 | Break test 2: auto-summary on a discontiguous layout, broken and fixed |
| 33 - 36 | Convergence ping runs (A, B, C-RIPv2, C-OSPF) |
| 37 | Python tool output |

## 7. How to run

### Packet Tracer files

1. Install Cisco Packet Tracer (8.x recommended) and open any `.pkt` file.
2. Wait about a minute for RIP or OSPF to converge, then open a router's CLI tab.
3. Useful checks:

```
show ip interface brief
show ip route
show ip protocols
show ip ospf neighbor     (OSPF file only)
show ip dhcp binding      (Scenario C)
```

4. From a PC's Command Prompt, ping other LANs, for example from Engineering to HR in Scenario C: `ping 192.168.10.210`.

To repeat the convergence test, run `ping -t` from an Engineering PC to an HR PC, then shut `interface serial0/0/1` on R1 and count the lost pings.

### Python tool

Requires Python 3.7 or newer.

```
python3 vlsm.py
```

The script reads the requirements from the `req` dictionary at the top of the file, allocates subnets largest-first inside 192.168.10.0/24, checks for overlaps and prints the efficiency figures. Expected end of output:

```
Allocated 244 Required 188
AUE 77.05%
Remaining in base: 12
A allocated 2048 AUE 9.18%
B allocated 1024 AUE 18.36%
```

The script is a design calculator. It does not read the `.pkt` files, so compare its subnet list with the routing tables in the Evidence folder to confirm that the configured network matches the plan.

## 8. Limitations

- Each LAN has only 2 test PCs, so subnet capacity is shown by calculation rather than simulated with full host counts.
- Packet Tracer timings are indicative, not production-equivalent. One ping per second cannot resolve outages shorter than about a second, and the OSPF row rests on three short trials.
- The Guest Wi-Fi and R&D growth figures (512, 256 and 40 addresses for A, B and C) are analytical and were not simulated.
- IPv6 and physical hardware are out of scope.

## 9. Future work

- IPv6 dual-stack addressing plan.
- Generate router configs automatically from the Python plan.
- VLANs with router-on-a-stick.
- Access lists aligned to subnet boundaries.
- More convergence trials and larger topologies.
- Alternative weightings for the composite efficiency score.

## 10. References

1. RFC 791, Internet Protocol.
2. RFC 950, Internet Standard Subnetting Procedure.
3. RFC 1519 and RFC 4632, Classless Inter-Domain Routing (CIDR).
4. RFC 1058 and RFC 2453, RIP versions 1 and 2.
5. RFC 2328, OSPF Version 2.
6. RFC 1918, Address Allocation for Private Internets.
