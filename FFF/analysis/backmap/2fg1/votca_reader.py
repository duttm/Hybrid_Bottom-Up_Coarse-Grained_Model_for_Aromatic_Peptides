import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time


def main():
    # count the arguments
    arguments = len(sys.argv) - 1

    # output argument-wise

    ###### command line section ####################

    filename = sys.argv[1]
    print('filename is %s' % (filename))
    NOF = int(sys.argv[2])
    print('NOF is %s' % (NOF))
    a = int(sys.argv[3])
    print('No. of elements in a single frame is %s' % (a))
    v1 = int(sys.argv[4])  # number of coordinates in 1 molecule
    v2 = int(sys.argv[5])  # total number of molecules
    CG = int(sys.argv[
                 6])  # total number of CG residues in 1 molecule ( in C-V6K2-N , there are 10 residues , i.e 2 termmini, 6 valines and 2 lysines)
    ions = int(sys.argv[7])
    #####################################################################

    y = 0
    f = open(filename, "r")
    lines = f.readlines()

    result = []
    for x in lines:
        result.append(x)
        y = y + 1

    f.close()

    print(y)
    counter = 0
    refine = []
    x = 0

    while x <= (a + 3) * (NOF + 1):
        if x == 0 or x == 1:  # skip first 2 lines
            counter = counter + 1
            x = x + 1
            # print("x is %s and counter in %s in stage 1" % (x, counter))

        elif 2 <= counter <= a + 1:
            refine.append(result[x])
            x = x + 1
            counter = counter + 1
            # print("x is %s and counter in %s in stage 2" % (x, counter))

        elif counter == a + 2:
            counter = 2
            x = x + 3
            if x > y:
                break
            # print("x is %s and counter in %s in stage 3" % (x, counter))

        else:
            print(0)

    file_out = open("array.txt", "w")

    # admit values into a large 2D array

    rows, cols = (a * NOF, 4)
    array = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(a * NOF):
        # print(i)
        t = refine[i][0:8]
        id = refine[i][15:20]  # Column values may vary on the basis of gromacs version
        x = refine[i][21:28]
        y = refine[i][29:36]
        z = refine[i][37:44]
        array[i][0] = id
        array[i][1] = x
        array[i][2] = y
        array[i][3] = z

    for i in range(rows):
        file_out.writelines(str(array[i]) + '\n')
        # view array.txt to check
    file_out.close()

    # 2d big to 3D small conversion

    rows, cols, pages = (a, 4, NOF)
    array3d = [[[0 for k in range(pages)] for i in range(cols)] for j in range(rows)]

    h = 0

    for k in range(pages):
        for i in range(rows):
            array3d[i][0][k] = float(array[h][0])
            array3d[i][1][k] = float(array[h][1])
            array3d[i][2][k] = float(array[h][2])
            array3d[i][3][k] = float(array[h][3])
            h = h + 1

    ## Writing to gro format

    Col1 = ['NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1', 'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2', 'CA3', 'PHA3', 'PHB3', 'PHC3', 'COO']
    Col2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    Col3 = ['NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1', 'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2', 'CA3', 'PHA3', 'PHB3', 'PHC3', 'COO']
    Col4 = ['W']
    Col5 = ['SOL']
    Col6 = ['CL']
    from array import array

    D1 = array('i')
    D2 = []
    D3 = []
    D4 = array('i')
    D5 = array('d')
    D6 = array('d')
    D7 = array('d')

    l1 = 1
    m = 1
    h = 0
    for k in range(pages):

        for j in range(v2):
            for i in range(v1):
                D1.append(Col2[i])
                D2.append(Col1[i])
                D3.append(Col3[i])
                D4.append(m)
                D5.append(array3d[h][1][k])
                D6.append(array3d[h][2][k])
                D7.append(array3d[h][3][k])

                m = m + 1
                h = h + 1

        l1 = D1[v1*v2-1] + 1
        for i in range(v1 * v2, a-ions):
            D1.append(l1)
            D2.append(Col5[0])
            D3.append(Col4[0])
            D4.append(m)
            D5.append(array3d[i][1][k])
            D6.append(array3d[i][2][k])
            D7.append(array3d[i][3][k])

            m = m + 1
            l1 = l1 + 1

        for i in range(a - ions, a):
                D1.append(l1)
                D2.append(Col6[0])
                D3.append(Col6[0])
                D4.append(m)
                D5.append(array3d[i][1][k])
                D6.append(array3d[i][2][k])
                D7.append(array3d[i][3][k])

                m = m + 1
                l1 = l1 + 1

    file_write_water = open(str(v2)+"_CG_rewrite.gro", "w")

    # view upper_mono.txt to check

    file_write_water.writelines('we are making a grid' + '\n')
    file_write_water.write(str(m-1) + '\n')
    for k in range(m-1):
        file_write_water.writelines(
            '{:>5}'.format(str(D1[k])) + '{:>5}'.format(str(D2[k])) + '{:>5}'.format(str(D3[k])) + '{:>5}'.format(
                str(D4[k])) + '{:8.3f}'.format(D5[k]) + '{:8.3f}'.format(D6[k]) + '{:8.3f}'.format(D7[k]) + '\n')

    boxlength = float(lines[-1].split()[0])

#    file_write_water.writelines('{:8.3f}'.format(5.54793) + '{:8.3f}'.format(5.54793) + '{:8.3f}'.format(5.54793))
    file_write_water.writelines('{:8.3f}'.format(boxlength) + '{:8.3f}'.format(boxlength) + '{:8.3f}'.format(boxlength))
    file_write_water.close()

    ####### Lets read Dendron file ##############################


### Section for later use ######


class Bead(object):
    def __init__(self, id, x_dim, y_dim, z_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim


######################################################################

if __name__ == "__main__":
    main()
