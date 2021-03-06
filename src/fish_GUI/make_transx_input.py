# download data from Fendl 3.1b
import os
import argparse as ap
import glob

"""
def download_data(datapath):
    print('Downloading Fendl 3.1b data to ./data/')
    os.system(
        "wget https://www-nds.iaea.org/fendl/data/neutron/fendl31b-neutron-matxs.zip")
    print('Extracting Data')
    os.system("unzip fendl31b-neutron-matxs.zip -d {}".format(datapath))
    os.system("rm fendl31b-neutron-matxs.zip")
"""


def card1():
    c = " /transx input/\n"
    return(c)


def card2(n_TF, g_TF):
    # use default values
    IPRINT = 0
    IOUT = 4
    IPROB = 0

    ISET = ""
    if n_TF:
        ISET += "1"
    if g_TF:
        ISET += "2"

    IFORM = 1
    ITIME = 1
    IDECAY = 0
    ITRC = 0
    ICOLL = 0
    INITF = 0

    c = " {0} {1} {2} {3} {4}    {5} {6} {7} {8} {9}/\n".format(IPRINT, IOUT, IPROB,
                                                                ISET, IFORM, ITIME,
                                                                IDECAY, ITRC, ICOLL,
                                                                INITF)

    return c


def card3(datapath, n_TF, g_TF, count1, count2, count3, count4):

    # NGROUP = neutron + gamma
    any_file = os.listdir(datapath)[0]
    f = open('{}/{}'.format(datapath, any_file), "r")
    for i in range(0, 8):
        line = f.readline()

    if n_TF:
        n_group = int(line.split()[0])
    else:
        n_group = 0

    if g_TF:
        g_group = int(line.split()[1])
    else:
        g_group = 0

    # negative indicates that data will be read from the directory
    NGROUP = -(n_group + g_group)

    # NL = ??
    NL = count3

    # NUP = ??
    NUP = 0

    # NTHG = ??
    NTHG = 0

    # NMIX = number of mixes (ie number of *.m files)
    NMIX = count1

    # NREG - number of regions, assume 1 (need extra add)
    NREG = NMIX

    # NMIXS = number of mix specifications
    NMIXS = count2

    # NED = number of extra edits, always assume 7 for heat, kerma, dame, dpa,
    # t, he, and h
    NED = count4

    # NEDS = equals the number of entries for the edits
    NEDS = NED

    # NTABL = ??
    NTABL = abs(NGROUP) + NED + NUP + 3

    c = " {0} {1} {2} {3} {4}   {5} {6} {7} {8} {9}/\n".format(NGROUP, NL,
                                                               NTABL, NUP,
                                                               NTHG, NMIX,
                                                               NREG, NMIXS,
                                                               NED, NEDS)
    c += " */home/maps/matxsdata/*/\n"
    return c


def card4(list1):
    # For every .m file in the datapath, reads line 1 to get name
    c = ""
    names = []
    """
    for filename in sorted(os.listdir(datapath)):
        # read line 1
        path = '{}/{}'.format(datapath, filename)
        f = open(path, 'r')
        line = f.readline()
        name = line.split('*')[1][9:].strip()
        c += name + " "
        names.append(name)
        f.close()

    c = c.rstrip() + "\n"
    """
    for mat in list1:
        name = mat
        c += " " + str(name) + "\n"
        names.append(name)
    return c, names


def card5(count):
    c = ""
    for i in range(1, count + 1):
        c += ' r{} /\n'.format(i)
    return c


def card6():
    # only have values when abs(INTIF>=12)
    pass


def card7(names, n):
    c = ""
    for mix in names:
        c += " {}    {}    {}/\n".format(n + 1, n + 1, mix)

    return c


def card8(names):
    c = ''
    for exs in names:
        c += ' {}\n'.format(exs)
    return c


def card9(names):
    c = ''
    for i, exs in enumerate(names):
        c += ' {}  {}  /\n'.format(i + 1, exs)
    return c


"""
def card8():
    # Add something to make these edits optional?
    HED = ['heat', 'kerma', 'dame', 'dpa', 't', 'he', 'h']
    c = '{0} {1} {2} {3} {4} {5} {6}\n'.format(HED[0], HED[1], HED[2], HED[3],
                                               HED[4], HED[5], HED[6])
    return c, HED


def card9(datapath, HED, n_TF, g_TF):
    c = ""
    count = 0

    for i, edit in enumerate(HED):

        # assume all mixes are used in heat with standard multiplier
        if edit == 'heat':
            # check if writing for neutron, gammas, or both
            if n_TF:
                c += '{} heat/\n'.format(i + 1)
                count += 1
            if g_TF:
                c += '{} gheat/\n'.format(i + 1)
                count += 1

        # assume all mixes are used in kerma with standard multiplier
        elif edit == 'kerma':
            # check if writing for neutron, gammas, or both
            if n_TF:
                c += '{} kerma/\n'.format(i + 1)
                count += 1
            if g_TF:
                c += '{} gheat/\n'.format(i + 1)
                count += 1

        elif edit == 'dame':
            c += '{} dame/\n'.format(i + 1)
            count += 1

        # assume all mixes are used in dame with standard multiplier
        elif edit == 'dpa':
            # right now, this is just what has always been used
            c += '4 dame .0129 be9/\n'
            c += '4 dame .0129 c12/\n'
            c += '4 dame .016 na23/\n'
            count += 3

            #c += '4 dame .016 mgnat/\n'
            c += '4 dame .016 mg23/\n'
            c += '4 dame .016 mg24/\n'
            c += '4 dame .016 mg25/\n'
            c += '4 dame .016 mg26/\n'
            count += 4

            c += '4 dame .0148 al27/\n'
            c += '4 dame .016 si28/\n'
            c += '4 dame .016 si29/\n'
            c += '4 dame .016 si30/\n'
            count += 4

            #c += '4 dame .01 knat/\n'
            c += '4 dame .01 k39/\n'
            c += '4 dame .01 k40/\n'
            c += '4 dame .01 k41/\n'
            count += 3

            #c += '4 dame .01 canat/\n'
            c += '4 dame .01 ca40/\n'
            c += '4 dame .01 ca42/\n'
            c += '4 dame .01 ca43/\n'
            c += '4 dame .01 ca44/\n'
            c += '4 dame .01 ca46/\n'
            c += '4 dame .01 ca48/\n'
            count += 6

            c += '4 dame .01 ti46/\n'
            c += '4 dame .01 ti47/\n'
            c += '4 dame .01 ti48/\n'
            c += '4 dame .01 ti49/\n'
            c += '4 dame .01 ti50/\n'
            count += 5

            #c += '4 dame .01 vnat/\n'
            c += '4 dame .01 v50/\n'
            c += '4 dame .01 v51/\n'
            count += 2

            c += '4 dame .01 cr50/\n'
            c += '4 dame .01 cr52/\n'
            c += '4 dame .01 cr53/\n'
            c += '4 dame .01 cr54/\n'
            count += 4

            c += '4 dame .01 mn55/\n'
            count += 1

            c += '4 dame .01 fe54/\n'
            c += '4 dame .01 fe56/\n'
            c += '4 dame .01 fe57/\n'
            c += '4 dame .01 fe58/\n'
            count += 4

            c += '4 dame .01 co59/\n'
            count += 1

            c += '4 dame .01 ni58/\n'
            c += '4 dame .01 ni60/\n'
            c += '4 dame .01 ni61/\n'
            c += '4 dame .01 ni62/\n'
            c += '4 dame .01 ni64/\n'
            count += 5

            c += '4 dame .01 cu63/\n'
            c += '4 dame .01 cu65/\n'
            count += 2

            #c += '4 dame .01 zrnat/\n'
            c += '4 dame .01 zr90/\n'
            c += '4 dame .01 zr91/\n'
            c += '4 dame .01 zr92/\n'
            c += '4 dame .01 zr94/\n'
            c += '4 dame .01 zr96/\n'
            count += 5

            c += '4 dame .01 nb93/\n'
            count += 1

            c += '4 dame .00667 mo92/\n'
            c += '4 dame .00667 mo94/\n'
            c += '4 dame .00667 mo95/\n'
            c += '4 dame .00667 mo96/\n'
            c += '4 dame .00667 mo97/\n'
            c += '4 dame .00667 mo98/\n'
            c += '4 dame .00667 mo100/\n'
            count += 7

            c += '4 dame .00444 ta181/\n'
            count += 1

            c += '4 dame .00444 w182/\n'
            c += '4 dame .00444 w183/\n'
            c += '4 dame .00444 w184/\n'
            c += '4 dame .00444 w186/\n'
            count += 4

            c += '4 dame .01333 au197/\n'
            c += '4 dame .016 pb206/\n'
            count += 2

            c += '4 dame .016 pb207/\n'
            c += '4 dame .016 pb208/\n'
            count += 2

        elif edit == 't':
            c += '{} * .h3*/\n'.format(i + 1)
            count += 1

        elif edit == 'he':
            c += '{} * .he3*/\n'.format(i + 1)
            c += '{} * .he4*/\n'.format(i + 1)
            count += 2

        elif edit == 'h':
            c += '{} * .h1*/\n'.format(i + 1)
            c += '{} * .h2*/\n'.format(i + 1)
            c += '{} * .h3*/\n'.format(i + 1)
            count += 3

    return c, count


def card10():
    pass


def card11():
    pass
"""

"""
def main():
    # NEED TO MAKE THE OPTION TO CHOOSE NEUTRON, GAMMA, OR BOTH

    ### DOWNLOAD & EXTRACT DATA ###
    datapath = './data/'

    # check if data folder already exist
    if os.path.isdir(datapath):
        # if folder is empty download data
        if not os.listdir(datapath):
            download_data(datapath)
        else:
            # assume data exists
            print("Data already exists in ./data/. Will not download.")
    else:
        # Folder does not exist so create folder
        os.system("mkdir data")
        # get data
        download_data(datapath)

    # BBC

    ### CREATE INPUT ###
    # create a string for each card individually

    # card 1 - Title
    c1 = card1()

    # card 2 - Options
    # make optional card arguments, otherwise defaults?
    c2 = card2(n_TF, g_TF)

    # card 4 - Mix Names
    c4, names = card4(datapath)

    c5 = card5()

    c6 = card6()

    c7 = card7(names)

    c8, HED = card8()

    c9, count = card9(datapath, HED, n_TF, g_TF)

    # card 3 - Parameters
    # This has to be done after the rest maybe?
    c3, NMIX = card3(datapath, n_TF, g_TF, count)

    total = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + 'stop'
    input_file = open("input.txt", "w")
    input_file.write(total)
    input_file.close()


if __name__ == "__main__":
    main()
"""
