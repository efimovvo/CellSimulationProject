import unittest
from actions_module import *
from vis_module import *
from main import user_parameters


class ProgramTests(unittest.TestCase):
    """ A class for the main program test."""
    def test_vec_module(self):
        """Tests vec_module function."""

        res = vec_module(np.array([30, 40]))
        self.assertEqual(res, 50.0)

    def test_find_vector(self):
        """Tests find_vector function."""

        # creates 2 cells

        cell1 = Cell(1, 0.8, 1)
        cell2 = Cell(1, 0.8, 1)
        # gives positions to the cells

        cell1.position = np.array([10, 10])
        cell2.position = np.array([1, 1])
        # result of the function

        res = find_vector(cell1, cell2)
        res = list(res)

        # compares result
        self.assertEqual(res, [-9, -9])

    def test_multiply_cell(self):
        """Function tests multiply method of Cell class.
        It is OK if new cell's spawns are not nested to the mother cell

        """

        # the mother cell
        parameters = user_parameters()
        cell = Cell(1, 0.8, 1)
        list_cell = [cell]
        # creates new cell until it will be 'Cell' type
        new_cell = cell.multiply(list_cell, parameters)
        while new_cell == 0:
            new_cell = cell.multiply(list_cell, parameters)

        distance = vec_module(find_vector(new_cell, cell))
        # a final
        self.assertTrue(abs(distance - float(2*new_cell.size)) <= 10**-4)

    def test_change_age_step(self):
        """Tests change_age_step function"""

        cell = Cell(1, 0.8, 1)
        age_step = cell.age_step
        list_cell = [cell]
        # change_age_step increases
        change_age_step(list_cell, 1)
        self.assertEqual(cell.age_step, age_step + 0.001)

        # change_age_step decreases
        change_age_step(list_cell, 2)
        self.assertTrue(abs(cell.age_step - age_step) <= 10**-4)

    def test_change_multiply_skill(self):
        """Function tests change_multiply_skill function"""

        cell = Cell(0.003, 0.8, 0.3)
        multiply_skill = cell.multiply_skill
        list_cell = [cell]
        # multiply_skill increases
        change_multiply_skill(list_cell, 1)
        self.assertEqual(cell.multiply_skill, multiply_skill + 0.02)

        # multiply_skill decreases
        change_multiply_skill(list_cell, 2)
        self.assertEqual(cell.multiply_skill, multiply_skill)

    def test_write_data(self):
        """Function tests write_data function"""

        # clear file
        with open('data.txt', 'w') as data_file:
            print('', file=data_file)

        # create 2 different cells
        cell = Cell(1, 0.8, 1)
        cell_predator = Cell(1, 0.8, 1)
        cell.predator = True
        list_cell = [cell, cell_predator]

        # call write_data_function
        write_data(list_cell, 2)

        # read data
        (time_list,
         victims_list, predators_list,
         victims_list_mid_age, predators_list_mid_age,
         victims_list_mid_engine, predators_list_mid_engine,
         victims_list_mid_satiety, predators_list_mid_satiety) = read_data('data.txt')

        # compare time with 2
        self.assertEqual(time_list, [2])

        # compare amount of victims
        self.assertEqual(victims_list[0], 1)

        # compare amount of predators
        self.assertEqual(predators_list[0], 1)

        with open('data.txt', 'w') as data_file:
            print('', file=data_file)

    def test_kill_the_cell(self):
        """Function tests kill_the_cell function"""

        # create two cells and add to the list:
        cell1 = Cell(1, 0.8, 1)
        cell2 = Cell(1, 0.8, 1)
        list_cell = [cell1, cell2]
        # kill cell1
        kill_the_cell(list_cell, cell1, 1)

        # compare
        self.assertEqual(len(list_cell), 1)

    def test_born_cell(self):
        """Function tests born_the_cell function"""

        # creates the mother cell
        parameters = user_parameters()
        cell = Cell(1, 0.8, 1)
        list_cell = [cell]

        # adds a new cell
        new_cell = cell.multiply(list_cell, parameters)
        while new_cell == 0:
            new_cell = cell.multiply(list_cell, parameters)

        # calls the function
        born_the_cell(list_cell, new_cell, 1)

        # compares result
        self.assertEqual(len(list_cell), 2)


if __name__ == '__main__':
    unittest.main()
