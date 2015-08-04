import unittest
from engine.ui.hand_evaluator import HandEvaluator
from engine.ui.card import Card

class HnadEvalTest(unittest.TestCase):

  def setUp(self):
    self.E = HandEvaluator()

  def testHighCard(self):
    hole = []
    r = self.E.checkHighCard(hole)
    r1 = (r & (15<<4))>>4
    r2 = r & 15
    self.assertEqual(0, r1)
    self.assertEqual(0, r2)


    hole = [Card(3,4),Card(9,2)]
    r = self.E.checkHighCard(hole)
    r1 = (r & (15<<4))>>4
    r2 = r & 15
    self.assertEqual(9, r1)
    self.assertEqual(3, r2)

    hole = [Card(2,4),Card(2,2)]
    r = self.E.checkHighCard(hole)
    r1 = (r & (15<<4))>>4
    r2 = r & 15
    self.assertEqual(2, r1)
    self.assertEqual(2, r2)

  def testHandStrength(self):
    community = [Card(3,4),Card(5,4),Card(7,2),Card(6,4),Card(10,2)]
    hole1 = [Card(2,4),Card(9,2)] # no pair
    hole2 = [Card(3,4),Card(8,2)] # one pair
    s1 = self.E.evalHand(hole1, community)
    s2 = self.E.evalHand(hole2, community)
    self.assertTrue(s1<s2)

    community = [Card(3,4),Card(5,4),Card(7,2),Card(6,4),Card(10,2)]
    hole1 = [Card(4,4),Card(9,2)] # straight
    hole2 = [Card(8,4),Card(9,2)] # straight
    s1 = self.E.evalHand(hole1, community)
    s2 = self.E.evalHand(hole2, community)
    self.assertTrue(s1<s2)

    community = [Card(3,4),Card(3,4),Card(3,2),Card(6,4),Card(10,2)]
    hole1 = [Card(4,4),Card(6,2)] # full house
    hole2 = [Card(3,4),Card(9,2)] # four card
    s1 = self.E.evalHand(hole1, community)
    s2 = self.E.evalHand(hole2, community)
    self.assertTrue(s1<s2)
    

  def testEvalHand(self):
    # no pair
    community = [Card(3,2),Card(5,4),Card(7,2),Card(6,4),Card(10,2)]
    hole = [Card(2,4),Card(9,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(0, self.E.maskHand(bit))
    self.assertEqual(9, self.E.maskHighRank(bit))
    self.assertEqual(2, self.E.maskLowRank(bit))

    # one pair
    community = [Card(3,4),Card(5,4),Card(7,2),Card(6,4),Card(10,2)]
    hole = [Card(3,4),Card(9,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.ONEPAIR, self.E.maskHand(bit))
    self.assertEqual(3, self.E.maskHighRank(bit))
    # two pair
    community = [Card(3,4),Card(2,4),Card(7,2),Card(5,4),Card(9,2)]
    hole = [Card(3,4),Card(9,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.TWOPAIR, self.E.maskHand(bit))
    self.assertEqual(9, self.E.maskHighRank(bit))
    self.assertEqual(3, self.E.maskLowRank(bit))
    # three card
    community = [Card(3,4),Card(5,4),Card(7,2),Card(6,4),Card(3,2)]
    hole = [Card(3,4),Card(9,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.THREECARD, self.E.maskHand(bit))
    self.assertEqual(3, self.E.maskHighRank(bit))
    # four card
    community = [Card(5,4),Card(5,4),Card(7,2),Card(5,4),Card(2,2)]
    hole = [Card(3,4),Card(5,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.FOURCARD, self.E.maskHand(bit))
    self.assertEqual(5, self.E.maskHighRank(bit))
    # straight
    community = [Card(6,4),Card(5,4),Card(7,2),Card(2,4),Card(3,2)]
    hole = [Card(5,4),Card(4,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.STRAIGHT, self.E.maskHand(bit))
    self.assertEqual(7, self.E.maskHighRank(bit))
    # flash
    community = [Card(6,4),Card(5,4),Card(7,2),Card(2,4),Card(3,4)]
    hole = [Card(5,4),Card(4,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.FLASH, self.E.maskHand(bit))
    self.assertEqual(6, self.E.maskHighRank(bit))
    # fullhouse
    community = [Card(6,4),Card(5,4),Card(4,2),Card(2,4),Card(4,4)]
    hole = [Card(5,4),Card(4,2)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.FULLHOUSE, self.E.maskHand(bit))
    self.assertEqual(4, self.E.maskHighRank(bit))
    self.assertEqual(5, self.E.maskLowRank(bit))
    # straight flush
    community = [Card(11,8),Card(5,4),Card(13,8),Card(12,8),Card(4,4)]
    hole = [Card(10,8),Card(14,8)]
    bit = self.E.evalHand(hole, community)
    self.assertEqual(self.E.STRAIGHTFLASH, self.E.maskHand(bit))
    self.assertEqual(14, self.E.maskHighRank(bit))


  def testOnePair(self):
    cards = [Card(2,2),Card(2,4),Card(3,4),Card(5,4),Card(7,2),Card(3,4),Card(9,2)]
    res = self.E.checkOnePair(cards)
    self.assertEqual(3, res)
    cards = [Card(7,2),Card(2,4),Card(7,4),Card(9,4),Card(7,2),Card(3,4),Card(3,2)]
    res = self.E.checkOnePair(cards)
    self.assertEqual(7, res)
    cards = [Card(2,2),Card(6,4),Card(11,4),Card(5,4),Card(7,2),Card(3,4),Card(9,2)]
    res = self.E.checkOnePair(cards)
    self.assertEqual(-1, res)

  def testTwoPair(self):
    cards = [Card(4,2),Card(4,4),Card(3,4),Card(3,4),Card(7,2),Card(3,4),Card(9,2)]
    flg, r1, r2 = self.E.checkTwoPair(cards)
    self.assertEqual(4, r1)
    self.assertEqual(3, r2)
    cards = [Card(2,2),Card(7,4),Card(3,4),Card(3,4),Card(7,2),Card(3,4),Card(2,2)]
    flg, r1, r2 = self.E.checkTwoPair(cards)
    self.assertEqual(7, r1)
    self.assertEqual(3, r2)
    cards = [Card(2,2),Card(2,4),Card(4,4),Card(5,4),Card(7,2),Card(3,4),Card(9,2)]
    flg, r1, r2 = self.E.checkTwoPair(cards)
    self.assertFalse(flg)

  def testThreeCard(self):
    cards = [Card(2,2),Card(6,4),Card(11,4),Card(5,4),Card(2,4),Card(3,4),Card(2,8)]
    res = self.E.checkThreeCard(cards)
    self.assertEqual(2, res)
    cards = [Card(2,2),Card(7,4),Card(3,4),Card(3,4),Card(7,2),Card(3,4),Card(2,2)]
    res = self.E.checkThreeCard(cards)
    self.assertEqual(3, res)
    cards = [Card(3,2),Card(7,4),Card(3,4),Card(3,4),Card(7,2),Card(3,4),Card(2,2)]
    res = self.E.checkThreeCard(cards)
    self.assertEqual(3, res)

  def testStraight(self):
    cards = [Card(4,2),Card(6,4),Card(11,4),Card(5,4),Card(2,4),Card(3,4),Card(2,8)]
    res = self.E.checkStraight(cards)
    self.assertEqual(6, res)
    cards = [Card(10,2),Card(12,4),Card(11,4),Card(13,4),Card(14,4),Card(3,4),Card(2,8)]
    res = self.E.checkStraight(cards)
    self.assertEqual(14, res)
    cards = [Card(2,2),Card(12,4),Card(11,4),Card(13,4),Card(14,4),Card(3,4),Card(2,8)]
    res = self.E.checkStraight(cards)
    self.assertEqual(-1, res)
    cards = [Card(2,2),Card(3,4),Card(7,4),Card(4,4),Card(8,4),Card(6,4),Card(5,8)]
    res = self.E.checkStraight(cards)
    self.assertEqual(8, res)

  def testFlash(self):
    cards = [Card(2,2),Card(12,4),Card(11,4),Card(13,4),Card(14,4),Card(3,4),Card(2,8)]
    res = self.E.checkFlash(cards)
    self.assertEqual(14, res)
    cards = [Card(2,16),Card(12,16),Card(11,16),Card(13,16),Card(14,2),Card(3,16),Card(2,16)]
    res = self.E.checkFlash(cards)
    self.assertEqual(13, res)
    cards = [Card(2,2),Card(12,2),Card(11,4),Card(13,4),Card(14,4),Card(3,4),Card(2,8)]
    res = self.E.checkFlash(cards)
    self.assertEqual(-1, res)

  def testFullHouse(self):
    cards = [Card(2,2),Card(12,2),Card(3,4),Card(3,4),Card(14,4),Card(3,4),Card(2,8)]
    flg, r1,r2 = self.E.checkFullHouse(cards)
    self.assertEqual(3, r1)
    self.assertEqual(2, r2)
    cards = [Card(4,2),Card(12,2),Card(4,4),Card(3,4),Card(2,4),Card(3,4),Card(2,8)]
    flg, r1,r2 = self.E.checkFullHouse(cards)
    self.assertFalse(flg)
    self.assertEqual(-1, r1)
    self.assertEqual(-1, r2)
    cards = [Card(2,2),Card(14,4),Card(14,4),Card(14,4),Card(7,2),Card(14,4),Card(2,2)]
    flg, r1,r2 = self.E.checkFullHouse(cards)
    self.assertTrue(flg)
    self.assertEqual(14, r1)
    self.assertEqual(2, r2)

  def testFourCard(self):
    cards = [Card(2,2),Card(6,4),Card(11,4),Card(5,4),Card(2,4),Card(3,4),Card(2,8)]
    res = self.E.checkFourCard(cards)
    self.assertEqual(-1, res)
    cards = [Card(3,2),Card(7,4),Card(3,4),Card(3,4),Card(7,2),Card(3,4),Card(2,2)]
    res = self.E.checkFourCard(cards)
    self.assertEqual(3, res)

  def testStraightFlash(self):
    cards = [Card(3,4),Card(7,4),Card(6,4),Card(3,2),Card(5,4),Card(4,4),Card(2,4)]
    res = self.E.checkStraightFlash(cards)
    self.assertEqual(7, res)
    cards = [Card(3,4),Card(7,2),Card(6,4),Card(3,2),Card(5,4),Card(4,4),Card(2,4)]
    res = self.E.checkStraightFlash(cards)
    self.assertEqual(6, res)
    cards = [Card(3,4),Card(7,2),Card(6,4),Card(3,2),Card(5,2),Card(4,4),Card(2,4)]
    res = self.E.checkStraightFlash(cards)
    self.assertEqual(-1, res)

if __name__ == '__main__':
    unittest.main()
