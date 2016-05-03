PAYIN = 1
PAYOUT = 2
WEB_PAYIN = 3
WEB_PAYOUT = 4

lmap = {
    PAYIN: 'PAYIN',
    PAYOUT: 'PAYOUT',
    WEB_PAYIN: 'WEB_PAYIN',
    WEB_PAYOUT: 'WEB_PAYOUT',
}

lrev = dict((v, k) for k, v in lmap.items())
