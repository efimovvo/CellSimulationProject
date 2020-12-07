'''This module will contain functions for reading from file and
for writing to file'''
from shutil import copyfile, move
import datetime


def write_data(list_cells, time):
    """ Function add line in data.txt file

    Parameters
    ----------
    list_cells : list
        list of cells
    time : int
        current time = step of modelling

    Returns
    ----------
    """
    list_victim = [cell for cell in list_cells if not cell.predator]
    list_predator = [cell for cell in list_cells if cell.predator]

    list_victim_age = [cell.age for cell in list_cells if not cell.predator]
    list_predator_age = [cell.age for cell in list_cells if cell.predator]

    list_victim_engine = [cell.engines for cell in list_cells if not cell.predator]
    list_predator_engine = [cell.engines for cell in list_cells if cell.predator]

    list_victim_satiety = [cell.satiety for cell in list_cells if not cell.predator]
    list_predator_satiety = [cell.satiety for cell in list_cells if cell.predator]

    if list_victim != 0:
        with open('data.txt', 'a') as file:
            cell_data = [str(time),
                         str(len(list_victim)),
                         str(len(list_predator)),
                         str(sum(list_victim_age) / len(list_victim_age)),
                         str(sum(list_predator_age) / len(list_predator_age)),
                         str(sum(list_victim_engine) / len(list_victim_engine)),
                         str(sum(list_predator_engine) / len(list_predator_engine)),
                         str(sum(list_victim_satiety) / len(list_victim_satiety)),
                         str(sum(list_predator_satiety) / len(list_predator_satiety)),
                         ]
            cell_data = ' '.join(cell_data)
            cell_data = cell_data + '\n'
            file.write(cell_data)


def read_data():
    """ Function reads data from data.txt file

    Parameters
    ----------

    Returns
    ----------
    victims_list : list
        list of victim population at the moments in time
    predators_list : list
        list of predator population at the moments in time
    time : list
        list of time moments
    """
    time_list = []
    input_data = []
    victims_list = []
    predators_list = []
    victims_list_mid_age = []
    predators_list_mid_age = []
    victims_list_mid_engine = []
    predators_list_mid_engine = []
    victims_list_mid_satiety = []
    predators_list_mid_satiety = []

    with open('data.txt', 'r') as file:
        for line in file:
            input_data.append(line.split())
    for i in range(1, len(input_data)):
        time_list.append(int(input_data[i][0]))
        victims_list.append(int(input_data[i][1]))
        predators_list.append(int(input_data[i][2]))
        victims_list_mid_age.append(float(input_data[i][3]))
        predators_list_mid_age.append(float(input_data[i][3]))
        victims_list_mid_engine.append(float(input_data[i][3]))
        predators_list_mid_engine.append(float(input_data[i][3]))
        victims_list_mid_satiety.append(float(input_data[i][3]))
        predators_list_mid_satiety.append(float(input_data[i][3]))

    return (time_list,
            victims_list, predators_list,
            victims_list_mid_age, predators_list_mid_age,
            victims_list_mid_engine, predators_list_mid_engine,
            victims_list_mid_satiety, predators_list_mid_satiety,
            )


def save_file():
    """ Function copy data.txt file to data_yyyy_mm_dd_hh_mm_ss.txt file

    Parameters
    ----------

    Returns
    ----------
    """
    x = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    a = 'data_' + str(x) + '.txt'
    copyfile('data.txt', str(a))
    move(str(a), 'database')
    file = open('data.txt', 'w')
    file.close()