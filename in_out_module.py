"""This module will contain functions for reading from file and
for writing to file"""
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

    list_victim_satiety = [cell.satiety * 100 for cell in list_cells if not cell.predator]
    list_predator_satiety = [cell.satiety * 100 for cell in list_cells if cell.predator]

    if len(list_victim) > 0 and len(list_predator) > 0:
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


def read_data(file_name):
    """ Function reads data from 'file_name' file

    Parameters
    ----------
    file_name : string
        name of the data file
    Returns
    ----------
    victims_list : list
        list of the victim's population at the particular moment in time
    predators_list : list
        list of the predator's population at the particular moment in time
    time : list
        list of the particular moments
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

    with open(file_name, 'r') as file:
        for line in file:
            input_data.append(line.split())
    for i in range(1, len(input_data)):
        time_list.append(int(input_data[i][0]))
        victims_list.append(int(input_data[i][1]))
        predators_list.append(int(input_data[i][2]))
        victims_list_mid_age.append(float(input_data[i][3]))
        predators_list_mid_age.append(float(input_data[i][4]))
        victims_list_mid_engine.append(float(input_data[i][5]))
        predators_list_mid_engine.append(float(input_data[i][6]))
        victims_list_mid_satiety.append(float(input_data[i][7]))
        predators_list_mid_satiety.append(float(input_data[i][8]))

    return (time_list,
            victims_list, predators_list,
            victims_list_mid_age, predators_list_mid_age,
            victims_list_mid_engine, predators_list_mid_engine,
            victims_list_mid_satiety, predators_list_mid_satiety,
            )


def save_file(file_name, folder_name):
    """ Function copies 'data.txt' file to 'data_yyyy_mm_dd_hh_mm_ss.txt' file

    Parameters
    ----------
    file_name : string
        name of the data file
    folder_name : string
        name of the data file folder
    Returns
    ----------
    """
    x = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    a = 'data_' + str(x) + '.txt'
    copyfile(file_name, str(a))
    move(str(a), folder_name)
    clean_file(file_name)


def clean_file(file_name):
    """ Function cleans 'data.txt' file

    Parameters
    ----------
    file_name : string
        name of the data file
    Returns
    ----------
    """
    file = open(file_name, 'w')
    file.close()
