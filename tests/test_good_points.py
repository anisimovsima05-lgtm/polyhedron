import unittest
from common.r3 import R3
from shadow.polyedr import Polyedr


class TestGoodPoints(unittest.TestCase):
    """Тесты для проверки 'хороших' точек и длин проекций."""

    def test_is_good_inside_sphere(self):
        # Точка внутри сферы — не хорошая.
        p = R3(0.5, 0.5, 0.5)  # 0.75 < 1
        self.assertFalse(p.is_good())

    def test_is_good_outside_sphere(self):
        # Точка вне сферы — хорошая.
        p = R3(1.0, 1.0, 1.0)  # 3 > 1
        self.assertTrue(p.is_good())

    def test_is_good_on_sphere(self):
        # Точка на сфере — не хорошая (строго вне!).
        p = R3(1.0, 0.0, 0.0)  # 1 == 1
        self.assertFalse(p.is_good())

    def test_is_good_origin(self):
        # Начало координат — не хорошая.
        p = R3(0.0, 0.0, 0.0)  # 0 < 1
        self.assertFalse(p.is_good())

    def test_proj_length_horizontal(self):
        # Длина проекции горизонтального отрезка.
        a = R3(0.0, 0.0, 0.0)
        b = R3(3.0, 4.0, 0.0)
        self.assertAlmostEqual(a.proj_dist(b), 5.0)

    def test_proj_length_vertical_z(self):
        # Длина проекции вертикального отрезка (вдоль Z) = 0.
        a = R3(1.0, 2.0, 0.0)
        b = R3(1.0, 2.0, 10.0)
        self.assertAlmostEqual(a.proj_dist(b), 0.0)

    def test_proj_length_3d(self):
        # Длина проекции 3D отрезка на XY.
        a = R3(0.0, 0.0, 100.0)
        b = R3(3.0, 4.0, -50.0)
        self.assertAlmostEqual(a.proj_dist(b), 5.0)

    def test_all_bad_polyedr(self):
        # Все вершины внутри сферы → сумма = 0.
        p = Polyedr("data/test_all_bad.geom")
        self.assertAlmostEqual(p.calc_good_edges_proj_sum(), 0.0)

    def test_all_good_polyedr(self):
        # Все вершины вне сферы → сумма всех проекций.
        p = Polyedr("data/test_all_good.geom")
        expected = 4 * (2**0.5) + 8  # 4√2 + 8
        self.assertAlmostEqual(
            p.calc_good_edges_proj_sum(), expected, places=5)

    def test_mixed_polyedr(self):
        # Смешанный случай — часть вершин внутри, часть вне.
        p = Polyedr("data/test_mixed.geom")
        expected = 2 * (1.53**0.5) + 2 * (3.33**0.5) + 3.0
        self.assertAlmostEqual(
            p.calc_good_edges_proj_sum(), expected, places=3)


if __name__ == '__main__':
    unittest.main()
