class HandEvaluator:

  ONEPAIR = 1<<8
  TWOPAIR = 1<<9
  THREECARD = 1<<10
  STRAIGHT = 1<<11
  FLASH = 1<<12
  FULLHOUSE = 1<<13
  FOURCARD = 1<<14
  STRAIGHTFLASH = 1<<15

  HANDRANK_MAP = {
      0:'NO PAIR',
      ONEPAIR:'ONE PAIR',
      TWOPAIR:'TWO PAIR',
      THREECARD:'THREE CARD',
      STRAIGHT:'STRAIGHT',
      FLASH:'FLASH',
      FULLHOUSE:'FULLHOUSE',
      FOURCARD:'FOUR CARD',
      STRAIGHTFLASH:'STRAIGHT FLASH'
      }

  def maskHand(self, bit):
    return bit & 511<<8 # 511 = (1<<9)-1

  def maskHighRank(self, bit):
    return (bit & 15<<4)>>4 # 15 = (1<<4)-1

  def maskLowRank(self, bit):
    return bit & 15 # 15 = (1<<4)-1

  """
  # BELOW EXAMPLE IS WRONG AFTER FOURCARD
  return format
  [BIT flg of hand][rank1(4bit)][rank2(4bit)]
  ex.)
    no-pair hole card 3,4    =>           100 0101
    one pair of rank 3       =>        1 0011 0000
    two pair of rank 4,A     =>       10 1110 0100
    three card of rank 9     =>      100 1001 0000
    four card of rank 2      =>     1000 0010 0000
    straight of rank 10      =>    10000 1010 0000
    flash of rank 5          =>   100000 0101 0000
    fullhouse of rank 3,4    =>  1000000 0100 0011
    straight flash of rank 7 => 10000000 0111 0000
  """
  def evalHand(self, holl, community):
    cards = holl + community
    r1 = self.checkStraightFlash(cards)
    if r1 != -1: return self.STRAIGHTFLASH | r1<<4
    flg,r1,r2 = self.checkFullHouse(cards)
    if flg: return self.FULLHOUSE | r1<<4 | r2
    r1 = self.checkFlash(cards)
    if r1 != -1: return self.FLASH | r1<<4
    r1 = self.checkStraight(cards)
    if r1 != -1: return self.STRAIGHT | r1<<4
    r1 = self.checkFourCard(cards)
    if r1 != -1: return self.FOURCARD | r1<<4
    r1 = self.checkFlash(cards)
    if r1 != -1: return self.FLASH | r1<<4
    r1 = self.checkThreeCard(cards)
    if r1 != -1: return self.THREECARD | r1<<4
    flg, r1, r2 = self.checkTwoPair(cards)
    if flg: return self.TWOPAIR | r1<<4 | r2
    r1 = self.checkOnePair(cards)
    if r1 != -1: return self.ONEPAIR | r1<<4
    return self.checkHighCard(holl)

  """
  return rank of two holl card
  higher one is upper 4 bit
  lower one is lower 4bit
  """
  def checkHighCard(self, hole):
    if len(hole) == 0: return 0
    r1 = hole[0].getRank()
    r2 = hole[1].getRank()
    return max(r1,r2)<<4|min(r1,r2)



  """
  return rank of pair or -1 if no one-pair
  """
  def checkOnePair(self, cards):
    rank = -1
    memo = 0 # bit memo
    for card in cards:
      mask = 1<<card.getRank()
      if memo & mask != 0:
        rank = max(rank, card.getRank())
      memo |= mask
    return rank

  """
  return (flg, rank1, rank2)
  flg : True/False if TwoPair exists
  rank1 : higher rank of pair
  rank2 : lower rank of pair
  """
  def checkTwoPair(self, cards):
    rank1, rank2 = -1, -1
    memo = 0 # bit memo
    for card in cards:
      mask = 1<<card.getRank()
      if memo & mask != 0:
        tmp = card.getRank()
        if tmp >= rank1:
          rank2 = rank1
          rank1 = tmp
        elif tmp > rank2:
          rank2 = tmp
      memo |= mask
    return rank2>0, rank1, rank2

  """
  return rank of three card.
  if found multiple, return higher one
  if not found return -1
  """
  def checkThreeCard(self, cards):
    rank = -1
    memo = 0 # use 3 bit for each rank to count
    for card in cards:
      memo += 1<<((card.getRank()-1)*3)
    for i in range(2,15):
      memo >>= 3
      count = memo & 7
      if count >= 3: # not "=" but ">=" is for FullHouse check 
        rank = max(rank, i)
    return rank

  def checkFourCard(self, cards):
    rank = -1
    memo = 0 # use 3 bit for each rank to count
    for card in cards:
      memo += 1<<((card.getRank()-1)*3)
    for i in range(2,15):
      memo >>= 3
      count = memo & 7
      if count >= 4: # not "=" but ">=" is for FullHouse check 
        rank = max(rank, i)
    return rank


  def checkStraight(self, cards):
    rank = -1
    memo = 0
    for card in cards:
      memo |= 1<<card.getRank()
    memo >>= 2
    count = 0
    for k in range(2,16): # 16 is for the case when rank is 14(highest card is A).
      if memo&1:
        count += 1
      else:
        if count >= 5:
          rank = k-1
        count = 0
      memo>>=1
    return rank

  def checkFlash(self, cards):
    memo = 0 # use 3-bit for each suit(3*4 bit-string)
    for card in cards:
      if card.getSuit() == 2: # CLUB
        memo += 1
      elif card.getSuit() == 4: # DIAMOND
        memo += 1<<3
      elif card.getSuit() == 8: # HEART
        memo += 1<<6
      else:
        memo += 1<<9
    rank = -1
    for i in range(4):
      if memo&7 >=5:
        suit = 2<<i
        for card in cards:
          if card.getSuit() == suit:
            rank = max(rank, card.getRank())
        break
      memo >>=3
    return rank

  def checkFullHouse(self, cards):
    # check three cards
    r1 = self.checkThreeCard(cards)
    if r1 == -1:
      return False, -1, -1
    # check one pair which has different rank from three cards
    r2 = -1
    memo = 0 # bit memo
    for card in cards:
      mask = 1<<card.getRank()
      if memo & mask != 0 and card.getRank()!=r1:
        r2 = max(r2, card.getRank())
      memo |= mask
    return r2>0, r1, r2

  def checkStraightFlash(self, cards):
    # devide cards by their suit
    c,d,h,s = [],[],[],[]
    for card in cards:
      suit = card.getSuit()
      array = c if suit == 2 else d if suit == 4 \
          else h if suit == 8 else s
      array.append(card)
    # check straight for each suit
    rank = -1
    for cards in [c,d,h,s]:
      if len(cards) >= 5:
        res = self.checkStraight(cards)
        if res != -1:
          rank = max(rank, res)
    return rank
