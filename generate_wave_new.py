import os
import Cookie
def generate_wave(neu_n, cycle_n):
    pwd = os.path.abspath('.')
    file_header = []
    file_header.append(open(pwd + '\\wave\\sa0', 'wt'))
    for i in range(neu_n):
        path = pwd + '\\wave\\open%d' %(i + 1)
        file_header.append(open(path, 'wt'))
    period = 20e-6
    delay = (1- (1/4)) * period
    delta = period * 0.001


    sa0 = '0\t0\n'
    waveopen = ['0\t0\n' for i in range(neu_n)] 

    sa0 += '%.10f\t%f\n%.10f\t%f\n' %(delay, 0, delay + delta, 1.8)
    sa0 += '%.10f\t%f\n%.10f\t%f\n' %(period, 1.8, period + delta, 0)
    sa0 += '%.10f\t%f\n' %((neu_n*cycle_n + 1)* period, 0)    #7*100+1

    for i in range(cycle_n):
        for j in range(neu_n - 1):#should remove a line in last wave
            waveopen[j] += '%.10f\t%f\n%.10f\t%f\n' \
            %((neu_n*i + j + 1)*period + delay, 0, (neu_n * i + j + 1)*period + delay + delta, 1.8)
            waveopen[j] += '%.10f\t%f\n%.10f\t%f\n' \
            %((neu_n*i + j + 2)*period, 1.8, (neu_n*i + j + 2)*period + delta, 0)
            waveopen[j] += '%.10f\t%f\n' %((neu_n * i + neu_n + 1) * period, 0)
        waveopen[neu_n-1] += '%.10f\t%f\n%.10f\t%f\n' \
        %((neu_n*i + neu_n)*period + delay, 0, (neu_n * i + neu_n) * period + delay + delta, 1.8)
        waveopen[neu_n-1] += '%.10f\t%f\n%.10f\t%f\n' \
        %((neu_n*i + neu_n + 1)*period, 1.8, (neu_n * i + neu_n + 1) * period + delta, 0)

    file_header[0].write(sa0)
    file_header[0].close()
    for i in range(neu_n):
        file_header[i+1].write(waveopen[i])
        file_header[i+1].close()
generate_wave(49, 150)
