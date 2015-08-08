def logo():
    print ''
    print '==================================================================='
    print '                                                                   '
    print '  oooooo   oo   oo  oooooo    ooooo    o     o  ooooooo   oooooo   '
    print '  8     8   o   o   8     8  8     8   8   oo   8         8     8  '
    print '  8     8    o o    8     8  8     8   8  oo    8         8     8  '
    print '  8ooooo      8     8ooooo   8     8   8 oo     8ooooooo  8ooooo   '
    print '  8           8     8        8     8   8   o    8         8   o    '
    print '  8           8     8        8     8   8    o   8         8    o   '
    print '  8           8     8         ooooo    8     o  oooooooo  8     o  '
    print '                                                                   '
    print '==================================================================='
    print ''

def round_info(cur_round, max_round, players, sb_pos):
    """ SAMPLE ROUND INFORMATION

    print ''
    print ' -- Next Round Information --'
    print '============================================'
    print ' ROUND  : 2 / 100'
    print ' PLAYER : akita san ( $1999 ) <- SMALL BLIND'
    print '        :  buri san ( $1999 ) <- RETIRED    '
    print '        :     c san ( $1999 ) '
    print ''
    print '============================================'
    print ''

    """
    def print_line(title, content):
        print '{0:>7} : {1:<10}'.format(title, content)

    badge_counter = 0
    badge = ["SMALL BLIND", "BIG BLIND", "RETIRED"] # Now big blind is not used
    print ''
    print ' -- Next Round Information --'
    print '================================================='
    print_line("ROUND", "{0} / {1}".format(cur_round, max_round))
    for i in range(len(players)):
        p = players[i]
        content = "{0:<10} ( ${1:^5} )".format(p.NAME, p.stack)
        if p.stack == 0: content = "{0} <- {1:<10}".format(content, badge[2])
        elif i == sb_pos: content = "{0} <- {1:<10}".format(content, badge[0])
        print_line("PLAYER", content)
    print '================================================='
    print ''
