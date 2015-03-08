import os

def weight_pn(neu_n):
    netlist = 'subckt weight_pn '
    for i in range(1, neu_n+1):
        for j in range(1, neu_n+1):
            netlist += 'w%d_%d_pn ' %(i, j)
    netlist += '\n'
    v_n = 1
    for i in range(1, neu_n+1):
        for j in range(1, neu_n+1):
            netlist += 'V%d (w%d_%d_pn v_shift) vsource dc=v_w%d_%d_pn type=dc\n' \
            %(v_n, i, j, i, j)
            v_n += 1
    netlist += 'V%d (v_shift 0) vsource dc=0 type=dc\nends weight_pn\n' %(v_n)
    return netlist

# wd = open('C:\\Users\\Charles\\Desktop\\netlist\\weight_pn.txt','w')
# wd.write(weight_pn(7))
# wd.close()

def clk_module(neu_n):
    netlist = 'subckt clk_module '
    for i in range(1, neu_n+1):
        netlist += 'open%d ' %(i)
    netlist += 'sa0\n'
    for i in range(1, neu_n+1):
        netlist += 'V%d (open%d vbias) vsource \\\n\
    file="./wave/open%d" type=pwl\n' %(i, i, i)
    i += 1
    netlist += 'V%d (sa0 vbias) vsource\\\n\
        file="/home/users/wjj/Project/finalnetlist/wave/sa0" type=pwl\n' %(i)
    netlist += 'V%d (vbias 0) vsource dc=-900m type=dc\nends clk_module\n' %(i+1)
    return netlist

#wd = open('C:\\Users\\Charles\\Desktop\\netlist\\clk_module.txt','w')
#wd.write(clk_module(7))
#wd.close()

def adder_schematic(neu_n):
    netlist = 'subckt adder_schematic '
    for i in range(1, neu_n+2):#include vth
        netlist += 'vin%d ' %(i)
    netlist += 'vout vdd vss\nI0 (vss vdd net2 net1 vout) op\n'
    for i in range(1, neu_n+2):
        netlist += 'R%d (vin%d net1) resistor r=500K\n' %(i, i)
    
    i += 1
    netlist += 'R%d (net1 0) resistor r=500K\n' %(i)
    i += 1
    netlist += 'R%d (net2 vout) resistor r=500K\n' %(i)
    i += 1
    netlist += 'R%d (net2 0) resistor r=%fK\n' %(i, 500/(neu_n + 1))
    netlist += 'ends adder_schematic\n'
    return netlist

# wd = open('C:\\Users\\Charles\\Desktop\\netlist\\adder_schematic.txt','w')
# wd.write(adder_schematic(7))
# wd.close()

def synapse(neu_n):
    netlist = 'subckt synapse '
    for i in range(1, neu_n+1):
        netlist += 'ADD%d ' %(i)
    for i in range(1, neu_n+1):
        netlist += 'CON%d ' %(i)
    netlist += 'VOUT VTH vdd vss\n'
    ins_n = 0
    netlist += 'I%d (' %(ins_n)
    ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'vin%d ' %(i)
    netlist += 'VTH VOUT vdd vss) adder_schematic\n'
    for i in range(1, neu_n+1):
        netlist += 'I%d (CON%d CON%d_N vdd vss) not\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (ADD%d net%d vdd vss) buffer\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (net%d net1_%d vdd vss) inverter\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (CON%d net%d vin%d vdd vss) tran_gate\n' %(ins_n, i, i, i)
        ins_n += 1
        netlist += 'I%d (CON%d_N net1_%d vin%d vdd vss) tran_gate\n' %(ins_n, i, i, i)
        ins_n += 1
    netlist += 'ends synapse\n'
    return netlist
# wd = open('C:\\Users\\Charles\\Desktop\\netlist\\synapse.txt','w')
# wd.write(synapse(7))
# wd.close()

def res_matrix(neu_n):
    res_n = 1
    netlist = ''
    for i in range(1, neu_n+1):
        for j in range(1, neu_n+1):
            netlist += 'R%d (x%d x%d_%d) resistor r=3M\n' %(res_n, j, i, j)
            res_n += 1
            r_lable = '%d_%d' %(i, j)
            netlist += 'R%d (0 x%d_%d) resistor r=res_%s\n' %(res_n, i, j, r_lable)
            res_n += 1
    return netlist

# wd = open('C:\\Users\\Charles\\Desktop\\netlist\\res_matrix.txt','w')
# wd.write(res_matrix(7))
# wd.close()

def main_list(neu_n):
    ins_n = 0
    vol_n = 0
    netlist = 'I%d (' %(ins_n)
    ins_n += 1
    for i in range(1, neu_n+1):
        for j in range(1, neu_n+1):
            netlist += 'w%d_%d_pn ' %(i, j)
    netlist += ') weight_pn\nI%d (' %(ins_n)
    ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'open%d ' %(i)
    netlist += 'sa0) clk_module\n'
    for i in range(1, neu_n+1):
        netlist += 'V%d (net%d 0) vsource dc=v_init%d type=dc\n' %(vol_n, i, i)
        vol_n += 1
    netlist += 'V%d (VTH 0) vsource dc=vth type=dc\n' %(vol_n)
    vol_n += 1
    netlist += 'V%d (vss 0) vsource dc=-900m type=dc\n' %(vol_n)
    vol_n += 1
    netlist += 'V%d (vdd 0) vsource dc=900m type=dc\n' %(vol_n)
    vol_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (' %(ins_n)
        for j in range(1, neu_n+1):
            netlist += 'x%d_%d ' %(i, j)
        for j in range(1, neu_n+1):
            netlist += 'w%d_%d_pn ' %(i, j)
        netlist += 'net_syn%d VTH vdd vss) synapse\n' %(i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (0 net_syn%d net_cmp%d vdd vss) cmp\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (N%d x%d vdd vss) storage\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (sa0 net%d N%d vdd vss) tran_gate\n' %(ins_n, i, i)
        ins_n += 1
    for i in range(1, neu_n+1):
        netlist += 'I%d (open%d net_cmp%d N%d vdd vss) tran_gate\n' %(ins_n, i, i, i)
        ins_n += 1
    return netlist
# wd = open('C:\\Users\\Charles\\Desktop\\netlist\\main_list.txt','w')
# wd.write(main_list(7))
# wd.close()

def ckt_para(weight_m, vth, start_state):
    netlist = 'parameters vth=%dm ' %(vth)
    neu_n = len(weight_m)
    for i in range(neu_n):
        for j in range(neu_n):
            if weight_m[i][j] >= 0:
                netlist += 'v_w%d_%d_pn=0.9 ' %(i+1, j+1)
            else:
                netlist += 'v_w%d_%d_pn=-0.9 ' %(i+1, j+1)
    for i in range(neu_n):
        if start_state[i] > 0:
            netlist += 'v_init%d=0.9 ' %(i+1)
        else:
            netlist += 'v_init%d=-0.9 ' %(i+1)
    for i in range(neu_n):
        for j in range(neu_n):
            netlist += 'res_%d_%d=%fk ' %(i+1, j+1, abs(weight_m[i][j]))
    netlist += '\n'
    return netlist

def makenetlist(vth):
    pwd = os.path.abspath('.')
    netlist = '// Generated for: spectre\n\
// Generated on: Feb 10 10:48:34 2015\n\
// Design library name: hopfiled7\n\
// Design cell name: hopfield\n\
// Design view name: schematic\n\
simulator lang=spectre\n\
global 0\n\
include "/home/EDA/Cadence/CDS/IC5141USR6/tools/dfII/samples/artist/ahdlLib/quantity.spectre"\n'
    read_hder1 = open(pwd+'\\ckt_matrix.txt', 'r')
    matrix_strrow = read_hder1.readline()[:-1].split('\t')
    neu_n = len(matrix_strrow)
    weight_m = [[0 for col in range(neu_n)] for row in range(neu_n)]
    for i in range(neu_n):
        for j in range(neu_n):
            weight_m[i][j] = float(matrix_strrow[j])
        matrix_strrow = read_hder1.readline()[:-1].split('\t')
    read_hder1.close()
    read_hder2 = open(pwd+'\\init_state.txt', 'r')
    init_state_strrow = read_hder2.readline()[:-1].split('\t')
    init_state = [int(init_s) for init_s in init_state_strrow]
    read_hder2.close()
    netlist += ckt_para(weight_m, vth, init_state)
    netlist += 'include "/home/Process/GSMC_018_2014/Models\\\
/PSP/v1.9/spectre/corners/corners.scs" section=nominal\n'
    netlist += weight_pn(neu_n)
    netlist += clk_module(neu_n)
    read_hder1 = open(pwd+'\\cmp.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    read_hder1 = open(pwd+'\\op.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    netlist += adder_schematic(neu_n) 
    read_hder1 = open(pwd+'\\not.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    read_hder1 = open(pwd+'\\inverter.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    read_hder1 = open(pwd+'\\buffer.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    read_hder1 = open(pwd+'\\tran_gate.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    netlist += synapse(neu_n)      
    read_hder1 = open(pwd+'\\storage.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()
    netlist += main_list(neu_n)
    netlist += res_matrix(neu_n)
    read_hder1 = open(pwd+'\\simulaoroptions.txt', 'r')
    netlist += read_hder1.read()
    read_hder1.close()

    point2save = 'save '
    for i in range(neu_n):
        point2save += 'N%d open%d ' %(i+1, i+1)
    point2save += 'sa0\nsaveOptions options save=selected\n'
    netlist += point2save
    return netlist


pwd = os.path.abspath('.')
wd = open(pwd+'\\final_netlist', 'w')
wd.write(makenetlist(5))
wd.close()