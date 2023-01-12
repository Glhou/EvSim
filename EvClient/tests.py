import unittest
import util.chooseGenerator as cg


class ChooseGeneratorTests(unittest.TestCase):
    def testNoInput(self):
        generators = []
        radius = 1
        self.assertEqual(cg.choose(generators, radius), -1)

    def testNormalDistance(self):
        generators = [{'port': 1, 'dist': 2, 'price': 1},
                      {'port': 2, 'dist': 3, 'price': 1}]
        radius = 2.5
        self.assertEqual(cg.choose(generators, radius), 1)

    def testNormalPrice(self):
        generators = [{'port': 1, 'dist': 1, 'price': 2},
                      {'port': 2, 'dist': 1, 'price': 1}]
        radius = 2
        self.assertEqual(cg.choose(generators, radius), 2)

    def testSamePriceSameDist(self):
        generators = [{'port': 1, 'dist': 1, 'price': 1},
                      {'port': 2, 'dist': 1, 'price': 1}]
        radius = 2
        self.assertIn(cg.choose(generators, radius), [1, 2])


if __name__ == '__main__':
    unittest.main()
