import unittest
from game import Game, GameState

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, 10, 10)
    
    def test_init(self):
        self.assertEqual(self.game.getWidth(), 10)
        self.assertEqual(self.game.getHeight(), 8)
        self.assertEqual(self.game.getMinesNum(), 10)
        self.assertEqual(self.game.getSize(), (8, 10))
        self.assertEqual(self.game.gameState, GameState.PLAYING)

    def test_openCell(self):
        self.assertTrue(self.game.openCell(0, 0))
        self.assertTrue(self.game.getCellIsOpen(0, 0))
        self.assertFalse(self.game.openCell(0, 0))
    
    def test_Flag(self):
        self.assertTrue(self.game.setFlag(0, 0))
        self.assertTrue(self.game.getCellHasFlag(0, 0))
        self.assertFalse(self.game.setFlag(0, 0))
        self.assertTrue(self.game.removeFlag(0, 0))
        self.assertFalse(self.game.getCellHasFlag(0, 0))
        self.assertFalse(self.game.removeFlag(0, 0))
    
    def test_getCellDatas(self):
        for i in range(8):
            for j in range(10):
                self.assertTrue(self.game.getCellData(i, j) in range(-1, 9))

    def test_getCellIsOpens(self):
        for i in range(8):
            for j in range(10):
                self.assertFalse(self.game.getCellIsOpen(i, j))
    
    def test_getCellHasFlags(self):
        for i in range(8):
            for j in range(10):
                self.assertFalse(self.game.getCellHasFlag(i, j))
    
    def test_getMap(self):
        self.assertEqual(len(self.game.getMap()), 8)
        self.assertEqual(len(self.game.getMap()[0]), 10)

    def test_getWidth(self):
        self.assertEqual(self.game.getWidth(), 10)
    
    def test_getHeight(self):
        self.assertEqual(self.game.getHeight(), 8)

    def test_getSize(self):
        self.assertEqual((self.game.getSize()), (8, 10))
    
    def test_getMinesNum(self):
        self.assertEqual(self.game.getMinesNum(), 10)

    def test_validPos(self):
        self.assertTrue(self.game.validPos(0, 0))
        self.assertFalse(self.game.validPos(8, 10))
    
    def test_printMap(self):
        self.game.printMap()
    
    def test_printGameState(self):
        self.game.printGameState()
    
    def test_getAdjacent(self):
        print(f"(0, 0)'s adjacent is {self.game.getAdjacent(0, 0)}")
        print(f"(4, 5)'s adjacent is {self.game.getAdjacent(4, 5)}")
        print(f"(7, 4)'s adjacent is {self.game.getAdjacent(7, 4)}")
        

if __name__ == "__main__":
    unittest.main()