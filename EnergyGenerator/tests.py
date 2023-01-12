import unittest
import util.auction as au


class ClosestTest(unittest.TestCase):

    def test_only_one(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 1,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_multiple_positive(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 1,
            "CarLon": 0
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 2,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_multiple_negative(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -1,
            "CarLon": 0
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -2,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_mutltiple_negative_float(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -1.5,
            "CarLon": 0
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -2.5,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_multiple_negative_and_positive_float(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -1.5,
            "CarLon": 0
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 2.5,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_multiple_negative_and_positive_float_with_lat_and_lon(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -1.5,
            "CarLon": 0.5
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 2.5,
            "CarLon": 1
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_second_is_closest(self):
        bids = [{
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 2.5,
            "CarLon": 1
        }, {
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": -1.5,
            "CarLon": 0.5
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[1])

    def test_with_ten_bids(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 1,
            "CarLon": 0
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 2,
            "CarLon": 0
        }, {
            "CarId": "ev-3",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 3,
            "CarLon": 0
        }, {
            "CarId": "ev-4",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 4,
            "CarLon": 0
        }, {
            "CarId": "ev-5",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 5,
            "CarLon": 0
        }, {
            "CarId": "ev-6",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 6,
            "CarLon": 0
        }, {
            "CarId": "ev-7",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 7,
            "CarLon": 0
        }, {
            "CarId": "ev-8",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 8,
            "CarLon": 0
        }, {
            "CarId": "ev-9",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 9,
            "CarLon": 0
        }, {
            "CarId": "ev-10",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 10,
            "CarLon": 0
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])

    def test_square_corner(self):
        bids = [{
            "CarId": "ev-1",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 0.6,
            "CarLon": 0.6,
        }, {
            "CarId": "ev-2",
            "CarEnergy": 100,
            "CarRadius": 100,
            "CarLat": 0,
            "CarLon": 1
        }]
        pos = {
            "lat": 0,
            "lon": 0
        }
        self.assertEqual(au.searchClosest(bids, pos), bids[0])


if __name__ == '__main__':
    unittest.main()
