from copy import deepcopy
from elma.constants import VERSION_ACROSS
from elma.models import Level
from elma.models import Obj
from elma.models import Picture
from elma.models import Point
from elma.models import Polygon
from elma.models import Top10Time
import unittest


class TestLevelPacking(unittest.TestCase):

    def test_packing(self):
        level = Level()
        # Specify level id to make testing easier
        level.level_id = 2535781587
        level.polygons = [Polygon([Point(0, 0), Point(0, 1), Point(1, 0)])]
        level.pictures = [Picture(Point(0, 0))]
        level.objects = [
            Obj(Point(0, 0), Obj.FLOWER),
            Obj(Point(0, 0), Obj.START),
            Obj(Point(0, 0), Obj.KILLER),
            Obj(Point(0, 0), Obj.FOOD),
            Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_UP),
            Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_DOWN),
            Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_LEFT),
            Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_RIGHT),
            Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_NORMAL)
        ]
        level.top10.single.append(Top10Time(1386, 'player1'))
        level.top10.single.append(Top10Time(1379, 'player2'))
        level.top10.multi.append(Top10Time(709, 'player3', 'player2', True))
        level.top10.multi.append(Top10Time(714, 'player4', 'player1', True))
        original_level = level
        packed = level.pack()
        level = Level.unpack(packed)
        self.assertEqual(2535781587, level.level_id)
        self.assertEqual('Unnamed', level.name)
        self.assertEqual('DEFAULT', level.lgr)
        self.assertEqual('ground', level.ground_texture)
        self.assertEqual('sky', level.sky_texture)

        # polygons
        self.assertEqual(1, len(level.polygons))
        self.assertEqual(Point(0, 0), level.polygons[0].points[0])
        self.assertEqual(Point(0, 1), level.polygons[0].points[1])
        self.assertEqual(Point(1, 0), level.polygons[0].points[2])

        # pictures
        self.assertEqual(1, len(level.pictures))
        picture = level.pictures[0]
        original_picture = original_level.pictures[0]
        self.assertEqual(original_picture.picture_name, picture.picture_name)
        self.assertEqual(original_picture.texture_name, picture.texture_name)
        self.assertEqual(original_picture.mask_name, picture.mask_name)
        self.assertEqual(original_picture.distance, picture.distance)
        self.assertEqual(original_picture.clipping, picture.clipping)

        # objects
        self.assertEqual(9, len(level.objects))
        for expected_obj, obj in zip([
                Obj(Point(0, 0), Obj.FLOWER),
                Obj(Point(0, 0), Obj.START),
                Obj(Point(0, 0), Obj.KILLER),
                Obj(Point(0, 0), Obj.FOOD),
                Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_UP),
                Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_DOWN),
                Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_LEFT),
                Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_RIGHT),
                Obj(Point(0, 0), Obj.FOOD, gravity=Obj.GRAVITY_NORMAL)
                ], level.objects):
            self.assertEqual(expected_obj, obj)

        # top10
        self.assertEqual(2, len(level.top10.single))
        self.assertEqual(2, len(level.top10.multi))
        self.assertEqual(Top10Time(1379, 'player2'), level.top10.single[0])
        self.assertEqual(Top10Time(1386, 'player1'), level.top10.single[1])
        self.assertEqual(Top10Time(709, 'player3', 'player2', True),
                         level.top10.multi[0])
        self.assertEqual(Top10Time(714, 'player4', 'player1', True),
                         level.top10.multi[1])

        # merge top10s
        level2 = deepcopy(level)
        level2.top10.single.append(Top10Time(1383, 'player2'))
        level2.top10.multi.append(Top10Time(714, 'player1', 'player5'))
        level.top10.merge(level2.top10)
        self.assertEqual(3, len(level.top10.single))
        self.assertEqual(3, len(level.top10.multi))
        self.assertEqual(Top10Time(1379, 'player2'), level.top10.single[0])
        self.assertEqual(Top10Time(1383, 'player2'), level.top10.single[1])
        self.assertEqual(Top10Time(1386, 'player1'), level.top10.single[2])
        self.assertEqual(Top10Time(709, 'player3', 'player2', True),
                         level.top10.multi[0])
        self.assertEqual(Top10Time(714, 'player4', 'player1', True),
                         level.top10.multi[1])
        self.assertEqual(Top10Time(714, 'player1', 'player5', True),
                         level.top10.multi[2])

    def test_packing_across(self):
        level = Level()
        level.version = VERSION_ACROSS
        # Specify level id to make testing easier
        level.level_id = 2535781587
        level.polygons = [Polygon([Point(0, 0), Point(0, 1), Point(1, 0)])]
        level.objects = [
            Obj(Point(0, 0), Obj.FLOWER),
            Obj(Point(0, 0), Obj.START),
            Obj(Point(0, 0), Obj.KILLER),
            Obj(Point(0, 0), Obj.FOOD)
        ]
        packed = level.pack()
        level = level.unpack(packed)
        self.assertEqual(VERSION_ACROSS, level.version)
        self.assertEqual(2535781587, level.level_id)
        self.assertEqual('Unnamed', level.name)

        # polygons
        self.assertEqual(1, len(level.polygons))
        self.assertEqual(Point(0, 0), level.polygons[0].points[0])
        self.assertEqual(Point(0, 1), level.polygons[0].points[1])
        self.assertEqual(Point(1, 0), level.polygons[0].points[2])

        # objects
        self.assertEqual(4, len(level.objects))
        for expected_obj, obj in zip([
                Obj(Point(0, 0), Obj.FLOWER),
                Obj(Point(0, 0), Obj.START),
                Obj(Point(0, 0), Obj.KILLER),
                Obj(Point(0, 0), Obj.FOOD)
                ], level.objects):
            self.assertEqual(expected_obj, obj)
